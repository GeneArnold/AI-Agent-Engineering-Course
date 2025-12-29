#!/usr/bin/env python3
"""
Module 5: LLM as Judge & Evaluation
====================================

A judge agent that evaluates outputs against configurable rubrics.

Key Concepts:
- Judge vs Critic: Judge is standalone evaluator, Critic is in-workflow QC
- Multi-criteria evaluation: Score across multiple dimensions
- Comparison mode: Rank multiple outputs
- Bias awareness: Understanding and mitigating evaluation biases

Usage:
    python judge_agent.py
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Configuration
MODEL = "gpt-4o-mini"
MAX_TOKENS = 2000
TEMPERATURE = 0.3  # Lower temperature for more consistent evaluation

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class JudgeAgent:
    """
    LLM-as-Judge evaluator that scores outputs against rubrics.

    This is NOT a Critic (which is part of a workflow). This is a standalone
    evaluator that measures quality for analysis and improvement.

    Think: Product reviewer (Judge) vs Factory QC (Critic)
    """

    def __init__(self, rubric_path: Optional[str] = None):
        """
        Initialize judge with optional rubric.

        Args:
            rubric_path: Path to JSON rubric file
        """
        self.rubric = None
        if rubric_path:
            self.load_rubric(rubric_path)

    def load_rubric(self, rubric_path: str) -> None:
        """Load evaluation rubric from JSON file."""
        with open(rubric_path, 'r') as f:
            self.rubric = json.load(f)
        print(f"✅ Loaded rubric: {self.rubric.get('name', 'Unknown')}")

    def evaluate(self,
                 output: str,
                 context: Optional[str] = None,
                 log_results: bool = True) -> Dict[str, Any]:
        """
        Evaluate a single output against the rubric.

        Args:
            output: The text/content to evaluate
            context: Optional context (e.g., original task, requirements)
            log_results: Whether to log evaluation to file

        Returns:
            Dictionary with scores, reasoning, and metadata
        """
        if not self.rubric:
            raise ValueError("No rubric loaded. Use load_rubric() first.")

        # Build evaluation prompt
        prompt = self._build_evaluation_prompt(output, context)

        # Get LLM evaluation
        start_time = time.time()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert evaluator. Provide objective, detailed assessments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        evaluation_time = time.time() - start_time
        raw_response = response.choices[0].message.content

        # Parse structured output
        result = self._parse_evaluation(raw_response, evaluation_time)

        # Add metadata
        result['metadata'] = {
            'rubric': self.rubric['name'],
            'model': MODEL,
            'timestamp': datetime.now().isoformat(),
            'evaluation_time_seconds': round(evaluation_time, 2),
            'tokens_used': response.usage.total_tokens
        }

        # Log if requested
        if log_results:
            self._log_evaluation(output, context, result)

        return result

    def compare(self,
                outputs: List[str],
                labels: Optional[List[str]] = None,
                context: Optional[str] = None,
                log_results: bool = True) -> Dict[str, Any]:
        """
        Compare multiple outputs and rank them.

        This is comparison mode - evaluates outputs relative to each other.

        Args:
            outputs: List of outputs to compare (2-5 recommended)
            labels: Optional labels for each output (e.g., ["Agent A", "Agent B"])
            context: Optional context about the task
            log_results: Whether to log comparison results

        Returns:
            Dictionary with rankings, scores, and reasoning
        """
        if not self.rubric:
            raise ValueError("No rubric loaded. Use load_rubric() first.")

        if len(outputs) < 2:
            raise ValueError("Need at least 2 outputs to compare")

        # Default labels if not provided
        if not labels:
            labels = [f"Output {i+1}" for i in range(len(outputs))]

        # Build comparison prompt
        prompt = self._build_comparison_prompt(outputs, labels, context)

        # Get LLM comparison
        start_time = time.time()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert evaluator. Compare outputs objectively and explain your rankings."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        evaluation_time = time.time() - start_time
        raw_response = response.choices[0].message.content

        # Parse comparison results
        result = self._parse_comparison(raw_response, labels, evaluation_time)

        # Add metadata
        result['metadata'] = {
            'rubric': self.rubric['name'],
            'model': MODEL,
            'timestamp': datetime.now().isoformat(),
            'evaluation_time_seconds': round(evaluation_time, 2),
            'tokens_used': response.usage.total_tokens,
            'num_outputs_compared': len(outputs)
        }

        # Log if requested
        if log_results:
            self._log_comparison(outputs, labels, context, result)

        return result

    def _build_evaluation_prompt(self, output: str, context: Optional[str]) -> str:
        """Build prompt for single output evaluation."""
        prompt_parts = [
            f"# Evaluation Task",
            f"\nRubric: {self.rubric['name']}",
            f"Description: {self.rubric['description']}\n"
        ]

        # Add context if provided
        if context:
            prompt_parts.append(f"## Context\n{context}\n")

        # Add output to evaluate
        prompt_parts.append(f"## Output to Evaluate\n{output}\n")

        # Add evaluation criteria
        prompt_parts.append("## Evaluation Criteria\n")
        for criterion in self.rubric['criteria']:
            scale = self.rubric['scale']
            prompt_parts.append(
                f"\n**{criterion['name']}** ({scale['min']}-{scale['max']} scale: {scale['type']})"
            )
            prompt_parts.append(f"Definition: {criterion['description']}")
            if 'indicators' in criterion:
                prompt_parts.append("Good indicators:")
                for indicator in criterion['indicators']:
                    prompt_parts.append(f"  - {indicator}")

        # Add output format instructions
        prompt_parts.append("\n## Output Format")
        prompt_parts.append("Provide your evaluation in this format:\n")
        prompt_parts.append("SCORES:")
        for criterion in self.rubric['criteria']:
            prompt_parts.append(f"{criterion['name']}: [score]")
        prompt_parts.append("\nREASONING:")
        for criterion in self.rubric['criteria']:
            prompt_parts.append(f"{criterion['name']}: [detailed explanation]")
        prompt_parts.append("\nOVERALL ASSESSMENT:")
        prompt_parts.append("[Summary of strengths and weaknesses]")

        return "\n".join(prompt_parts)

    def _build_comparison_prompt(self, outputs: List[str], labels: List[str], context: Optional[str]) -> str:
        """Build prompt for comparing multiple outputs."""
        prompt_parts = [
            f"# Comparison Task",
            f"\nRubric: {self.rubric['name']}",
            f"Description: {self.rubric['description']}\n"
        ]

        # Add context if provided
        if context:
            prompt_parts.append(f"## Context\n{context}\n")

        # Add outputs to compare
        prompt_parts.append("## Outputs to Compare\n")
        for label, output in zip(labels, outputs):
            prompt_parts.append(f"### {label}")
            prompt_parts.append(output)
            prompt_parts.append("")

        # Add evaluation criteria
        prompt_parts.append("## Evaluation Criteria\n")
        for criterion in self.rubric['criteria']:
            prompt_parts.append(f"\n**{criterion['name']}**")
            prompt_parts.append(f"{criterion['description']}")

        # Add output format instructions
        prompt_parts.append("\n## Output Format")
        prompt_parts.append("Compare the outputs and provide:\n")
        prompt_parts.append("RANKING:")
        prompt_parts.append("1st place: [label]")
        prompt_parts.append("2nd place: [label]")
        prompt_parts.append("(etc.)\n")
        prompt_parts.append("CRITERION ANALYSIS:")
        for criterion in self.rubric['criteria']:
            prompt_parts.append(f"\n{criterion['name']}:")
            prompt_parts.append("[Compare how each output performs on this criterion]")
        prompt_parts.append("\nOVERALL REASONING:")
        prompt_parts.append("[Explain your ranking decisions]")

        return "\n".join(prompt_parts)

    def _parse_evaluation(self, response: str, eval_time: float) -> Dict[str, Any]:
        """Parse LLM response into structured evaluation results."""
        # This is simplified parsing - production version would be more robust
        result = {
            'scores': {},
            'reasoning': {},
            'overall_assessment': '',
            'raw_response': response
        }

        # Extract scores
        if 'SCORES:' in response:
            scores_section = response.split('SCORES:')[1].split('REASONING:')[0]
            for criterion in self.rubric['criteria']:
                name = criterion['name']
                # Look for pattern like "Criterion: 4" or "Criterion: 4/5"
                for line in scores_section.split('\n'):
                    if name in line and ':' in line:
                        try:
                            score_part = line.split(':')[1].strip()
                            # Extract number (handle "4/5" or "4" format)
                            score = int(score_part.split('/')[0].strip())
                            result['scores'][name] = score
                        except (ValueError, IndexError):
                            pass

        # Extract reasoning
        if 'REASONING:' in response:
            reasoning_section = response.split('REASONING:')[1].split('OVERALL ASSESSMENT:')[0]
            for criterion in self.rubric['criteria']:
                name = criterion['name']
                # Look for criterion name and capture explanation
                for i, line in enumerate(reasoning_section.split('\n')):
                    if name in line and ':' in line:
                        explanation = line.split(':', 1)[1].strip()
                        # Capture multi-line explanations
                        j = i + 1
                        lines = reasoning_section.split('\n')
                        while j < len(lines) and not any(c['name'] in lines[j] for c in self.rubric['criteria']):
                            if lines[j].strip():
                                explanation += ' ' + lines[j].strip()
                            j += 1
                        result['reasoning'][name] = explanation

        # Extract overall assessment
        if 'OVERALL ASSESSMENT:' in response:
            result['overall_assessment'] = response.split('OVERALL ASSESSMENT:')[1].strip()

        # Calculate average score
        if result['scores']:
            result['average_score'] = round(sum(result['scores'].values()) / len(result['scores']), 2)

        return result

    def _parse_comparison(self, response: str, labels: List[str], eval_time: float) -> Dict[str, Any]:
        """Parse LLM comparison response into structured results."""
        result = {
            'ranking': [],
            'criterion_analysis': {},
            'overall_reasoning': '',
            'raw_response': response
        }

        # Extract ranking
        if 'RANKING:' in response:
            ranking_section = response.split('RANKING:')[1].split('CRITERION ANALYSIS:')[0]
            # Look for "1st place:", "2nd place:", etc.
            for line in ranking_section.split('\n'):
                if 'place:' in line.lower():
                    for label in labels:
                        if label in line:
                            result['ranking'].append(label)
                            break

        # Extract criterion analysis
        if 'CRITERION ANALYSIS:' in response:
            analysis_section = response.split('CRITERION ANALYSIS:')[1].split('OVERALL REASONING:')[0]
            for criterion in self.rubric['criteria']:
                name = criterion['name']
                for i, line in enumerate(analysis_section.split('\n')):
                    if name in line and ':' in line:
                        analysis = line.split(':', 1)[1].strip()
                        # Capture multi-line analysis
                        j = i + 1
                        lines = analysis_section.split('\n')
                        while j < len(lines) and not any(c['name'] in lines[j] for c in self.rubric['criteria']):
                            if lines[j].strip():
                                analysis += ' ' + lines[j].strip()
                            j += 1
                        result['criterion_analysis'][name] = analysis

        # Extract overall reasoning
        if 'OVERALL REASONING:' in response:
            result['overall_reasoning'] = response.split('OVERALL REASONING:')[1].strip()

        return result

    def _log_evaluation(self, output: str, context: Optional[str], result: Dict[str, Any]) -> None:
        """Log evaluation results to JSONL file."""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "evaluations.jsonl"

        log_entry = {
            'type': 'single_evaluation',
            'output': output[:500],  # Truncate for logging
            'context': context,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }

        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def _log_comparison(self, outputs: List[str], labels: List[str], context: Optional[str], result: Dict[str, Any]) -> None:
        """Log comparison results to JSONL file."""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "comparisons.jsonl"

        log_entry = {
            'type': 'comparison',
            'outputs': [o[:200] for o in outputs],  # Truncate for logging
            'labels': labels,
            'context': context,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }

        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


def print_evaluation_results(result: Dict[str, Any]) -> None:
    """Pretty print evaluation results."""
    print("\n" + "="*60)
    print("📊 EVALUATION RESULTS")
    print("="*60)

    # Print scores
    if result.get('scores'):
        print("\n🎯 SCORES:")
        for criterion, score in result['scores'].items():
            print(f"  {criterion}: {score}")
        if 'average_score' in result:
            print(f"\n  Average: {result['average_score']}")

    # Print reasoning
    if result.get('reasoning'):
        print("\n💭 REASONING:")
        for criterion, explanation in result['reasoning'].items():
            print(f"\n  {criterion}:")
            print(f"    {explanation}")

    # Print overall assessment
    if result.get('overall_assessment'):
        print("\n📝 OVERALL ASSESSMENT:")
        print(f"  {result['overall_assessment']}")

    # Print metadata
    if result.get('metadata'):
        meta = result['metadata']
        print(f"\n⚙️  Metadata: {meta['model']}, {meta['tokens_used']} tokens, {meta['evaluation_time_seconds']}s")

    print("="*60 + "\n")


def print_comparison_results(result: Dict[str, Any]) -> None:
    """Pretty print comparison results."""
    print("\n" + "="*60)
    print("🏆 COMPARISON RESULTS")
    print("="*60)

    # Print ranking
    if result.get('ranking'):
        print("\n🥇 RANKING:")
        for i, label in enumerate(result['ranking'], 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
            print(f"  {medal} {label}")

    # Print criterion analysis
    if result.get('criterion_analysis'):
        print("\n📊 CRITERION ANALYSIS:")
        for criterion, analysis in result['criterion_analysis'].items():
            print(f"\n  {criterion}:")
            print(f"    {analysis}")

    # Print overall reasoning
    if result.get('overall_reasoning'):
        print("\n💭 OVERALL REASONING:")
        print(f"  {result['overall_reasoning']}")

    # Print metadata
    if result.get('metadata'):
        meta = result['metadata']
        print(f"\n⚙️  Metadata: {meta['model']}, {meta['tokens_used']} tokens, {meta['evaluation_time_seconds']}s")

    print("="*60 + "\n")


# ============================================================================
# DEMO: Example usage
# ============================================================================

def demo_single_evaluation():
    """Demo: Evaluate a single blog post."""
    print("\n" + "="*60)
    print("DEMO 1: Single Output Evaluation")
    print("="*60)

    # Load content quality rubric
    judge = JudgeAgent(rubric_path="rubrics/content_quality.json")

    # Sample blog post to evaluate
    blog_post = """
    Understanding Multi-Agent Systems in AI

    Multi-agent systems represent a powerful architectural pattern in AI engineering.
    Rather than relying on a single agent to handle complex tasks, we can design
    systems where multiple specialized agents collaborate.

    For example, a Planner agent breaks tasks into steps, a Worker agent executes
    those steps, and a Critic agent reviews the quality. This separation of concerns
    leads to more robust and maintainable systems.

    The key insight is that orchestration doesn't need to be done by an LLM - we can
    use deterministic Python rules to coordinate agents, which is more reliable and
    cost-effective than LLM-based orchestration.
    """

    context = "Target: 300-word educational blog post about multi-agent systems"

    # Evaluate
    result = judge.evaluate(blog_post, context=context, log_results=False)
    print_evaluation_results(result)


def demo_comparison():
    """Demo: Compare multiple agent outputs."""
    print("\n" + "="*60)
    print("DEMO 2: Comparison Mode")
    print("="*60)

    # Load code quality rubric
    judge = JudgeAgent(rubric_path="rubrics/code_quality.json")

    # Sample code implementations to compare
    implementation_a = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
"""

    implementation_b = """
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
"""

    implementation_c = """
def calculate_average(numbers):
    \"\"\"Calculate the average of a list of numbers.

    Args:
        numbers: List of numeric values

    Returns:
        float: The arithmetic mean

    Raises:
        ValueError: If list is empty
    \"\"\"
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
"""

    outputs = [implementation_a, implementation_b, implementation_c]
    labels = ["Implementation A", "Implementation B", "Implementation C"]
    context = "Task: Write a function to calculate the average of a list of numbers"

    # Compare
    result = judge.compare(outputs, labels=labels, context=context, log_results=False)
    print_comparison_results(result)


if __name__ == "__main__":
    print("\n" + "🔍 Module 5: LLM as Judge & Evaluation".center(60))
    print("="*60)

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your API key in .env file")
        exit(1)

    # Run demos
    demo_single_evaluation()
    demo_comparison()

    print("\n✅ All demos completed!")
    print("📁 Check logs/ directory for evaluation history (if logging enabled)")
