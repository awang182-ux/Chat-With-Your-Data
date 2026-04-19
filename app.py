"""Simple Flask backend for Chat with Your Data."""

from __future__ import annotations

import numpy as np
import os
import tempfile
from typing import Any

import pandas as pd
from flask import Flask, jsonify, render_template, request

from analysis_pipeline import run_analysis

app = Flask(__name__)


@app.after_request
def add_cors_headers(response: Any) -> Any:
    """Allow browsers to call the API from another origin (e.g. opening index.html as a file)."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


import numpy as np
import pandas as pd

import numpy as np
import pandas as pd
from typing import Any

def _to_json_safe(value: Any) -> Any:
    if isinstance(value, pd.DataFrame):
        return value.applymap(_to_json_safe).to_dict(orient="records")

    if isinstance(value, pd.Series):
        return {str(k): _to_json_safe(v) for k, v in value.to_dict().items()}

    if isinstance(value, dict):
        return {str(k): _to_json_safe(v) for k, v in value.items()}

    if isinstance(value, (list, tuple)):
        return [_to_json_safe(v) for v in value]

    if isinstance(value, np.generic):
        return value.item()

    return value


@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze() -> tuple[Any, int]:
    """
    Analyze a CSV file with a natural language question.

    Expected form-data:
    - question: text field
    - file: CSV file upload
    """
    if request.method == "OPTIONS":
        return jsonify({}), 204

    question = request.form.get("question", "").strip()
    uploaded_file = request.files.get("file")

    if not question:
        return jsonify({"success": False, "error": "Question cannot be empty."}), 400

    if uploaded_file is None or uploaded_file.filename == "":
        return (
            jsonify(
                {
                    "success": False,
                    "error": "CSV file is required (form field: file).",
                }
            ),
            400,
        )

    temp_csv_path = ""
    try:
        # Save uploaded file to a temporary CSV path.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            uploaded_file.save(temp_file.name)
            temp_csv_path = temp_file.name

        analysis_output = run_analysis(temp_csv_path, question)

        response_data = {
            "success": True,
            "question": analysis_output["question"],
            "prompt": analysis_output["prompt"],
            "generated_code": analysis_output["generated_code"],
            "final_result": _to_json_safe(analysis_output["final_result"]),
        }
        return jsonify(response_data), 200
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        return jsonify({"success": False, "error": str(error)}), 400
    except Exception as error:
        # Generic fallback so students can see failures clearly.
        return jsonify({"success": False, "error": f"Unexpected server error: {error}"}), 500
    finally:
        # Clean up temporary file after processing.
        if temp_csv_path and os.path.exists(temp_csv_path):
            os.remove(temp_csv_path)


@app.route("/health", methods=["GET"])
def health() -> tuple[Any, int]:
    """Simple health-check endpoint for frontend/backend connectivity tests."""
    return jsonify({"success": True, "status": "ok"}), 200


@app.route("/")
def index() -> str:
    """Home page: CSV upload and question form (templates + static files)."""
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
