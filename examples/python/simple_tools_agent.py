from __future__ import annotations

from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands_tools import current_time, calculator


@tool
def letter_counter(text: str) -> str:
    """Count letters in the given text.

    Args:
        text: The text to analyze
    """
    letters = [c for c in text if c.isalpha()]
    return f"Letters: {len(letters)}"


def main() -> None:
    ollama_model = OllamaModel(host="http://localhost:11434", model_id="llama3.2")

    agent = Agent(
        model=ollama_model,
        system_prompt=(
            "You are a concise assistant. Use tools when helpful."
        ),
        tools=[current_time, calculator, letter_counter],
    )

    print(agent("What time is it now, and what is 23*19? Also count letters in 'Hello, Strands!'"))


if __name__ == "__main__":
    main()

