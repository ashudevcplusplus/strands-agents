from __future__ import annotations

import json
import os
from typing import Optional

from strands import Agent, tool
from strands.models.ollama import OllamaModel


GLOSSARY_FILE = os.path.join(os.path.dirname(__file__), "cs_glossary.json")


def _load_glossary() -> dict:
    if not os.path.exists(GLOSSARY_FILE):
        with open(GLOSSARY_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(GLOSSARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_glossary(glossary: dict) -> None:
    with open(GLOSSARY_FILE, "w", encoding="utf-8") as f:
        json.dump(glossary, f, ensure_ascii=False, indent=2)


@tool
def cs_glossary(action: str, term: Optional[str] = None, definition: Optional[str] = None) -> str:
    """Manage a glossary of CS terms. Actions: lookup, add, update, list.

    Args:
        action: One of 'lookup', 'add', 'update', 'list'
        term: Term to operate on
        definition: Definition for add/update
    """
    glossary = _load_glossary()

    if action == "lookup":
        if not term:
            return "Error: term required for lookup"
        return glossary.get(term, f"'{term}' not found")

    if action == "add":
        if not term or not definition:
            return "Error: provide term and definition"
        if term in glossary:
            return f"Error: '{term}' exists. Use update."
        glossary[term] = definition
        _save_glossary(glossary)
        return f"Added '{term}'"

    if action == "update":
        if not term or not definition:
            return "Error: provide term and definition"
        if term not in glossary:
            return f"Error: '{term}' not found. Use add."
        glossary[term] = definition
        _save_glossary(glossary)
        return f"Updated '{term}'"

    if action == "list":
        if not glossary:
            return "Glossary is empty"
        return "\n".join(f"- {t}" for t in sorted(glossary))

    return "Error: unknown action"


AGENT_PROMPT = (
    "You can maintain a glossary with cs_glossary. Use it to add, lookup, and list terms."
)


def main() -> None:
    ollama_model = OllamaModel(host="http://localhost:11434", model_id="llama3.2")
    agent = Agent(model=ollama_model, system_prompt=AGENT_PROMPT, tools=[cs_glossary])

    print("=== Add term ===")
    print(agent("Add 'recursion' to the glossary with a concise definition."))

    print("\n=== List terms ===")
    print(agent("What terms are in the glossary?"))

    print("\n=== Lookup term ===")
    print(agent("Look up recursion in the glossary."))


if __name__ == "__main__":
    main()

