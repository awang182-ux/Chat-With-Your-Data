"""Build prompts for LLM-based pandas data analysis."""

from __future__ import annotations

from typing import Any


def build_prompt(question: str, summary: dict[str, Any]) -> str:
    """
    Create a prompt that guides an LLM to generate safe pandas code.

    The generated code is expected to use an existing DataFrame named `df`,
    answer the user's question, and store the final output in `result`.

    Args:
        question: User's natural language data question.
        summary: DataFrame summary dictionary (from data_loader module).

    Returns:
        A formatted prompt string for the LLM.
    """
    # Pull only the summary fields we need. Use defaults so the function
    # remains robust even if some keys are missing.
    columns = summary.get("columns", [])
    dtypes = summary.get("dtypes", {})
    preview = summary.get("preview", [])

    prompt = f"""
You are a data analysis assistant.

You already have a pandas DataFrame named df.

DataFrame information:
- columns: {columns}
- dtypes: {dtypes}
- preview rows: {preview}

User question:
{question}

Instructions:
1. Write executable Python code using pandas to answer the question.
2. Use only the existing DataFrame variable: df.
3. Store the final answer in a variable named result.
4. Output only Python code.
5. Do not include explanations, markdown, or comments in the output code.
6. Avoid unsafe operations (no file writes, no system commands, no network calls, no eval/exec).
7. Return plain Python objects only: dict, list, number, or string.
8. For grouped answers, return a pandas Series or dict with the group labels preserved.
9. Do not use f-strings, .format(), or any string interpolation.
10. Do not return raw arrays, .values, or unlabeled lists.
11. When the user asks to rank, sort, group, or compare values, inspect the column names, dtypes, and preview rows to choose the most relevant categorical and numeric columns.
12. If multiple columns could fit, choose the most likely one based on the question.
13. Preserve labels in the output when ranking or grouping.
"""
    # strip() removes the leading/trailing blank line from the triple-quoted string.
    return prompt.strip()


if __name__ == "__main__":
    # Quick local test:
    # Run: python prompt_builder.py
    sample_summary = {
        "columns": ["Name", "Age", "City"],
        "dtypes": {"Name": "object", "Age": "float64", "City": "object"},
        "preview": [
            {"Name": "Alice", "Age": 25, "City": "New York"},
            {"Name": "Bob", "Age": None, "City": "Los Angeles"},
            {"Name": "Carol", "Age": 30, "City": "Chicago"},
        ],
    }

    sample_question = "What is the average age by city?"
    built_prompt = build_prompt(sample_question, sample_summary)

    print("Generated prompt:\n")
    print(built_prompt)
