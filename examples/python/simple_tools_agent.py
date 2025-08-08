from __future__ import annotations

import os

from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands_tools import calculator, current_time


@tool
def letter_counter(text: str) -> str:
    """Count letters in the given text.

    Args:
        text: The text to analyze
    """
    letters = [c for c in text if c.isalpha()]
    return f"Letters: {len(letters)}"


def main() -> None:
    model_tag = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    ollama_model = OllamaModel(host="http://localhost:11434", model_id=model_tag)

    agent = Agent(
        model=ollama_model,
        system_prompt=("You are a concise assistant. Use tools when helpful."),
        tools=[current_time, calculator, letter_counter],
    )

    print(agent("What time is it now, and what is 23*19? Also count letters in 'Hello, Strands!'"))


if __name__ == "__main__":
    main()
