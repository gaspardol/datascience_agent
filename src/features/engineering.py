"""Placeholder feature engineering helpers for a blank competition."""
from __future__ import annotations

import pandas as pd


def engineer_all(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the input frame.

    Replace this with competition-specific feature engineering.
    """

    return df.copy()


def get_feature_cols(df: pd.DataFrame) -> list[str]:
    """Return the columns to keep as model features."""

    excluded = {"class", "target", "label"}
    return [column for column in df.columns if column not in excluded]
