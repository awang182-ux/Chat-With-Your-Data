"""Simple end-to-end test pipeline for the Chat with Your Data project."""

from __future__ import annotations

from analysis_pipeline import run_analysis


def main() -> None:
    """Run a real end-to-end pipeline test with an LLM call."""
    csv_file = "sample.csv"

    # Let the user type a question in the terminal.
    question = input("Enter your question: ").strip()
    if not question:
        print("Question cannot be empty.")
        return

    try:
        # Run the reusable backend pipeline function.
        analysis_output = run_analysis(csv_file, question)

        print("=" * 60)
        print("Question:")
        print(analysis_output["question"])

        # 3) Print the generated prompt.
        print("\nGenerated Prompt:")
        print(analysis_output["prompt"])

        # 5) Print the generated code from the model.
        print("\nGenerated Code:")
        print(analysis_output["generated_code"])

        # 6) Print final result from executed code.
        print("\nFinal Result:")
        print(analysis_output["final_result"])
        print("=" * 60)
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        # Keep error handling simple and beginner-friendly.
        print(f"Pipeline error: {error}")


if __name__ == "__main__":
    # Run with: python test_pipeline.py
    main()
