"""Utilities for loading CSV data and extracting a DataFrame summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def load_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame and clean column names.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A pandas DataFrame with cleaned column names.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be read as a valid CSV.
    """
    path = Path(file_path)

    # Check early so the error message is clearer for beginners.
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    try:
        dataframe = pd.read_csv(path)
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"The CSV file is empty: {path}") from error
    except pd.errors.ParserError as error:
        raise ValueError(f"The file is not a valid CSV format: {path}") from error
    except Exception as error:  # Catch other read errors (permissions, encoding, etc.)
        raise ValueError(f"Could not read CSV file: {path}") from error

    # Clean column names by removing leading/trailing spaces.
    dataframe.columns = dataframe.columns.str.strip()

    return dataframe


def get_dataframe_summary(dataframe: pd.DataFrame) -> dict[str, Any]:
    """
    Build a beginner-friendly summary of a DataFrame.

    Args:
        dataframe: The pandas DataFrame to summarize.

    Returns:
        A dictionary containing shape, columns, data types, preview rows,
        and missing values count.
    """
    summary = {
        "shape": dataframe.shape,
        "columns": dataframe.columns.tolist(),
        # Convert dtype objects to strings for clean and readable output.
        "dtypes": {column: str(dtype) for column, dtype in dataframe.dtypes.items()},
        # Convert preview rows to list-of-dicts so it is easy to print or JSON-serialize.
        "preview": dataframe.head(5).to_dict(orient="records"),
        "missing_values": dataframe.isnull().sum().to_dict(),
    }
    return summary


if __name__ == "__main__":
    # Quick local test:
    # 1) Put a sample CSV in the same folder, e.g. sample.csv
    # 2) Run: python data_loader.py
    sample_file = "sample.csv"

    try:
        df = load_csv(sample_file)
        info = get_dataframe_summary(df)

        print("DataFrame summary:")
        for key, value in info.items():
            print(f"\n{key}:")
            print(value)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
