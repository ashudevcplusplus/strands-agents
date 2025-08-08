from __future__ import annotations

import json
import os
import re
from datetime import datetime

from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands_tools import http_request

AUTOMATION_DIR = os.path.join("runlogs", "automation")


def _ensure_parent(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)


@tool
def ensure_dir(path: str) -> str:
    """Create directory if it does not exist (including parents)."""
    os.makedirs(path, exist_ok=True)
    return f"Ensured directory: {path}"


@tool
def write_text_file(path: str, text: str, mode: str = "w") -> str:
    """Write text to file. mode: 'w' to overwrite, 'a' to append."""
    if mode not in {"w", "a"}:
        return "Error: mode must be 'w' or 'a'"
    _ensure_parent(path)
    with open(path, mode, encoding="utf-8") as f:
        f.write(text)
        if mode == "a":
            f.write("\n")
    return f"Wrote to {path}"


@tool
def read_text_file(path: str, max_chars: int | None = 4000) -> str:
    """Read text from file, optionally truncating to max_chars."""
    if not os.path.exists(path):
        return f"Error: file not found: {path}"
    with open(path, encoding="utf-8") as f:
        data = f.read()
    if max_chars is not None and len(data) > max_chars:
        return data[:max_chars] + "\n...[truncated]"
    return data


@tool
def list_dir(path: str) -> str:
    """List files and directories (non-recursive)."""
    if not os.path.isdir(path):
        return f"Error: not a directory: {path}"
    entries = sorted(os.listdir(path))
    if not entries:
        return "(empty)"
    return "\n".join(entries)


@tool
def append_log(name: str, entry: str) -> str:
    """Append a timestamped log entry under runlogs/automation/{name}.log"""
    os.makedirs(AUTOMATION_DIR, exist_ok=True)
    ts = datetime.utcnow().isoformat() + "Z"
    path = os.path.join(AUTOMATION_DIR, f"{name}.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {entry}\n")
    return f"Appended log entry to {path}"


@tool
def extract_title(html: str) -> str:
    """Extract the <title> from HTML. Returns '(no title)' if not found."""
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if not m:
        return "(no title)"
    return re.sub(r"\s+", " ", m.group(1)).strip()


@tool
def save_json(path: str, data: str) -> str:
    """Save JSON string to a file with pretty formatting."""
    try:
        obj = json.loads(data)
    except json.JSONDecodeError as e:
        return f"Error: invalid JSON: {e}"
    _ensure_parent(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return f"Saved JSON to {path}"


def build_model() -> OllamaModel:
    model_tag = os.getenv("OLLAMA_MODEL", "qwen3:4b")
    return OllamaModel(host="http://localhost:11434", model_id=model_tag)


def build_file_agent(model: OllamaModel) -> Agent:
    return Agent(
        model=model,
        system_prompt="You manage files reliably. Prefer absolute/explicit paths.",
        tools=[ensure_dir, write_text_file, read_text_file, list_dir, append_log, save_json],
    )


def build_web_agent(model: OllamaModel) -> Agent:
    return Agent(
        model=model,
        system_prompt="You fetch URLs and extract key info using tools.",
        tools=[http_request, extract_title],
    )


def build_delegate_tools(file_agent: Agent, web_agent: Agent):
    @tool
    def files_task(instruction: str) -> str:
        """Delegate file-related tasks (create dirs, read/write files, logs, JSON)."""
        return str(file_agent(instruction))

    @tool
    def web_task(instruction: str) -> str:
        """Delegate web-related tasks (HTTP requests, parse titles)."""
        return str(web_agent(instruction))

    return files_task, web_task


def build_orchestrator(model: OllamaModel, files_task, web_task) -> Agent:
    return Agent(
        model=model,
        system_prompt=(
            "You are an automation orchestrator.\n"
            "- Use web_task for HTTP fetching and HTML parsing.\n"
            "- Use files_task for directory management, file I/O, logging, and JSON.\n"
            "Execute steps in order and confirm results succinctly."
        ),
        tools=[files_task, web_task],
    )


def main() -> None:
    model = build_model()

    file_agent = build_file_agent(model)
    web_agent = build_web_agent(model)
    files_task, web_task = build_delegate_tools(file_agent, web_agent)
    orchestrator = build_orchestrator(model, files_task, web_task)

    run_dir = AUTOMATION_DIR
    title_path = os.path.join(run_dir, "title.txt")

    print("=== Automation Task 1: Fetch URL and save title ===")
    print(
        orchestrator(
            f"Create directory '{run_dir}'. "
            "Fetch https://example.com, extract the HTML <title>, "
            f"save it to '{title_path}', "
            "and append a 'fetched example.com' entry to automation log 'session'."
        )
    )

    print("\n=== Automation Task 2: Append timestamped log ===")
    print(
        orchestrator(
            "Append a timestamped log entry 'automation run complete' to automation log 'session'."
        )
    )

    print("\n=== Automation Task 3: List run directory ===")
    print(orchestrator(f"List files in '{run_dir}'."))

    print("\n=== Automation Task 4: Save small JSON artifact ===")
    artifact_path = os.path.join(run_dir, "artifact.json")
    artifact_json = json.dumps({"status": "ok", "ts": datetime.utcnow().isoformat() + "Z"})
    print(orchestrator(f"Save this JSON to '{artifact_path}': {artifact_json}"))


if __name__ == "__main__":
    main()
