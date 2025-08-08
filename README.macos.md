## Strands Agents — macOS Setup (Terminal)

### Prerequisites
- **macOS 12+** (Apple Silicon or Intel)
- **Python 3.10+** (check with `python3 --version`)
- **Ollama for macOS** (download from [Ollama download page](https://ollama.com/download))
- Optional: **Homebrew** and **Git**

### 1) Clone or open the project
If you haven’t already:

```bash
git clone https://github.com/your-org/strands-agents.git
cd strands-agents
```

### 2) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Install and run Ollama (model server)
1. Install the Ollama app and start it (local server at `http://localhost:11434`).
2. Pull a model (default used here: `qwen3:8b`):

```bash
ollama pull qwen3:8b
# If the server isn’t running already:
ollama serve
```

### 4) Run the example agent
Set the model (optional; defaults to `qwen3:8b`) and run the business rules demo:

```bash
export OLLAMA_MODEL="qwen3:8b"
python examples/python/business_rules_agent.py
```

You should see decisions printed and logs written to `runlogs/business_rules/` (e.g., `runlogs/business_rules/ORD-1001.log`).

### Other example scripts
```bash
python examples/python/agent_quickstart.py
python examples/python/simple_tools_agent.py
python examples/python/glossary_memory_agent.py
python examples/python/automation_agents.py
python examples/python/orchestrator_agent.py
```

### Troubleshooting
- **Cannot connect to Ollama / connection refused**: Ensure the Ollama app is open and the server is running at `http://localhost:11434` (run `ollama serve` if needed).
- **Model not found**: Run `ollama pull qwen3:8b` (or export another model via `export OLLAMA_MODEL=...`).
- **ImportError for `strands`**: Ensure the virtual environment is active and `pip install -r requirements.txt` completed without errors.


