# Module 5: LLM as Judge & Evaluation

## ✅ Released December 29, 2025 (Week 5)

Build evaluation systems to measure agent quality—implement the LLM-as-judge pattern with rubrics and multi-criteria scoring.

## Learning Objectives
- Design evaluation rubrics for agent outputs
- Implement the LLM-as-judge pattern
- Build multi-criteria scoring systems
- Create quality metrics and benchmarks
- Understand bias mitigation in evaluation

## Concepts Covered
- LLM as evaluator/judge
- Rubric design principles
- Multi-criteria evaluation
- Scoring methods (Likert scale, binary, weighted)
- Judge panels and consensus mechanisms
- Evaluation logging and analysis

## Project: `judge_agent.py`

### Requirements
- Configurable evaluation rubrics (criteria + scoring scales)
- LLM-as-judge implementation (evaluator agent)
- Multi-criteria scoring (quality, relevance, accuracy, etc.)
- Structured evaluation output (scores + reasoning)
- Evaluation logging for analysis
- Comparison mode (evaluate multiple agent outputs)

### Success Criteria
✅ Rubrics clearly define evaluation criteria
✅ Judge agent produces scores with detailed reasoning
✅ Multi-criteria evaluation works across different dimensions
✅ Evaluation results are logged and analyzable
✅ System can compare multiple outputs and rank them
✅ Bias mitigation strategies are documented

## Files in This Module
- `SOLUTION/judge_agent.py` - LLM-as-judge implementation
- `SOLUTION/rubrics/` - Example evaluation rubrics
- `logs/` - Evaluation results and analysis
- `CONCEPTS.md` - Theory: Evaluation methods, rubric design
- `PROJECT.md` - Architecture: Design decisions, seed questions
- `README.md` - This file - Module overview

## Key Features

**What the judge agent demonstrates:**
- **Rubric-based evaluation** - Structured criteria and scoring
- **Reasoning transparency** - Judges explain their scores
- **Multi-dimensional** - Evaluate across multiple criteria
- **Comparative analysis** - Rank multiple outputs
- **Bias awareness** - Understand and mitigate evaluation biases

## Reflection Questions
After completing this module, answer:
1. How do rubrics improve evaluation consistency?
2. What biases did you notice in LLM-as-judge evaluation?
3. When should you use multiple judges vs single judge?
4. How would you validate that your evaluations are accurate?
5. What's the trade-off between detailed rubrics and flexibility?

## Common Evaluation Patterns

**Pattern 1: Single Judge, Single Criterion**
- Simplest approach
- Use when: One clear quality dimension (e.g., "Is this summary accurate?")

**Pattern 2: Single Judge, Multi-Criteria**
- Most common pattern
- Use when: Multiple quality dimensions (accuracy, relevance, clarity)

**Pattern 3: Judge Panel, Consensus**
- Multiple judges score independently, aggregate results
- Use when: High-stakes decisions or bias mitigation needed

**Pattern 4: Comparative Ranking**
- Judge compares multiple outputs, ranks them
- Use when: Relative quality matters more than absolute scores

## Learning Workflow

**Recommended path through this module:**

### Step 1: Understand the Concepts (1-2 hours)
📖 **Read [CONCEPTS.md](CONCEPTS.md)** - Start here!

Key sections to focus on:
- **Judge vs Critic** - Understand the critical distinction (Factory QC vs YouTube reviewer)
- **Bias in LLM Evaluation** - The fox-guarding-henhouse problem
- **Rubric Design** - What makes a good rubric?
- **Evaluation Patterns** - When to use what

**Checkpoint:** Can you explain the mountain bike analogy? (Factory QC = Critic, YouTube reviewer = Judge)

### Step 2: Study the Implementation (30-60 minutes)
📂 **Explore [SOLUTION/](SOLUTION/)**

1. **Read the rubrics** - See what good rubrics look like:
   - [code_quality.json](SOLUTION/rubrics/code_quality.json) - For evaluating code
   - [content_quality.json](SOLUTION/rubrics/content_quality.json) - For evaluating writing
   - [customer_service.json](SOLUTION/rubrics/customer_service.json) - For evaluating support responses

2. **Study [judge_agent.py](SOLUTION/judge_agent.py)** - See the implementation:
   - How rubrics are loaded (JSON → Python dict)
   - How prompts are built (rubric + output + context)
   - How responses are parsed (scores + reasoning)
   - How results are logged (JSONL for analysis)

**Checkpoint:** Understand what each function does

### Step 3: Run the Demos (15-30 minutes)
💻 **Execute the code:**

```bash
cd module_5_evaluation/SOLUTION
python judge_agent.py
```

Watch the output:
- **Demo 1:** Single evaluation - See how a blog post is scored across 4 criteria
- **Demo 2:** Comparison mode - See how 3 code implementations are ranked

**Checkpoint:** Can you explain why one output ranked higher than another?

### Step 4: Design Your Own Rubric (30-60 minutes)
✏️ **Create a rubric for your domain**

Think about something you want to evaluate:
- Code for a specific language (Python, JavaScript, etc.)
- A specific type of content (tutorials, documentation, social media posts)
- A specific interaction (sales emails, technical explanations, etc.)

Create `my_rubric.json`:
```json
{
  "name": "My Custom Rubric",
  "description": "Evaluates...",
  "scale": {"min": 1, "max": 5, "type": "Likert"},
  "criteria": [
    {
      "name": "Criterion 1",
      "description": "What this measures...",
      "indicators": ["Good sign 1", "Good sign 2"]
    }
  ]
}
```

**Checkpoint:** Your rubric has 3-5 specific, independent criteria with clear indicators

### Step 5: Test for Bias (30-45 minutes)
🔬 **Run bias experiments:**

**Position Bias Test:**
```python
outputs = ["Output A", "Output B", "Output C"]
result1 = judge.compare(outputs, labels=["A", "B", "C"])
result2 = judge.compare(outputs[::-1], labels=["C", "B", "A"])
# Are rankings consistent?
```

**Length Bias Test:**
```python
short = "Brief but good answer."
long = short + " " + " ".join(["Filler."] * 50)
result_short = judge.evaluate(short)
result_long = judge.evaluate(long)
# Does the judge prefer longer just because it's longer?
```

**Checkpoint:** You've identified at least one bias in the judge

### Step 6: Analyze Results (30-45 minutes)
📊 **Load and analyze evaluation logs:**

```python
import json

# Load evaluations
evaluations = []
with open('../logs/evaluations.jsonl', 'r') as f:
    for line in f:
        evaluations.append(json.loads(line))

# Compute stats
avg_scores = [e['result']['average_score'] for e in evaluations]
print(f"Mean score: {sum(avg_scores) / len(avg_scores):.2f}")

# Find weaknesses
clarity_scores = [e['result']['scores']['Clarity'] for e in evaluations]
print(f"Clarity average: {sum(clarity_scores) / len(clarity_scores):.2f}")
```

**Checkpoint:** You can identify patterns in evaluation data

### Step 7: Read Architecture Details (Optional, 1 hour)
🏗️ **Deep dive: [PROJECT.md](PROJECT.md)**

Study:
- Design decisions and rationales
- Extension ideas (judge panels, calibration, bias detection)
- Real-world applications
- 20 seed questions for deeper understanding

**Checkpoint:** You can answer the seed questions

---

## Quick Start (If You're in a Hurry)

**30-minute speedrun:**
1. Read "Judge vs Critic" and "Bias" sections in [CONCEPTS.md](CONCEPTS.md) (10 min)
2. Run the demos: `python SOLUTION/judge_agent.py` (5 min)
3. Study one rubric: [SOLUTION/rubrics/content_quality.json](SOLUTION/rubrics/content_quality.json) (5 min)
4. Read key functions in [judge_agent.py](SOLUTION/judge_agent.py) (10 min)

**What you'll miss:** Bias testing, custom rubric design, log analysis, architectural details

---

## Real-World Applications

**After completing this module, you can:**

✅ **Evaluate agent outputs systematically**
- Not just "does this look good?" but "scores 4.2/5 on clarity, 3.8/5 on engagement"

✅ **Compare different agents/models/prompts**
- "Agent A scores 4.1 average, Agent B scores 3.7 average → use Agent A"

✅ **Monitor quality over time**
- "Clarity scores dropped from 4.5 to 3.8 this week → investigate"

✅ **Build quality gates**
- "Only merge code with average score ≥ 4.0"

✅ **Understand bias and limitations**
- "Judge prefers longer outputs → add 'appropriate length' criterion"

---

## Next Module

**Module 6: Visual Recognition (Part 1)** (January 5, 2026)
Apply RAG patterns to image recognition with vector databases.

After measuring text quality, you'll learn to work with images, embeddings, and similarity search.
