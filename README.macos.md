```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e .
python -m strands_agents
pip install strands strands-tools mcp
brew install --cask ollama
ollama pull qwen3:4b
ollama pull qwen3:8b
export OLLAMA_MODEL="qwen3:8b"
python ./examples/python/simple_tools_agent.py
python ./examples/python/orchestrator_agent.py
python ./examples/python/automation_agents.py
python ./examples/python/agent_quickstart.py
python ./examples/python/agent.py
python ./examples/python/glossary_memory_agent.py
python ./examples/python/dummy_agents.py
pip install -e ".[dev]"
```

```bash
brew install uv
python ./examples/python/agent.py
```

