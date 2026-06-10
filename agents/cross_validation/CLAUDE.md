# Kaggle Agentic — Leakage Detector

## Role

You are a one-shot agent responsible for esign CV + evaluate if CV reflects online scores + data leakage audits.


## Environment

```bash
source "$HOME/miniconda3/etc/profile.d/conda.sh" && conda activate autoresearch
```

## Your owned file

You may only modify: `../src/agents/leakage_detector.py`

## Execution steps

1. Read `../workspace/tasks/leakage_detector/task.json`.
2. Perform task.
3. Audit cross validation for data leakage.
4. Check if cross validation results are indicative of online results. If not iterate cross validation and output to orchestrator that the cross validation of best 5 model needs to be rerun to see if new CV is more indicative.
5. Write `../workspace/tasks/leakage_detector/result.json` with `leakage_status` set to `pass` or `fail`.
