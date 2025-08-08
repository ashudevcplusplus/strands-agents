## Strands Agents — Local Examples

This repo contains local examples for Strands Agents. Choose your OS guide to get started:

- See Windows setup: `README.windows.md`
- See macOS setup: `README.macos.md`

### Quick Start (once dependencies are installed)

Default model is `qwen3:8b` via Ollama at `http://localhost:11434`. You can override with the `OLLAMA_MODEL` env var.

```bash
# macOS/Linux
export OLLAMA_MODEL="qwen3:8b"
python examples/python/business_rules_agent.py

# Windows (PowerShell)
$env:OLLAMA_MODEL = "qwen3:8b"
python examples\python\business_rules_agent.py
```

Logs are written under `runlogs/business_rules/`.


