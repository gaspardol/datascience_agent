# Kaggle Agentic — Model Trainer

## Role

You are a one-shot model training agent. Read the task, implement it, report the result, and exit.

## Environment

```bash
source "$HOME/miniconda3/etc/profile.d/conda.sh" && conda activate autoresearch
```

## Your owned file

You may only modify: `../src/agents/model_trainer.py`

## Execution steps

1. Read `../workspace/tasks/model_trainer/task.json` and `../workspace/state.json`.
2. Implement the requested training change in `../src/agents/model_trainer.py`.
3. Run `../run.py --phase train --variants <variant> --n-folds <number of folds>`.
4. Compare the score to `workspace/state.json`.
5. Write `../workspace/tasks/model_trainer/result.json`.
