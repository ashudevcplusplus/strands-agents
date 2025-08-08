```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -e .
python -m strands_agents
pip install strands strands-tools mcp
pip install pipx
pipx ensurepath
pipx install uv
winget install --id Ollama.Ollama -e --accept-source-agreements --accept-package-agreements
ollama pull qwen3:4b
ollama pull qwen3:8b
$env:OLLAMA_MODEL = "qwen3:8b"
python .\examples\python\simple_tools_agent.py
python .\examples\python\orchestrator_agent.py
python .\examples\python\automation_agents.py
python .\examples\python\agent_quickstart.py
python .\examples\python\agent.py
python .\examples\python\glossary_memory_agent.py
python .\examples\python\dummy_agents.py
pip install -e ".[dev]"
```

