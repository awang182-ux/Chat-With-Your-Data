"""Simple OpenAI-compatible client for generating pandas code."""

from __future__ import annotations

import os

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


def generate_pandas_code(prompt: str) -> str:
    """
    Send a prompt to an OpenAI-compatible chat completion API.

    Configuration is read from environment variables:
    - API_KEY (required)
    - BASE_URL (optional, default: https://openrouter.ai/api/v1)
    - MODEL_NAME (optional, default: openrouter/free)

    Args:
        prompt: The prepared instruction prompt for the LLM.

    Returns:
        The model's text content (expected Python code).

    Raises:
        ValueError: If required configuration is missing or response is empty.
        RuntimeError: If the API call fails.
    """
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL", "https://openrouter.ai/api/v1")
    model_name = os.getenv("MODEL_NAME", "openrouter/free")

    # API key is required for calling OpenRouter.
    if not api_key:
        raise ValueError("Missing API_KEY environment variable.")

    client = OpenAI(api_key=api_key, base_url=base_url)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You generate pandas Python code only. Return plain Python objects only. Do not use f-strings, .format(), or string interpolation."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
    except Exception as error:
        raise RuntimeError(f"Failed to call LLM API: {error}") from error

    content = response.choices[0].message.content if response.choices else None
    if not content:
        raise ValueError("The model returned an empty response.")

    return content.strip()


if __name__ == "__main__":
    # Quick local test:
    # 1) Install dependency: pip install openai
    # 2) Export env vars:
    #    export API_KEY="your_openrouter_key"
    #    export BASE_URL="https://openrouter.ai/api/v1"   # optional
    #    export MODEL_NAME="openrouter/free"              # optional
    # 3) Run: python llm_client.py
    sample_prompt = (
        "Use pandas with DataFrame df to find the average Age by City. "
        "Store final output in variable result. Output code only."
    )

    try:
        code = generate_pandas_code(sample_prompt)
        print("Generated code:\n")
        print(code)
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")

