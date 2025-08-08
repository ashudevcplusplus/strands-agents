## Strands Agents — Windows Setup (PowerShell)

### Prerequisites
- **Windows 10/11**
- **Python 3.10+** (check with `py -V` or `python --version`)
- **Ollama for Windows** (download from [Ollama download page](https://ollama.com/download))
- Optional: **Git** for cloning

### 1) Clone or open the project
If you haven’t already:

```powershell
git clone https://github.com/your-org/strands-agents.git
cd strands-agents
```

### 2) Create and activate a virtual environment
```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Install and run Ollama (model server)
1. Install Ollama from the link above and start it (it runs a local server at `http://localhost:11434`).
2. Pull a model (default used here: `qwen3:8b`):

```powershell
ollama pull qwen3:8b
# If Ollama is not already running in the background:
ollama serve
```

### 4) Run the example agent
Set the model (optional; defaults to `qwen3:8b`) and run the business rules demo:

```powershell
$env:OLLAMA_MODEL = "qwen3:8b"
python examples/python/business_rules_agent.py
```

You should see decisions printed and logs written to `runlogs/business_rules/` (for example `runlogs/business_rules/ORD-1001.log`).

### Other example scripts
```powershell
python examples/python/agent_quickstart.py
python examples/python/simple_tools_agent.py
python examples/python/glossary_memory_agent.py
python examples/python/automation_agents.py
python examples/python/orchestrator_agent.py
```

### Troubleshooting
- **Cannot connect to Ollama / connection refused**: Ensure the Ollama service is running and listening on `http://localhost:11434` (start the Ollama app or run `ollama serve`).
- **Model not found**: Run `ollama pull qwen3:8b` (or set another model via `$env:OLLAMA_MODEL`).
- **ImportError for `strands`**: Make sure the virtual environment is active and `pip install -r requirements.txt` completed successfully.
- **Permission error when activating venv**: In PowerShell, you may need to allow scripts: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (then re-open PowerShell).


