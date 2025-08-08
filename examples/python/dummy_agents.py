from __future__ import annotations

import os

from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands_tools import calculator, current_time


# Custom toy tool
@tool
def echo_upper(text: str) -> str:
    """Return the text in UPPERCASE."""
    return text.upper()


def build_model() -> OllamaModel:
    model_tag = os.getenv("OLLAMA_MODEL", "qwen3:4b")
    return OllamaModel(host="http://localhost:11434", model_id=model_tag)


# a1: general assistant with a couple of tools
def build_a1(model: OllamaModel) -> Agent:
    return Agent(
        model=model,
        system_prompt="You are a helpful general assistant. Be concise.",
        tools=[current_time, echo_upper],
    )


# a2: math specialist using calculator tool
def build_a2(model: OllamaModel) -> Agent:
    return Agent(
        model=model,
        system_prompt="You are a math expert. Show brief steps.",
        tools=[calculator],
    )


# Tool wrappers to delegate to a1 and a2 (for a3 orchestrator)
def build_delegate_tools(a1: Agent, a2: Agent):
    @tool
    def ask_a1(query: str) -> str:
        """Delegate general questions to agent a1."""
        return str(a1(query))

    @tool
    def ask_a2(query: str) -> str:
        """Delegate math problems to agent a2."""
        return str(a2(query))

    return ask_a1, ask_a2


# a3: simple orchestrator that routes via tools
def build_a3(model: OllamaModel, ask_a1, ask_a2) -> Agent:
    return Agent(
        model=model,
        system_prompt=(
            "You are an orchestrator. Use ask_a2 for calculations. Use ask_a1 for everything else."
        ),
        tools=[ask_a1, ask_a2],
    )


def main() -> None:
    model = build_model()

    a1 = build_a1(model)
    a2 = build_a2(model)
    ask_a1, ask_a2 = build_delegate_tools(a1, a2)
    a3 = build_a3(model, ask_a1, ask_a2)

    print("=== a1: general assistant with tools ===")
    print(a1("What time is it now? Also echo 'hello agents' in uppercase."))

    print("\n=== a2: math specialist (calculator tool) ===")
    print(a2("Compute 57 * 89 and show brief steps."))

    print("\n=== a3: orchestrator (delegates to a1/a2 tools) ===")
    print(a3("Find the derivative of x^3 and evaluate at x=3. Then greet me."))


if __name__ == "__main__":
    main()
