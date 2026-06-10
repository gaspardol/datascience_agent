import pandas as pd
import numpy as np
import json
from pathlib import Path


def profile_dataset():
    """Profile the spaceship titanic dataset."""

    # Load data
    train_path = Path(__file__).parent.parent.parent.parent / "data" / "train.csv"
    test_path = Path(__file__).parent.parent.parent.parent / "data" / "test.csv"

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    findings = {}

    # 1. Class balance of Transported
    if "Transported" in train.columns:
        transported_counts = train["Transported"].value_counts()
        transported_pct = train["Transported"].value_counts(normalize=True) * 100
        findings["class_balance"] = {
            "true": int(transported_counts.get(True, 0)),
            "false": int(transported_counts.get(False, 0)),
            "true_pct": float(transported_pct.get(True, 0)),
            "false_pct": float(transported_pct.get(False, 0))
        }

    # 2. Missing values per column
    train_missing = train.isnull().sum()
    test_missing = test.isnull().sum()
    findings["missing_values"] = {
        "train": {col: int(count) for col, count in train_missing[train_missing > 0].items()},
        "test": {col: int(count) for col, count in test_missing[test_missing > 0].items()},
        "train_total": int(train_missing.sum()),
        "test_total": int(test_missing.sum())
    }

    # 3. Cabin parsing analysis
    cabin_analysis = {
        "non_null_cabins_train": int(train["Cabin"].notna().sum()),
        "null_cabins_train": int(train["Cabin"].isna().sum()),
        "non_null_cabins_test": int(test["Cabin"].notna().sum()),
        "null_cabins_test": int(test["Cabin"].isna().sum()),
    }

    # Parse cabin format for non-null values
    if train["Cabin"].notna().any():
        sample_cabins = train[train["Cabin"].notna()]["Cabin"].head(10).tolist()
        cabin_analysis["sample_cabins"] = sample_cabins

        # Try to parse deck/num/side
        cabins_parsed = 0
        decks = set()
        for cabin in train[train["Cabin"].notna()]["Cabin"]:
            parts = str(cabin).split("/")
            if len(parts) == 3:
                cabins_parsed += 1
                decks.add(parts[0])

        cabin_analysis["format_DDD/NNN/S_count"] = cabins_parsed
        cabin_analysis["unique_decks"] = sorted(list(decks))

    findings["cabin_analysis"] = cabin_analysis

    # 4. Spending features distribution
    spending_cols = ["RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]
    spending_analysis = {}

    for col in spending_cols:
        if col in train.columns:
            non_zero = (train[col] > 0).sum()
            zero_count = (train[col] == 0).sum()
            missing = train[col].isna().sum()

            spending_analysis[col] = {
                "zero_count": int(zero_count),
                "zero_pct": float((zero_count / len(train)) * 100),
                "non_zero_count": int(non_zero),
                "null_count": int(missing),
                "mean": float(train[col].mean()) if train[col].notna().any() else 0,
                "median": float(train[col].median()) if train[col].notna().any() else 0,
                "max": float(train[col].max()) if train[col].notna().any() else 0
            }

    findings["spending_features"] = spending_analysis

    # 5. CryoSleep correlation with spending
    if "CryoSleep" in train.columns:
        cryo_spending = {}
        for col in spending_cols:
            if col in train.columns:
                cryo_true = train[train["CryoSleep"] == True][col]
                cryo_false = train[train["CryoSleep"] == False][col]

                cryo_spending[col] = {
                    "cryo_true_mean": float(cryo_true.mean()),
                    "cryo_true_median": float(cryo_true.median()),
                    "cryo_true_zero_pct": float((cryo_true == 0).sum() / len(cryo_true) * 100),
                    "cryo_false_mean": float(cryo_false.mean()),
                    "cryo_false_median": float(cryo_false.median()),
                    "cryo_false_zero_pct": float((cryo_false == 0).sum() / len(cryo_false) * 100)
                }

        findings["cryosleep_spending"] = cryo_spending

    # 6. PassengerId group encoding analysis
    if "PassengerId" in train.columns:
        pid_analysis = {
            "sample_ids": train["PassengerId"].head(10).tolist(),
            "format_observed": "GGGG_PP (expected)"
        }

        # Check if format matches GGGG_PP
        valid_format = 0
        for pid in train["PassengerId"]:
            parts = str(pid).split("_")
            if len(parts) == 2 and len(parts[0]) == 4 and len(parts[1]) == 2:
                valid_format += 1

        pid_analysis["valid_gggg_pp_format"] = valid_format
        pid_analysis["total_ids"] = len(train)

        findings["passengerid_analysis"] = pid_analysis

    return findings


def main():
    """Execute profiling and write results."""
    findings = profile_dataset()

    # Write results
    result_path = Path(__file__).parent.parent.parent.parent / "orchestrator" / "workspace" / "tasks" / "data_profiler" / "result.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)

    result = {
        "task_id": "dp_001",
        "status": "completed",
        "findings": findings,
        "summary": generate_summary(findings)
    }

    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Profile written to {result_path}")
    return result


def generate_summary(findings):
    """Generate a concise text summary of findings."""
    lines = []

    if "class_balance" in findings:
        cb = findings["class_balance"]
        lines.append(f"Class balance: {cb['true_pct']:.1f}% Transported=True, {cb['false_pct']:.1f}% False")

    if "missing_values" in findings:
        mv = findings["missing_values"]
        if mv.get("train"):
            lines.append(f"Train missing values: {mv['train_total']} total ({', '.join(f'{k}:{v}' for k,v in mv['train'].items())})")

    if "cabin_analysis" in findings:
        ca = findings["cabin_analysis"]
        lines.append(f"Cabin: {ca['non_null_cabins_train']} non-null (train), {ca['non_null_cabins_test']} (test)")
        if "unique_decks" in ca:
            lines.append(f"  Decks found: {', '.join(ca['unique_decks'])}")

    if "spending_features" in findings:
        lines.append("Spending features: High zero rates indicate many passengers don't spend")
        for col, stats in findings["spending_features"].items():
            lines.append(f"  {col}: {stats['zero_pct']:.1f}% zeros, median={stats['median']:.0f}, max={stats['max']:.0f}")

    if "cryosleep_spending" in findings:
        lines.append("CryoSleep correlation: Cryo passengers should have near-zero spending")
        cr = findings["cryosleep_spending"]
        if "RoomService" in cr:
            lines.append(f"  RoomService - Cryo mean={cr['RoomService']['cryo_true_mean']:.1f}, Non-cryo mean={cr['RoomService']['cryo_false_mean']:.1f}")

    if "passengerid_analysis" in findings:
        pa = findings["passengerid_analysis"]
        pct_valid = (pa['valid_gggg_pp_format'] / pa['total_ids']) * 100
        lines.append(f"PassengerId: {pct_valid:.1f}% match GGGG_PP format")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
