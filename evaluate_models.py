import os
import json
from analysis_pipeline import run_analysis

MODELS = [
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "google/gemma-4-26b-a4b-it:free",
    "openai/gpt-oss-120b:free",
    "meta-llama/llama-3.2-3b-instruct:free",
]

TEST_CASES = [
    {
        "dataset": "sales_data",
        "csv_file": "sample_data/sales_data.csv",
        "question": "Which Region has the highest total Sales?",
    },
    {
        "dataset": "sales_data",
        "csv_file": "sample_data/sales_data.csv",
        "question": "What is the total Profit by Category?",
    },
    {
        "dataset": "student_data",
        "csv_file": "sample_data/student_data.csv",
        "question": "What is the average GPA by Major?",
    },
    {
        "dataset": "student_data",
        "csv_file": "sample_data/student_data.csv",
        "question": "Rank student GPA from highest to lowest",
    },
    {
        "dataset": "orders_data",
        "csv_file": "sample_data/orders_data.csv",
        "question": "What is the total Amount by Customer?",
    },
    {
        "dataset": "orders_data",
        "csv_file": "sample_data/orders_data.csv",
        "question": "Which Customer spent the most?",
    },
]

results = []

for case in TEST_CASES:
    print(f"\nTesting dataset: {case['dataset']}")
    for model in MODELS:
        print(f"  Running model: {model}")
        os.environ["MODEL_NAME"] = model

        try:
            output = run_analysis(case["csv_file"], case["question"])
            results.append({
                "dataset": case["dataset"],
                "question": case["question"],
                "model": model,
                "success": True,
                "final_result": str(output["final_result"]),
                "generated_code": output["generated_code"],
            })
        except Exception as e:
            results.append({
                "dataset": case["dataset"],
                "question": case["question"],
                "model": model,
                "success": False,
                "error": str(e),
            })

with open("model_eval_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nDone. Results saved to model_eval_results.json")
