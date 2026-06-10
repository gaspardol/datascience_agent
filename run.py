"""Pipeline runner for a blank Kaggle competition template."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
EXPERIMENTS = ROOT / "experiments"

sys.path.insert(0, str(ROOT))


def _require_data_files() -> None:
    missing = [name for name in ("train.csv", "test.csv") if not (ROOT / name).exists()]
    if missing:
        raise FileNotFoundError(
            "Missing data files: "
            + ", ".join(missing)
            + ". Add competition data to the template root before running feature generation."
        )


def phase_features() -> None:
    from src.features.engineering import engineer_all, get_feature_cols

    _require_data_files()
    train = pd.read_csv(ROOT / "train.csv")
    test = pd.read_csv(ROOT / "test.csv")

    train_fe = engineer_all(train)
    test_fe = engineer_all(test)
    feat_cols = get_feature_cols(train_fe)

    out = EXPERIMENTS / "features"
    out.mkdir(parents=True, exist_ok=True)

    keep_train = feat_cols + ([c for c in ("target", "class", "label") if c in train_fe.columns][:1])
    keep_test = [c for c in feat_cols if c in test_fe.columns]

    train_fe[keep_train].to_parquet(out / "train_features.parquet", index=False)
    test_fe[keep_test].to_parquet(out / "test_features.parquet", index=False)
    print(f"[features] saved {len(feat_cols)} features")


def phase_profile() -> None:
    from src.agents.data_profiler import run

    run()


def phase_train(variants: list[str], n_folds: int, seeds: list[int]) -> None:
    from src.agents.model_trainer import run

    for variant in variants:
        run(variant, n_folds=n_folds, seeds=seeds)


def phase_submit(variant: str, label: str | None) -> None:
    from src.agents.submission_manager import run

    path = run(variant, label=label)
    print(f"[submit] submission ready: {path}")


def phase_leakage() -> None:
    from src.agents.leakage_detector import run

    run()


def phase_ensemble() -> None:
    from src.agents.ensemble_agent import run

    run()


def phase_status() -> None:
    print("\n=== Status ===")

    model_dirs = sorted((EXPERIMENTS / "models").glob("*/result.json")) if (EXPERIMENTS / "models").exists() else []
    for path in model_dirs:
        result = json.loads(path.read_text())
        variant = result.get("variant", path.parent.name)
        cv_mean = result.get("cv_mean")
        cv_std = result.get("cv_std")
        oof = result.get("oof_acc")
        print(f"  {variant:30s}  CV={cv_mean}±{cv_std}  OOF={oof}")

    submissions = sorted((EXPERIMENTS / "submissions").glob("*.json")) if (EXPERIMENTS / "submissions").exists() else []
    if submissions:
        print("\n=== Submissions ===")
        for path in submissions:
            submission = json.loads(path.read_text())
            print(f"  {path.stem}: {submission.get('submission_status', 'pending')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=["features", "profile", "train", "submit", "status", "leakage", "ensemble"])
    parser.add_argument("--variants", nargs="+", default=["baseline"])
    parser.add_argument("--n-folds", type=int, default=5)
    parser.add_argument("--seeds", nargs="+", type=int, default=[42])
    parser.add_argument("--label", default=None)
    args = parser.parse_args()

    if args.phase == "features":
        phase_features()
    elif args.phase == "profile":
        phase_profile()
    elif args.phase == "train":
        phase_train(args.variants, args.n_folds, args.seeds)
    elif args.phase == "submit":
        phase_submit(args.variants[0], args.label)
    elif args.phase == "leakage":
        phase_leakage()
    elif args.phase == "ensemble":
        phase_ensemble()
    elif args.phase == "status":
        phase_status()


if __name__ == "__main__":
    main()
