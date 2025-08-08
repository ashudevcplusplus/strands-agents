from __future__ import annotations

from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands_tools import http_request, calculator


RESEARCH_PROMPT = (
    "You are a research assistant. Cite sources and be factual. Use http_request when needed."
)
MATH_PROMPT = "You are a math expert. Show steps briefly."

ollama_model = OllamaModel(host="http://localhost:11434", model_id="llama3.2")

research_agent = Agent(model=ollama_model, system_prompt=RESEARCH_PROMPT, tools=[http_request])
math_agent = Agent(model=ollama_model, system_prompt=MATH_PROMPT, tools=[calculator])


@tool
def research_tool(query: str) -> str:
    """Delegate research questions to the research agent."""
    return str(research_agent(query))


@tool
def math_tool(query: str) -> str:
    """Delegate math problems to the math agent."""
    return str(math_agent(query))


ORCH_PROMPT = (
    "You are an orchestrator. Route to research_tool for web/info, math_tool for calculations."
)


def main() -> None:
    orchestrator = Agent(model=ollama_model, system_prompt=ORCH_PROMPT, tools=[research_tool, math_tool])

    print("=== Research ===")
    print(orchestrator("Find the release year of Python 3.12 and cite a source."))

    print("\n=== Math ===")
    print(orchestrator("Compute the derivative of x^3 and evaluate at x=2."))


if __name__ == "__main__":
    main()

