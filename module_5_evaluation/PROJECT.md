# Module 5 Project: Building a Judge Agent

## Project Overview

**What we're building:** A judge agent that evaluates AI outputs using the LLM-as-judge pattern with configurable rubrics and multi-criteria scoring.

**Why we're building it:** After Modules 1-4 taught you to build agents, you need to measure if they're actually good. This module gives you the tools to evaluate quality systematically.

**Key features:**
- Multi-criteria evaluation with detailed reasoning
- Comparison mode to rank multiple outputs
- Configurable rubrics (JSON format)
- Structured output for analysis
- Evaluation logging

---

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                      Judge Agent                            │
│                                                             │
│  ┌──────────────┐         ┌─────────────────┐             │
│  │  Load Rubric │────────▶│ Evaluation Core │             │
│  │   (JSON)     │         │                 │             │
│  └──────────────┘         │  - Prompt       │             │
│                           │  - LLM call     │             │
│                           │  - Parse result │             │
│                           └─────────────────┘             │
│                                   │                        │
│                          ┌────────┴────────┐              │
│                          ▼                 ▼              │
│                  ┌──────────────┐  ┌──────────────┐       │
│                  │   Single     │  │  Comparison  │       │
│                  │  Evaluation  │  │     Mode     │       │
│                  └──────────────┘  └──────────────┘       │
│                          │                 │              │
│                          ▼                 ▼              │
│                  ┌─────────────────────────────┐          │
│                  │   Structured Output         │          │
│                  │   (scores + reasoning)      │          │
│                  └─────────────────────────────┘          │
│                                   │                        │
│                                   ▼                        │
│                           ┌──────────────┐                │
│                           │ Log to JSONL │                │
│                           └──────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

**1. JudgeAgent Class**
- Main entry point
- Loads and stores rubric
- Orchestrates evaluation flow

**2. Rubric System**
- JSON files define evaluation criteria
- Stored in `SOLUTION/rubrics/`
- Loaded at runtime

**3. Evaluation Modes**
- **Single evaluation:** Score one output
- **Comparison mode:** Rank multiple outputs

**4. Output Parser**
- Extracts scores from LLM response
- Extracts reasoning for each criterion
- Handles malformed responses gracefully

**5. Logger**
- Writes to JSONL files
- Separate files for evaluations vs comparisons
- Stores truncated outputs + full results

---

## Design Decisions

### Decision 1: Fixed Rubrics vs Dynamic Rubrics

**Options:**
- A) Load rubrics from JSON files (fixed)
- B) Generate rubrics dynamically with LLM
- C) Hybrid (templates + dynamic adjustment)

**Chosen:** A (Fixed rubrics)

**Rationale:**
- Consistency: Same criteria across evaluations
- Transparency: Rubrics are readable, auditable
- Cost: No LLM call needed to generate rubric
- Simplicity: Easier to understand and debug

**Trade-off:** Less flexible, but for learning and most use cases, fixed rubrics are better.

### Decision 2: Structured Output Parsing

**Options:**
- A) Ask LLM to return JSON
- B) Use format instructions, parse with regex
- C) Structured output mode (OpenAI function calling)

**Chosen:** B (Format instructions + parsing)

**Rationale:**
- Reliability: Format instructions are well-understood by models
- Compatibility: Works with all models (not just OpenAI)
- Observability: Raw response is visible for debugging
- Simplicity: No need for JSON schema definitions

**Trade-off:** Parsing is more fragile than structured output mode, but prompts work well enough.

### Decision 3: Single Judge vs Judge Panel

**Options:**
- A) Single judge (one LLM call)
- B) Judge panel (multiple judges, aggregate)
- C) Configurable (user chooses)

**Chosen:** A (Single judge), explain B in CONCEPTS.md

**Rationale:**
- Cost: 3x cheaper than panel
- Speed: 3x faster than panel
- Simplicity: Easier to understand
- Extendable: Users can implement panels if needed

**Trade-off:** More bias, less robust. But for learning/low-stakes, single judge is fine.

### Decision 4: Absolute Scores vs Comparative Ranking

**Options:**
- A) Only absolute scores (evaluate outputs independently)
- B) Only comparative ranking (rank outputs against each other)
- C) Both (separate methods)

**Chosen:** C (Both methods)

**Rationale:**
- **Absolute scores:** Good for understanding individual quality
- **Comparative ranking:** Good for choosing between options
- Both are useful in different scenarios
- Implementation overhead is low

### Decision 5: Evaluation Logging

**Options:**
- A) No logging (ephemeral results)
- B) Log to JSONL files
- C) Log to database (SQLite)

**Chosen:** B (JSONL files)

**Rationale:**
- Simplicity: No database setup needed
- Portability: JSONL is human-readable, easy to parse
- Append-only: Safe for concurrent writes
- Analysis-friendly: Easy to load into pandas/analysis tools

**Trade-off:** Less queryable than database, but simpler for learning context.

### Decision 6: Temperature Setting

**Options:**
- A) High temperature (0.7+) for creativity
- B) Low temperature (0.3 or less) for consistency
- C) Let user configure

**Chosen:** B (Low temperature, 0.3)

**Rationale:**
- Consistency: Evaluation should be deterministic-ish
- Reliability: Lower variance in scores
- Fairness: Same output should get similar scores each time

**Trade-off:** Less "creative" reasoning, but evaluation needs consistency, not creativity.

### Decision 7: Error Handling

**Options:**
- A) Fail loudly (raise exceptions)
- B) Fail gracefully (return None, log error)
- C) Retry with fallback

**Chosen:** A (Fail loudly) for learning, B for production

**Rationale:**
- Learning context: Students need to see errors
- Debugging: Exceptions are more informative than silent failures
- Simplicity: No retry logic complexity

**Production recommendation:** Add retry logic and graceful degradation.

---

## Implementation Details

### File Structure

```
module_5_evaluation/
├── SOLUTION/
│   ├── judge_agent.py          # Main implementation
│   └── rubrics/
│       ├── code_quality.json   # For evaluating code
│       ├── content_quality.json # For evaluating writing
│       └── customer_service.json # For evaluating support responses
├── logs/
│   ├── evaluations.jsonl       # Single evaluation logs
│   └── comparisons.jsonl       # Comparison logs
├── CONCEPTS.md                 # Theory and patterns
├── PROJECT.md                  # This file
└── README.md                   # Module overview
```

### Key Functions

**`JudgeAgent.__init__(rubric_path)`**
- Initialize judge with rubric
- Load rubric from JSON file
- Store in `self.rubric`

**`JudgeAgent.evaluate(output, context, log_results)`**
- Evaluate single output
- Build prompt with rubric criteria
- Call LLM, parse response
- Return structured results
- Optionally log to JSONL

**`JudgeAgent.compare(outputs, labels, context, log_results)`**
- Evaluate multiple outputs, rank them
- Build comparison prompt
- Call LLM, parse rankings
- Return structured results
- Optionally log to JSONL

**`_build_evaluation_prompt(output, context)`**
- Construct prompt for single evaluation
- Include rubric criteria and indicators
- Specify output format

**`_build_comparison_prompt(outputs, labels, context)`**
- Construct prompt for comparison
- Include all outputs with labels
- Specify ranking format

**`_parse_evaluation(response, eval_time)`**
- Extract scores from LLM response
- Extract reasoning for each criterion
- Calculate average score
- Return structured dict

**`_parse_comparison(response, labels, eval_time)`**
- Extract ranking from LLM response
- Extract criterion analysis
- Return structured dict

**`_log_evaluation(output, context, result)`**
- Write evaluation to JSONL file
- Include timestamp and metadata

**`_log_comparison(outputs, labels, context, result)`**
- Write comparison to JSONL file
- Include timestamp and metadata

### Rubric JSON Schema

```json
{
  "name": "Rubric Name",
  "description": "What this rubric evaluates",
  "version": "1.0",
  "scale": {
    "min": 1,
    "max": 5,
    "type": "Likert (1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent)"
  },
  "criteria": [
    {
      "name": "Criterion Name",
      "description": "What this criterion measures",
      "indicators": [
        "Indicator 1",
        "Indicator 2",
        "Indicator 3"
      ]
    }
  ],
  "use_cases": [
    "Use case 1",
    "Use case 2"
  ]
}
```

### Evaluation Output Schema

```python
{
    "scores": {
        "Criterion 1": 4,
        "Criterion 2": 5,
        "Criterion 3": 3
    },
    "reasoning": {
        "Criterion 1": "Detailed explanation...",
        "Criterion 2": "Detailed explanation...",
        "Criterion 3": "Detailed explanation..."
    },
    "average_score": 4.0,
    "overall_assessment": "Summary of strengths and weaknesses...",
    "metadata": {
        "rubric": "Rubric Name",
        "model": "gpt-4o-mini",
        "timestamp": "2025-12-22T10:30:00",
        "tokens_used": 450,
        "evaluation_time_seconds": 2.3
    },
    "raw_response": "Full LLM response for debugging..."
}
```

### Comparison Output Schema

```python
{
    "ranking": ["Output 1", "Output 3", "Output 2"],  # 1st to last
    "criterion_analysis": {
        "Criterion 1": "Comparison explanation...",
        "Criterion 2": "Comparison explanation...",
        "Criterion 3": "Comparison explanation..."
    },
    "overall_reasoning": "Why this ranking...",
    "metadata": {
        "rubric": "Rubric Name",
        "model": "gpt-4o-mini",
        "timestamp": "2025-12-22T10:30:00",
        "tokens_used": 650,
        "evaluation_time_seconds": 3.1,
        "num_outputs_compared": 3
    },
    "raw_response": "Full LLM response for debugging..."
}
```

---

## Testing Strategy

### Unit Tests (Recommended, Not Implemented)

```python
def test_rubric_loading():
    judge = JudgeAgent(rubric_path="rubrics/code_quality.json")
    assert judge.rubric is not None
    assert judge.rubric['name'] == "Code Quality Rubric"

def test_evaluation_output_structure():
    judge = JudgeAgent(rubric_path="rubrics/content_quality.json")
    result = judge.evaluate("Sample text", log_results=False)
    assert 'scores' in result
    assert 'reasoning' in result
    assert 'average_score' in result
    assert 'metadata' in result

def test_comparison_output_structure():
    judge = JudgeAgent(rubric_path="rubrics/code_quality.json")
    result = judge.compare(
        outputs=["code A", "code B"],
        labels=["A", "B"],
        log_results=False
    )
    assert 'ranking' in result
    assert 'criterion_analysis' in result
    assert len(result['ranking']) == 2
```

### Integration Tests (Manual Demos)

The `demo_single_evaluation()` and `demo_comparison()` functions serve as integration tests:
- Test actual LLM calls
- Verify prompt construction
- Verify output parsing
- Verify logging

**Run with:**
```bash
python SOLUTION/judge_agent.py
```

### Bias Testing (Recommended Exercise)

```python
# Test position bias
outputs = ["Output A", "Output B", "Output C"]
result1 = judge.compare(outputs, labels=["A", "B", "C"])
result2 = judge.compare(outputs[::-1], labels=["C", "B", "A"])
# Compare rankings - should be consistent

# Test length bias
short = "Brief answer."
long = "Brief answer. " + " ".join(["Filler."] * 50)
result_short = judge.evaluate(short)
result_long = judge.evaluate(long)
# Compare scores - should judge on quality, not length
```

---

## Extension Ideas

After completing the base implementation, consider extending with:

**1. Judge Panel Implementation**
- Create `JudgePanelAgent` class
- Run 3-5 judges, aggregate scores
- Identify disagreements for human review

**2. Calibration System**
- Create calibration dataset with human ratings
- Compare judge scores to human scores
- Tune rubric based on misalignments

**3. Bias Detection Tool**
- Automated tests for position, length, verbosity bias
- Report on bias metrics
- Suggest rubric adjustments

**4. Visualization Dashboard**
- Plot score distributions
- Show criterion breakdowns
- Track scores over time

**5. Custom Rubric Generator**
- LLM generates rubric from task description
- User reviews and edits
- Save as JSON for reuse

**6. A/B Testing Framework**
- Compare two agents systematically
- Statistical significance testing
- Recommendation on which agent is better

---

## Common Pitfalls and Solutions

### Pitfall 1: Vague Rubric Criteria

**Problem:** "Quality: Is this good?" is too vague
**Solution:** Be specific. "Clarity: Is the writing easy to understand, with well-explained concepts?"

### Pitfall 2: Too Many Criteria

**Problem:** 10 criteria makes evaluation arbitrary
**Solution:** Stick to 3-5 most important criteria

### Pitfall 3: Overlapping Criteria

**Problem:** "Clarity" and "Understandability" measure the same thing
**Solution:** Ensure criteria are independent dimensions

### Pitfall 4: Ignoring Bias

**Problem:** Assuming judge is objective
**Solution:** Test for bias, acknowledge limitations, consider judge panels

### Pitfall 5: Not Logging Results

**Problem:** Can't analyze trends or debug issues
**Solution:** Always log evaluations (set `log_results=True`)

### Pitfall 6: High Temperature

**Problem:** Temperature 0.7+ causes inconsistent scores
**Solution:** Use low temperature (0.3 or less) for evaluation

### Pitfall 7: Parsing Failures

**Problem:** LLM doesn't follow format, parsing breaks
**Solution:** Include error handling, log raw responses, refine prompts

---

## Seed Questions for Learning

Use these questions to deepen your understanding as you work through the module:

### Foundational Understanding (Questions 1-5)

1. **What is the difference between a Critic (Module 4) and a Judge (Module 5)?**
   - Hint: Think about timing, purpose, and output format

2. **Why use an LLM for evaluation instead of traditional metrics?**
   - Hint: What tasks are LLMs good at vs bad at?

3. **What makes a good rubric?**
   - Hint: Consider specificity, measurability, independence of criteria

4. **Why is bias a problem in LLM-as-judge systems?**
   - Hint: Think about the fox-guarding-henhouse analogy

5. **When would you use single evaluation vs comparison mode?**
   - Hint: When do you need absolute scores vs relative rankings?

### Architecture and Design (Questions 6-10)

6. **Why did we choose fixed rubrics instead of dynamically generated rubrics?**
   - Hint: Consider consistency, transparency, cost

7. **Why use JSONL format for logging instead of JSON or a database?**
   - Hint: Think about append operations, human readability, simplicity

8. **What's the advantage of separating prompt building from LLM calling?**
   - Hint: Testing, debugging, observability

9. **Why set temperature to 0.3 for evaluation instead of 0.7?**
   - Hint: What matters more for evaluation - creativity or consistency?

10. **How would you add a weighted scoring system?**
    - Hint: Where would weights be stored? How would you calculate weighted average?

### Bias and Limitations (Questions 11-15)

11. **How would you test for position bias in a judge?**
    - Hint: What happens if you shuffle the order of outputs?

12. **What's the fox-guarding-henhouse problem in agent evaluation?**
    - Hint: What if the same company builds the agent and the judge?

13. **How can you tell if your judge is too lenient or too harsh?**
    - Hint: Compare to human ratings, look at score distributions

14. **Why might a judge prefer longer outputs even if they're worse?**
    - Hint: What biases exist in LLM training data?

15. **How would you use a calibration dataset to improve a judge?**
    - Hint: What do you compare? What do you adjust?

### Advanced Patterns (Questions 16-20)

16. **How would you implement a judge panel with 3 judges?**
    - Hint: How do you aggregate scores? What do you do with disagreements?

17. **When would you choose comparison mode over single evaluation?**
    - Hint: When is relative quality more important than absolute scores?

18. **How would you build a self-improving judge?**
    - Hint: What feedback would you collect? How would you use it?

19. **What's the trade-off between detailed rubrics and simple rubrics?**
    - Hint: Consistency vs flexibility, clear criteria vs overfitting

20. **How would you evaluate a judge (meta-evaluation)?**
    - Hint: Inter-judge agreement, correlation with humans, bias detection

---

## Real-World Applications

### Application 1: Code Review Automation

**Scenario:** Your team uses coding agents. You want to evaluate code quality before merging.

**Implementation:**
```python
judge = JudgeAgent(rubric_path="rubrics/code_quality.json")

# Evaluate agent-generated code
result = judge.evaluate(
    output=generated_code,
    context="Task: Implement user authentication endpoint"
)

# Only merge if average score >= 4.0
if result['average_score'] >= 4.0:
    print("✅ Code quality passed, ready to merge")
else:
    print(f"❌ Code quality too low: {result['average_score']}")
    print("Issues:", result['reasoning'])
```

### Application 2: A/B Testing Content Generators

**Scenario:** You have two blog post generators. Which one is better?

**Implementation:**
```python
judge = JudgeAgent(rubric_path="rubrics/content_quality.json")

# Generate posts with both agents
post_a = agent_a.generate(topic)
post_b = agent_b.generate(topic)

# Compare
result = judge.compare(
    outputs=[post_a, post_b],
    labels=["Agent A", "Agent B"],
    context=f"Topic: {topic}"
)

print(f"Winner: {result['ranking'][0]}")
print(f"Reasoning: {result['overall_reasoning']}")
```

### Application 3: Customer Service Quality Monitoring

**Scenario:** Your support chatbot handles 1000 tickets/day. You want to monitor quality.

**Implementation:**
```python
judge = JudgeAgent(rubric_path="rubrics/customer_service.json")

# Evaluate random sample of responses
for ticket in random.sample(tickets, 50):
    result = judge.evaluate(
        output=ticket['bot_response'],
        context=f"Customer question: {ticket['question']}"
    )
    # Log results for analysis

# Analyze: Are scores trending down? Which criteria are weak?
```

### Application 4: Training Data Curation

**Scenario:** You're building a fine-tuned model. You need high-quality training examples.

**Implementation:**
```python
judge = JudgeAgent(rubric_path="rubrics/content_quality.json")

# Evaluate all candidate examples
high_quality_examples = []
for example in candidate_examples:
    result = judge.evaluate(example)
    if result['average_score'] >= 4.5:
        high_quality_examples.append(example)

# Use only high-quality examples for training
print(f"Selected {len(high_quality_examples)} / {len(candidate_examples)} for training")
```

---

## Success Criteria

You've successfully completed this module when:

✅ **Understand Judge vs Critic distinction**
- You can explain when to use each
- You understand timing, purpose, output differences

✅ **Can design effective rubrics**
- Rubrics have 3-5 specific, independent criteria
- Criteria are measurable with clear indicators

✅ **Understand bias and mitigation strategies**
- You can explain the fox-guarding-henhouse problem
- You know how to test for position, length, verbosity bias
- You understand when to use judge panels, calibration, human feedback

✅ **Can implement and extend the judge agent**
- Code runs without errors
- Evaluations return structured output
- Comparisons rank outputs correctly
- Logging works

✅ **Can analyze evaluation results**
- Load and parse JSONL logs
- Calculate average scores and distributions
- Identify trends and patterns

✅ **Can apply judges to real problems**
- Evaluate agent outputs
- Compare different implementations
- Monitor quality over time

---

## Learning Workflow

**Recommended sequence:**

1. **Read CONCEPTS.md** - Understand theory, patterns, bias
2. **Study example rubrics** - See what good rubrics look like
3. **Run demo code** - See judge in action
4. **Design your own rubric** - For a domain you care about
5. **Test for bias** - Shuffle orders, vary lengths
6. **Analyze results** - Load logs, compute stats
7. **Extend the system** - Add features (panels, calibration, etc.)

**Time estimate:** 4-6 hours for core module, 10+ hours with extensions

---

## Next Module Preview

**Module 6: Visual Recognition (Part 1)** - Apply RAG patterns to image recognition with vector databases.

After measuring text quality with judges, you'll learn to work with images, embeddings, and similarity search.
