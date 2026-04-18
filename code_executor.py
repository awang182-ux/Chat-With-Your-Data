"""Utilities for cleaning, validating, and executing generated pandas code."""

from __future__ import annotations

import ast
import re
from typing import Any

import pandas as pd


def clean_generated_code(code_text: str) -> str:
    """
    Remove markdown code fences and extra whitespace from generated code.

    Args:
        code_text: Raw code text (possibly with markdown fences).

    Returns:
        Clean executable Python code as a string.
    """
    cleaned = code_text.strip()

    # Remove opening markdown fences like ```python or ```py or ``` (case-insensitive).
    cleaned = re.sub(r"^```(?:python|py)?\s*", "", cleaned, flags=re.IGNORECASE)
    # Remove trailing markdown fence.
    cleaned = re.sub(r"\s*```$", "", cleaned)

    return cleaned.strip()


import ast
import re
from typing import Any

def validate_code_safety(code_text: str) -> None:
    blocked_patterns = [
        "import os",
        "from os",
        "import sys",
        "from sys",
        "open(",
        "eval(",
        "exec(",
        "subprocess",
        "requests",
        "__import__",
        ".format(",
    ]

    lowered = code_text.lower()
    for pattern in blocked_patterns:
        if pattern.lower() in lowered:
            raise ValueError(f"Unsafe code detected. Blocked pattern: {pattern}")

    try:
        tree = ast.parse(code_text)
    except SyntaxError as error:
        raise ValueError(f"Generated code is invalid Python: {error}") from error

    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            raise ValueError("Unsafe code detected. F-strings are not allowed.")
        
def execute_pandas_code(df: Any, code_text: str):
    """
    Clean, validate, and execute generated pandas code safely.

    The executed code must write the final output into a variable named `result`.

    Args:
        df: Existing pandas DataFrame object.
        code_text: Generated Python code string.

    Returns:
        The value stored in `result`.

    Raises:
        ValueError: For unsafe code or missing result.
        RuntimeError: If execution fails.
    """
    cleaned_code = clean_generated_code(code_text)
    if not cleaned_code:
        raise ValueError("Generated code is empty after cleaning.")

    validate_code_safety(cleaned_code)

    # Use one shared environment for both globals and locals.
    # This helps lambda/nested scopes resolve names like df and pd correctly.
    execution_env = {
        "__builtins__": {"len": len, "sum": sum, "min": min, "max": max},
        "df": df,
        "pd": pd,
    }

    try:
        exec(cleaned_code, execution_env, execution_env)
    except Exception as error:
        raise RuntimeError(f"Code execution failed: {error}") from error

    if "result" not in execution_env:
        raise ValueError("Execution finished, but `result` was never created.")

    return normalize_result(execution_env["result"])

import numpy as np
import pandas as pd

def normalize_result(result):
    if isinstance(result, pd.Series):
        return result.to_dict()
    if isinstance(result, pd.DataFrame):
        return result.to_dict(orient="records")
    if isinstance(result, np.generic):
        return result.item()
    return result

if __name__ == "__main__":
    # Quick local test:
    # Run: python code_executor.py
    import pandas as pd

    sample_df = pd.DataFrame(
        {
            "City": ["New York", "Los Angeles", "Chicago", "Chicago"],
            "Age": [25, 30, 35, 40],
        }
    )

    sample_code = """
```python
result = df.groupby("City")["Age"].mean()
```
"""

    try:
        output = execute_pandas_code(sample_df, sample_code)
        print("Execution result:")
        print(output)
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")
