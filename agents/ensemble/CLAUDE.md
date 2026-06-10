# Kaggle Agentic — Ensemble Agent

## Role

You are a one-shot ensemble agent. Read the task, implement it, report the result, and exit.

## Environment

```bash
source "$HOME/miniconda3/etc/profile.d/conda.sh" && conda activate autoresearch
```

## Your owned file

You may only modify: `../src/agents/ensemble_agent.py`

## Execution steps

1. Read `../workspace/tasks/ensemble/task.json` and `../workspace/state.json`.
2. Inspect the available model outputs in `../experiments/models/`.
3. Implement the requested blend in `../src/agents/ensemble_agent.py`.
4. Run `../run.py --phase ensemble`.
5. Write `../workspace/tasks/ensemble/result.json`.
