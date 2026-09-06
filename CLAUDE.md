---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [ai-agents, contributors]
last_updated: 2026-09-06
last-verified: 2026-09-06
---

# CLAUDE.md: MagLogic

Universal agent rules and simplicity defaults live in [AGENTS.md](AGENTS.md). Read that first.

## Claude-specific deltas

Shared voice and research-writing contract:

- <https://github.com/alawein/alawein/blob/main/docs/style/VOICE.md>
- <https://github.com/alawein/alawein/blob/main/prompt-kits/AGENT.md>

Extra verification useful in Claude sessions:

```bash
conda env create -f environment.yml
PYTHONPATH=python python -c "import maglogic"
```

Prefer the real engine boundary over fake abstraction when OOMMF/MuMax3 solver details matter.
