"""Reusable analysis pipeline for Chat with Your Data backend."""

from __future__ import annotations

from typing import Any

from code_executor import execute_pandas_code
from data_loader import get_dataframe_summary, load_csv
from llm_client import generate_pandas_code
from prompt_builder import build_prompt


def run_analysis(csv_file: str, question: str) -> dict[str, Any]:
    """
    Run the full CSV -> LLM code -> execution pipeline.

    This function is designed to be reusable in backend frameworks
    like Flask or FastAPI.

    Args:
        csv_file: Path to the CSV file.
        question: User's natural language question.

    Returns:
        A structured dictionary with question, prompt, generated code,
        and final result.

    Raises:
        ValueError: If question is empty or other validation fails.
        FileNotFoundError: If CSV file does not exist.
        RuntimeError: If LLM call or code execution fails.
    """
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")

    # 1) Load CSV and build DataFrame summary.
    df = load_csv(csv_file)
    summary = get_dataframe_summary(df)

    # 2) Build prompt from question and summary.
    prompt = build_prompt(question, summary)

    # 3) Ask the LLM to generate pandas code.
    generated_code = generate_pandas_code(prompt)

    # 4) Execute generated code and collect final result.
    final_result = execute_pandas_code(df, generated_code)

    return {
        "question": question,
        "prompt": prompt,
        "generated_code": generated_code,
        "final_result": final_result,
    }
