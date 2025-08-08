## Strands Agents (Local)

Minimal local package for experimenting with Strands Agents examples.

### Prerequisites
- **Python**: 3.10 or newer (64-bit)
- **Windows PowerShell** (these steps use PowerShell)

Optional (for examples):
- **Ollama**: local LLM server on `http://localhost:11434`
- **uv**: to run an MCP server via `uvx` (used by one example)
- **Git** (recommended)

### Quickstart
1) Create and activate a virtual environment
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

2) Install the package in editable mode
```powershell
pip install -U pip
pip install -e .
```

3) Verify install
```powershell
python -m strands_agents
```
Expected output: `Hello from strands-agents`

### Quickstart (macOS, Apple Silicon)
1) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install the package in editable mode
```bash
python -m pip install -U pip
pip install -e .
```

3) Verify install
```bash
python -m strands_agents
```
Expected output: `Hello from strands-agents`

4) Example dependencies (if you plan to run examples)
```bash
pip install strands strands-tools mcp
```

5) Ollama on macOS (Apple Silicon)
- Install from `https://ollama.com/download` or: `brew install --cask ollama`
- Pull models used by examples:
  - `ollama pull qwen3:4b`
  - `ollama pull qwen3:8b`
- Optional per-shell model selection:
  ```bash
  export OLLAMA_MODEL="qwen3:8b"
  ```

6) Run examples
```bash
# Simple tools agent (uses Ollama)
python ./examples/python/simple_tools_agent.py

# Orchestrator demo (uses Ollama)
python ./examples/python/orchestrator_agent.py

# Automation agents (file I/O, web fetch, JSON; uses Ollama)
python ./examples/python/automation_agents.py
```

Notes:
- If prompted to install Command Line Tools, run `xcode-select --install`.
- Apple Silicon is supported by Ollama out of the box (Metal acceleration handled by Ollama).

### Development setup (formatting, linting, hooks)
Install dev tools defined in the project extras:
```powershell
pip install -e ".[dev]"
```

Useful commands (if you have `make`, otherwise run the tools directly):
- Format: `make format` (or `ruff format .`)
- Lint: `make lint` (or `ruff check .`)
- Auto-fix: `make lint-fix` (or `ruff check --fix .`)
- Pre-commit hooks: `make hooks-install` then `make hooks-run`

### Running the examples
Example scripts are in `examples/python/`. They rely on external packages available on PyPI and, for most scripts, a local Ollama server.

Install example dependencies:
```powershell
pip install strands strands-tools mcp
```

Start Ollama (only required for examples that use `OllamaModel`):
- Install from `https://ollama.com/download` (Windows installer)
- Pull or run a model used by the examples (defaults shown below):
  - `ollama pull qwen3:4b`
  - `ollama pull qwen3:8b`

Optionally set the model for the current PowerShell session:
```powershell
$env:OLLAMA_MODEL = "qwen3:8b"
```

Run an example:
```powershell
# Simple tools agent (uses Ollama)
python .\examples\python\simple_tools_agent.py

# Orchestrator demo (uses Ollama)
python .\examples\python\orchestrator_agent.py

# Automation agents (file I/O, web fetch, JSON; uses Ollama)
python .\examples\python\automation_agents.py
```

Additional examples:
```powershell
# Quickstart (minimal Agent usage; no Ollama requirement in code)
python .\examples\python\agent_quickstart.py

# Multi-agent routing with tools (uses Ollama and an MCP server via uvx)
python .\examples\python\agent.py

# Glossary memory via a tool + Ollama
python .\examples\python\glossary_memory_agent.py

# Dummy agents
python .\examples\python\dummy_agents.py
```

### MCP tool example (domain name check)
`examples/python/agent.py` uses an MCP server launched via `uvx`. To run it:
1) Install `uv` so `uvx` is available (choose ONE):
   - Windows: `pipx install uv`
   - macOS: `brew install uv` or `curl -LsSf https://docs.astral.sh/uv/install.sh | sh`
   - Or follow `https://docs.astral.sh/uv/getting-started/` and ensure `uvx` is on PATH
2) Ensure `fastdomaincheck-mcp-server` is resolvable by `uvx` (it will be downloaded on first use)
3) Run the example:
```powershell
python .\examples\python\agent.py
```

If you prefer not to install `uv`, you can modify the example to invoke the underlying server directly, provided it is installed and available on PATH.

### Troubleshooting
- If `python -m strands_agents` fails, ensure your venv is active and `pip install -e .` succeeded.
- If examples that use Ollama hang or error, verify `ollama list` works and that `http://localhost:11434` is reachable. Pull the required model(s) with `ollama pull qwen3:4b` or `qwen3:8b`.
- On Windows, if `pip install -e ".[dev]"` complains about extras syntax, ensure you included the quotes.
- If `make` is not installed on Windows, run the underlying commands directly (shown above).

### Project info
- **Package name**: `strands-agents-local`
- **Module entry point**: `python -m strands_agents`
- **License**: MIT
- **Docs**: `https://strandsagents.com/latest/documentation/docs/`


