# Module 5 Concepts: LLM as Judge & Evaluation

## What You'll Learn

This module teaches you how to build evaluation systems for AI agents. After modules 1-4 taught you to build agents, this module shows you how to **measure if they're actually good**.

**Core concepts:**
- Judge vs Critic: Standalone evaluator vs in-workflow QC
- Multi-criteria evaluation: Scoring across multiple dimensions
- Rubric design: How to create effective evaluation criteria
- Bias awareness: The fox-guarding-henhouse problem
- Comparison mode: Ranking outputs against each other

---

## Judge vs Critic: Two Different Roles

Before we dive into evaluation techniques, let's clarify a critical distinction:

### Critic (Module 4)
- **Role:** Part of the workflow - acts as quality control gate
- **Purpose:** Block bad outputs, allow good ones through
- **Decision:** Binary (APPROVED / REJECTED)
- **Feedback:** Actionable (tells Worker what to fix)
- **Timing:** Real-time during task execution

**Example:** Factory quality control inspector

### Judge (Module 5)
- **Role:** Standalone evaluator - measures quality after the fact
- **Purpose:** Understand quality, compare options, improve systems
- **Decision:** Multi-dimensional scores + reasoning
- **Feedback:** Analytical (explains strengths and weaknesses)
- **Timing:** After task completion, for analysis

**Example:** Product reviewer on YouTube

### Real-World Analogy: Mountain Bikes

Your company manufactures mountain bikes:

**Critic = Factory QC Inspector**
- Checks each bike before it leaves the factory
- Binary decision: Pass (ship it) or Fail (fix the brakes)
- Part of the manufacturing process
- Goal: Don't ship broken bikes

**Judge = YouTube Bike Reviewer**
- Tests bikes after they're released
- Scores across multiple dimensions (handling, durability, value)
- Independent from manufacturer
- Goal: Help buyers understand quality and compare options

**Key insight:** You need BOTH. The factory QC prevents disasters. The independent reviewer helps you improve and lets customers make informed choices.

In AI systems:
- **Critic:** Prevents your agent from returning garbage results
- **Judge:** Helps you understand if your agent is truly excellent, and how it compares to alternatives

---

## The LLM-as-Judge Pattern

Using an LLM to evaluate outputs is powerful because LLMs excel at nuanced judgment tasks that are hard to capture in rules.

### What Judges Are Good At

**Subjective Quality Assessment:**
- "Is this writing clear and engaging?"
- "Does this code follow best practices?"
- "Is this customer service response empathetic?"

**Comparative Analysis:**
- "Which of these three implementations is better?"
- "Rank these responses from most to least helpful"

**Complex, Multi-Dimensional Evaluation:**
- Scoring across 4-5 criteria simultaneously
- Balancing trade-offs (e.g., accuracy vs brevity)

### What Judges Are Bad At

**Precision Tasks:**
- ❌ "Is this exactly 300 words?" (LLMs can't count reliably)
- ✅ Instead: `word_count = len(text.split())` (Python counts perfectly)

**Absolute Truth:**
- ❌ "Is this factually correct?" (LLMs hallucinate)
- ✅ Instead: Verify against authoritative sources

**Consistency:**
- ❌ Running the same evaluation twice may yield different scores
- ✅ Instead: Use lower temperature, average multiple runs, or use judge panels

### The Hybrid Pattern: Python + LLM

Best practice: Use Python for objective checks, LLM for subjective judgment.

```python
# Python: Objective validation
word_count = len(output.split())
has_examples = "for example" in output.lower()
meets_length = word_count >= 300

# LLM Judge: Subjective quality
prompt = f\"\"\"
OBJECTIVE CHECKS (pre-computed):
✅ Word count: {word_count}/300
✅ Contains examples: {has_examples}

QUALITY EVALUATION:
Evaluate this content for:
1. Clarity: Is the writing clear and easy to understand?
2. Engagement: Is it interesting and well-written?
3. Accuracy: Are the technical claims sound?

[content to evaluate]
\"\"\"
```

**Result:** Reliable validation + nuanced quality assessment.

---

## Bias in LLM Evaluation: The Fox Guarding the Henhouse

Here's the uncomfortable truth: **If you build an agent and a judge to evaluate that agent, you might be creating a biased system.**

### The Problem

Let's say you build an AI writing agent to generate blog posts. Then you build a judge to evaluate those posts. Both use LLMs from the same family (e.g., both use GPT-4).

**What happens?**

The judge might:
- Prefer the writing style that matches its own training data
- Miss flaws that the writer agent consistently makes
- Score favorably on criteria that don't matter to real users
- Give high marks to outputs that *sound good* but lack substance

**This is the fox-guarding-henhouse problem.**

If the judge and the creator share the same biases, limitations, and blind spots, the judge won't catch real problems.

### Real-World Example: Mountain Bike Quality

Imagine you manufacture mountain bikes and want to know if they're good. You have two options:

**Option 1: Internal QC Only** ❌
- Your factory QC team tests bikes
- They're incentivized to ship products
- They might overlook design flaws (because they designed it)
- They don't ride the bikes in real-world conditions like actual riders do

**Option 2: Independent Reviewers** ✅
- Send bikes to professional YouTube reviewers
- They test bikes in real trail conditions
- They compare to competitor bikes
- They represent actual customer perspectives
- They have no incentive to go easy on your product

**Which gives more honest assessment?** The independent reviewers.

### Bias Types in LLM Judges

**1. Position Bias**
- Judge favors the first option in a list (or last option)
- **Mitigation:** Randomize order, run multiple evaluations with shuffled positions

**2. Length Bias**
- Judge assumes longer = more thorough = better
- **Mitigation:** Include "appropriate length" as explicit criterion, test with varying lengths

**3. Verbosity Bias**
- Judge prefers flowery, complex language over simple clarity
- **Mitigation:** Emphasize clarity in rubric, compare against simple reference examples

**4. Style Bias**
- Judge prefers writing that matches its training data style
- **Mitigation:** Use diverse reference examples, specify desired style explicitly

**5. Shared Blind Spots**
- Judge and creator make the same types of mistakes
- **Example:** Both hallucinate similarly, both miss certain factual errors
- **Mitigation:** Use independent validation, fact-check against sources

### Solutions: How to Build More Objective Judges

**1. Independent Teams / Models**
- If possible, use a different model family for evaluation than for generation
- Example: Generate with GPT-4, evaluate with Claude
- Benefit: Different biases might cancel out

**2. Human Feedback Integration**
- Collect real user ratings
- Compare LLM judge scores to human ratings
- Calibrate the judge against human judgment

**3. Calibration Datasets**
- Create a "ground truth" dataset with known quality levels
- Test judge against this dataset
- Tune rubrics until judge agrees with ground truth

**4. Comparative Evaluation**
- Don't just score outputs in isolation
- Compare against known good/bad examples
- Rank outputs against each other

**5. Judge Panels**
- Use multiple judges with different prompts
- Aggregate scores (average or consensus)
- Identify disagreements for human review

**6. Explicit Bias Checks**
- Test judge with shuffled positions
- Test with varying lengths
- Look for systematic patterns in scores

### Practical Recommendations

**For learning/development (low stakes):**
- Single judge is fine
- Focus on clear rubrics
- Accept some bias as trade-off for speed/cost

**For production/high stakes:**
- Use judge panels (3+ judges)
- Calibrate against human feedback
- Monitor for bias over time
- Consider independent model for evaluation

**Red flags that indicate bias:**
- Judge always prefers longer outputs
- Scores are suspiciously high across the board
- Judge scores don't correlate with user satisfaction
- Judge can't distinguish between good and excellent

### The Bottom Line

**You cannot fully eliminate bias**, but you can:
1. **Acknowledge it exists** - Don't pretend your judge is objective
2. **Measure it** - Test for known bias types
3. **Mitigate it** - Use panels, calibration, human feedback
4. **Be transparent** - Document limitations in your evaluation system

**Key insight:** A good judge knows its own limitations. Build judges that are useful despite their biases, not judges that claim to be perfectly objective.

---

## Rubric Design: The Foundation of Good Evaluation

A rubric is a structured set of evaluation criteria. Good rubrics make evaluation consistent, transparent, and actionable.

### Anatomy of a Rubric

```json
{
  "name": "Content Quality Rubric",
  "description": "Evaluates written content...",
  "scale": {
    "min": 1,
    "max": 5,
    "type": "Likert"
  },
  "criteria": [
    {
      "name": "Clarity",
      "description": "Is the writing clear and easy to understand?",
      "indicators": [
        "Ideas are expressed clearly",
        "Jargon is explained or avoided",
        "Flow is logical"
      ]
    }
  ]
}
```

**Key components:**
1. **Name & Description:** What is this rubric for?
2. **Scale:** How are scores represented? (1-5, binary, etc.)
3. **Criteria:** What dimensions are we measuring?
4. **Indicators:** What does "good" look like for each criterion?

### Rubric Design Principles

**1. Specific, Not Vague**

❌ Bad: "Quality: Is this good?"
✅ Good: "Clarity: Is the writing easy to understand, with well-explained concepts and logical flow?"

**2. Measurable**

Each criterion should have clear indicators that help the judge decide.

❌ Bad: "Professionalism: Is it professional?"
✅ Good: "Professionalism: Is the tone courteous? Is grammar correct? Is formatting appropriate?"

**3. Independent Criteria**

Criteria should measure different aspects, not overlap.

❌ Bad: "Clarity" and "Understandability" (too similar)
✅ Good: "Clarity" and "Accuracy" (different dimensions)

**4. Appropriate Granularity**

Too few criteria → Can't capture nuance
Too many criteria → Hard to evaluate, scores become arbitrary

**Sweet spot:** 3-5 criteria for most use cases

**5. Aligned with Purpose**

Rubric should measure what actually matters for the use case.

**Example:** Evaluating customer service chatbot
- ✅ Helpful: "Does this solve the customer's problem?"
- ❌ Not helpful: "Is the response grammatically perfect?" (Nice-to-have, not critical)

### Common Rubric Patterns

**Pattern 1: Quality Dimensions**
Use when: Evaluating creative outputs (writing, code, design)

Criteria: Correctness, Clarity, Completeness, Creativity

**Pattern 2: Task Fulfillment**
Use when: Evaluating if requirements are met

Criteria: Requirements Met, Accuracy, Format Compliance, Timeliness

**Pattern 3: User Experience**
Use when: Evaluating user-facing outputs

Criteria: Helpfulness, Clarity, Empathy, Professionalism

### Fixed vs Dynamic Rubrics

**Fixed Rubrics:**
- Same criteria for all evaluations
- Example: All code evaluated on Correctness, Readability, Documentation
- **Pros:** Consistent, comparable scores over time
- **Cons:** Might not fit every task

**Dynamic Rubrics:**
- Criteria adapt to the specific task
- Example: For math code, emphasize Correctness; for UI code, emphasize Readability
- **Pros:** More relevant to each task
- **Cons:** Scores aren't directly comparable

**Recommendation:** Start with fixed rubrics. Add dynamic elements only if needed.

---

## Evaluation Patterns

### Pattern 1: Single Output, Multi-Criteria

**Use case:** Evaluate one output across multiple dimensions

**Example:**
```python
judge = JudgeAgent(rubric_path="content_quality.json")
result = judge.evaluate(blog_post, context="300-word educational post")
# Returns: Clarity: 4/5, Accuracy: 5/5, Engagement: 3/5, Structure: 4/5
```

**When to use:**
- Testing a single agent's output
- Detailed analysis of one result
- Understanding strengths and weaknesses

### Pattern 2: Multiple Outputs, Comparison

**Use case:** Rank multiple outputs against each other

**Example:**
```python
judge = JudgeAgent(rubric_path="code_quality.json")
result = judge.compare(
    outputs=[implementation_a, implementation_b, implementation_c],
    labels=["Basic", "Improved", "Production"]
)
# Returns: Ranking: 1. Production, 2. Improved, 3. Basic
```

**When to use:**
- A/B testing different approaches
- Choosing the best agent/model for a task
- Benchmarking

### Pattern 3: Binary (Pass/Fail)

**Use case:** Simple threshold check

**Example:**
```json
{
  "scale": {"min": 0, "max": 1, "type": "Binary (0=Fail, 1=Pass)"},
  "criteria": [{"name": "Meets Requirements", "threshold": 1}]
}
```

**When to use:**
- Quick go/no-go decisions
- High-volume screening
- When nuance doesn't matter

**Note:** This is closer to a Critic (Module 4) than a Judge

### Pattern 4: Likert Scale (1-5)

**Use case:** Nuanced quality assessment

**Example:**
```json
{
  "scale": {"min": 1, "max": 5, "type": "Likert"},
  "criteria": [
    {"name": "Clarity", "description": "..."}
  ]
}
```

**When to use:**
- Need to distinguish between "good" and "excellent"
- Tracking improvement over time
- Most general-purpose evaluation

**Scale meanings:**
- 1 = Poor (major problems)
- 2 = Fair (significant issues)
- 3 = Good (acceptable, minor issues)
- 4 = Very Good (high quality, few flaws)
- 5 = Excellent (exceptional quality)

### Pattern 5: Weighted Criteria

**Use case:** Some criteria matter more than others

**Example:**
```python
# In rubric:
{
  "criteria": [
    {"name": "Correctness", "weight": 0.5},  # 50% of score
    {"name": "Readability", "weight": 0.3},   # 30% of score
    {"name": "Documentation", "weight": 0.2}  # 20% of score
  ]
}

# Calculate weighted average:
weighted_score = (
    scores['Correctness'] * 0.5 +
    scores['Readability'] * 0.3 +
    scores['Documentation'] * 0.2
)
```

**When to use:**
- Clear priority hierarchy
- Trade-offs need to be explicit
- Aggregating to single score

---

## Advanced Patterns (Explained, Not Implemented)

These patterns are powerful but add complexity. Module 5 teaches the concepts; you can implement them when needed.

### Judge Panels

**Concept:** Use multiple judges, aggregate their scores

**Why it helps:**
- Reduces impact of individual judge biases
- More robust evaluation (like academic peer review)
- Can identify controversial outputs (high variance in scores)

**Implementation approaches:**

**1. Simple Averaging**
```python
judges = [JudgeAgent(rubric_path) for _ in range(3)]
results = [judge.evaluate(output) for judge in judges]
avg_scores = {
    criterion: sum(r['scores'][criterion] for r in results) / 3
    for criterion in rubric['criteria']
}
```

**2. Consensus (Agreement Required)**
```python
# Only accept if all judges agree within 1 point
def has_consensus(results, tolerance=1):
    for criterion in rubric['criteria']:
        scores = [r['scores'][criterion] for r in results]
        if max(scores) - min(scores) > tolerance:
            return False  # Flag for human review
    return True
```

**3. Weighted Panel (Expert Judges)**
```python
# Give more weight to judges that historically agree with humans
weights = [0.5, 0.3, 0.2]  # Based on calibration
weighted_avg = sum(w * r['scores'][criterion] for w, r in zip(weights, results))
```

**Trade-offs:**
- ✅ More robust, less bias
- ❌ 3x API cost, 3x latency
- **Use when:** High-stakes decisions, need high confidence

### Calibration with Ground Truth

**Concept:** Tune your judge by comparing to known-good evaluations

**Steps:**

1. **Create calibration dataset:**
```python
calibration_data = [
    {"output": "...", "human_score": 4, "notes": "Clear but brief"},
    {"output": "...", "human_score": 5, "notes": "Excellent"},
    # ... 20-50 examples with human ratings
]
```

2. **Run judge on calibration set:**
```python
for item in calibration_data:
    judge_result = judge.evaluate(item['output'])
    item['judge_score'] = judge_result['average_score']
```

3. **Analyze agreement:**
```python
# Calculate correlation
correlation = pearson_correlation(
    [item['human_score'] for item in calibration_data],
    [item['judge_score'] for item in calibration_data]
)
# Good: correlation > 0.8
# Needs tuning: correlation < 0.6
```

4. **Tune rubric:**
- If judge is too harsh, adjust criteria descriptions
- If judge misses key aspects, add criteria
- If judge is inconsistent, simplify rubric

**Use when:** You need high accuracy, you have human ratings available

### Meta-Evaluation (Evaluating the Evaluator)

**Concept:** How do you know if your judge is good?

**Metrics:**

**1. Inter-Judge Agreement**
- Run same evaluation with multiple judges
- High agreement = reliable judge
- Low agreement = judge is arbitrary or rubric is unclear

**2. Correlation with Human Judgment**
- Compare judge scores to human ratings
- High correlation = judge aligns with human values
- Low correlation = judge is measuring wrong things

**3. Bias Detection**
- Position bias: Shuffle order, check if scores change
- Length bias: Test with identical content at different lengths
- Consistency: Run same evaluation multiple times, check variance

**4. Discriminative Power**
- Can judge distinguish between quality levels?
- Test with obviously good vs obviously bad examples
- Good judge: clear score separation
- Bad judge: similar scores for everything

### Self-Improving Judges

**Concept:** Judges that learn from feedback

**Approach 1: Prompt Refinement**
```python
# Start with basic rubric
rubric_v1 = {...}

# Collect feedback
feedback = [
    {"output": "...", "judge_score": 4, "user_rating": 2, "issue": "Too lenient"},
    {"output": "...", "judge_score": 3, "user_rating": 5, "issue": "Missed creativity"}
]

# Use LLM to refine rubric
improvement_prompt = f"""
Current rubric: {rubric_v1}

Feedback showing judge is not aligned with users:
{feedback}

Suggest improvements to the rubric to better match user expectations.
"""

rubric_v2 = llm(improvement_prompt)  # Updated rubric
```

**Approach 2: Example Library**
```python
# Build library of examples with scores
examples = {
    "excellent": [output1, output2],
    "good": [output3, output4],
    "poor": [output5, output6]
}

# Include examples in judge prompt
prompt = f"""
Here are examples of different quality levels:
Excellent (5/5): {examples['excellent'][0]}
Good (3/5): {examples['good'][0]}
Poor (1/5): {examples['poor'][0]}

Now evaluate this output:
{output_to_judge}
"""
```

**Use when:** You have user feedback, judge needs to adapt to changing standards

---

## Evaluation Output Structure

A good judge returns structured output that's useful for analysis.

### Minimum Viable Output

```python
{
    "scores": {
        "Clarity": 4,
        "Accuracy": 5,
        "Engagement": 3
    },
    "average_score": 4.0
}
```

### Production-Ready Output

```python
{
    "scores": {
        "Clarity": 4,
        "Accuracy": 5,
        "Engagement": 3,
        "Structure": 4
    },
    "reasoning": {
        "Clarity": "Writing is clear with good examples. Minor jargon could be explained.",
        "Accuracy": "All technical claims are correct and well-supported.",
        "Engagement": "Solid but could use more compelling hooks.",
        "Structure": "Good flow, clear intro and conclusion."
    },
    "average_score": 4.0,
    "overall_assessment": "High-quality content with strong accuracy. Could improve engagement with more dynamic examples.",
    "metadata": {
        "rubric": "Content Quality Rubric v1.0",
        "model": "gpt-4o-mini",
        "timestamp": "2025-12-22T10:30:00",
        "tokens_used": 450,
        "evaluation_time_seconds": 2.3
    }
}
```

### Why Structured Output Matters

**1. Actionable Feedback**
- Scores tell you what's wrong
- Reasoning tells you how to fix it

**2. Trend Analysis**
```python
# Track improvement over time
evaluations = load_all_evaluations()
clarity_scores = [e['scores']['Clarity'] for e in evaluations]
# Plot trend: Are we getting better?
```

**3. Debugging**
```python
# Find outputs that scored low on specific criteria
low_clarity = [e for e in evaluations if e['scores']['Clarity'] < 3]
# Analyze patterns in failures
```

**4. Comparison**
```python
# Compare two agents
agent_a_avg = mean([e['average_score'] for e in agent_a_evaluations])
agent_b_avg = mean([e['average_score'] for e in agent_b_evaluations])
# Which agent is better?
```

---

## Logging and Analysis

Evaluation data is only useful if you can analyze it.

### Logging Format: JSONL

**Why JSONL?** (JSON Lines)
- One evaluation per line
- Easy to append new evaluations
- Easy to parse and analyze

```jsonl
{"type": "single_evaluation", "output": "...", "result": {...}, "timestamp": "2025-12-22T10:00:00"}
{"type": "single_evaluation", "output": "...", "result": {...}, "timestamp": "2025-12-22T10:05:00"}
{"type": "comparison", "outputs": [...], "result": {...}, "timestamp": "2025-12-22T10:10:00"}
```

### Basic Analysis

```python
import json

# Load all evaluations
evaluations = []
with open('logs/evaluations.jsonl', 'r') as f:
    for line in f:
        evaluations.append(json.loads(line))

# Average score over time
avg_scores = [e['result']['average_score'] for e in evaluations]
print(f"Mean score: {sum(avg_scores) / len(avg_scores):.2f}")

# Score distribution
from collections import Counter
score_dist = Counter(avg_scores)
print(f"Distribution: {score_dist}")

# Criteria breakdown
clarity_scores = [e['result']['scores']['Clarity'] for e in evaluations]
print(f"Clarity average: {sum(clarity_scores) / len(clarity_scores):.2f}")
```

### Advanced Analysis: Identifying Patterns

```python
# Find systematic weaknesses
low_engagement = [e for e in evaluations if e['result']['scores']['Engagement'] < 3]
print(f"Low engagement: {len(low_engagement)} / {len(evaluations)}")

# Correlation between criteria
import numpy as np
clarity = [e['result']['scores']['Clarity'] for e in evaluations]
engagement = [e['result']['scores']['Engagement'] for e in evaluations]
correlation = np.corrcoef(clarity, engagement)[0, 1]
print(f"Clarity-Engagement correlation: {correlation:.2f}")
# High correlation: improving one improves the other
```

---

## When to Use LLM-as-Judge vs Traditional Metrics

Not every evaluation needs an LLM. Sometimes simple metrics are better.

| Task | LLM Judge | Traditional Metric |
|------|-----------|-------------------|
| Word count | ❌ LLMs can't count | ✅ `len(text.split())` |
| Grammar check | ❌ Use LanguageTool | ✅ `language_tool.check(text)` |
| Factual accuracy | ❌ LLMs hallucinate | ✅ Verify against sources |
| Code correctness | ⚠️ Maybe, but test better | ✅ `pytest test_suite.py` |
| Writing clarity | ✅ LLMs excel at this | ❌ Hard to quantify |
| Tone/empathy | ✅ LLMs excel at this | ❌ Hard to quantify |
| Engagement | ✅ LLMs can judge this | ⚠️ User click-through rate (if available) |
| Code readability | ✅ LLMs can assess | ⚠️ Metrics like cyclomatic complexity (partial) |

**Rule of thumb:**
- **Objective, verifiable facts:** Traditional metrics
- **Subjective quality judgment:** LLM judge
- **Hybrid:** Use both (Python for facts, LLM for quality)

---

## Comparison: Judge vs Other Evaluation Approaches

### Judge vs Unit Tests

**Unit Tests:**
- Verify correctness (does code produce expected output?)
- Binary: pass or fail
- Fast, deterministic, free

**Judge:**
- Assess quality (is code well-written?)
- Nuanced: scores on multiple dimensions
- Slower, non-deterministic, costs money

**Use both:** Tests for correctness, judge for quality

### Judge vs User Feedback

**User Feedback:**
- Ground truth: actual user satisfaction
- Slow to collect
- Only available in production

**Judge:**
- Proxy for user satisfaction
- Fast: evaluate in development
- Available before deployment

**Use both:** Judge during development, validate with user feedback in production

### Judge vs Human Review

**Human Review:**
- Most accurate
- Expensive, slow
- Doesn't scale

**Judge:**
- Fast and scalable
- Cheaper
- Good enough for most cases

**Use both:** Judge for volume, human review for edge cases and calibration

---

## Key Takeaways

**1. Judge ≠ Critic**
- Critics are in-workflow (binary gates)
- Judges are standalone (measurement tools)

**2. Bias is real and unavoidable**
- Acknowledge it
- Measure it
- Mitigate it (panels, calibration, human feedback)
- Be transparent about limitations

**3. Rubrics are the foundation**
- Specific, measurable criteria
- 3-5 criteria sweet spot
- Aligned with what actually matters

**4. Hybrid evaluation is best**
- Python for precision (counting, validation)
- LLM for judgment (quality, nuance)

**5. Log everything for analysis**
- JSONL format
- Track scores over time
- Find patterns in strengths/weaknesses

**6. Start simple, add complexity when needed**
- Single judge, fixed rubric
- Add panels/calibration for high-stakes decisions
- Advanced patterns are powerful but costly

---

## Next Steps

1. Study the example rubrics in `SOLUTION/rubrics/`
2. Run `judge_agent.py` to see evaluation in action
3. Design your own rubric for your use case
4. Test for bias (shuffle orders, vary lengths)
5. Compare judge scores to your own judgment
6. Iterate on rubric until alignment is good

**Remember:** A good judge is useful, not perfect. Build judges that help you improve your agents, not judges that claim to be infallible.
