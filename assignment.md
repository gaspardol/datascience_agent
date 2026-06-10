# Competition Assignment

## Competition

- **Name**: `<competition name>`
- **Slug**: `<competition-slug>`  # use for kaggle CLI (e.g. "playground-series-s6e6")
- **URL**: `<competition url>`
- **Deadline**: `<deadline>`
- **Submission limit**: `<limit/day>`
- **Metric**: `<metric>`

## Task

Short description of the prediction problem, target column, and evaluation metric. Include:
- Target column name (e.g. `target`, `class`)
- Problem type (binary / multiclass / regression / ranking)
- Any special constraints (public/private test split, embargoed files, external data allowed?)

## Data

List expected files placed in the competition root and any schema notes:
- `train.csv` — training rows with target
- `test.csv` — test features
- `sample_submission.csv` — required submission format
- `additional/*` — any extra provided files

Record column types, important features, and any required preprocessing (e.g., date parsing, missing-value sentinel values).

## Setup instructions for the setup_competition agent

Write a task JSON to `agents/setup_competition/workspace/task.json` with the field `competition` set to either the competition slug or full Kaggle URL. The setup agent will:
1. Validate Kaggle CLI credentials (look for `~/.kaggle/kaggle.json` or env vars `KAGGLE_USERNAME`/`KAGGLE_KEY`).
2. Search for the competition if a slug is not exact.
3. Download competition overview (description) and rules into `reports/` and write metadata to `workspace/competition_metadata.json`.
4. Download any important rule files (e.g. `rules.pdf`) into `reports/` when available.

## Notes

Add domain knowledge, leakage warnings, or experiment constraints here.

---

When copying this template into a real competition, replace bracketed placeholders and run the setup agent to fetch competition files and populate `reports/` and `workspace/`.
