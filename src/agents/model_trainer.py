"""Placeholder model trainer for a blank competition."""
from __future__ import annotations


def run(variant: str, n_folds: int = 5, seeds: list[int] | None = None) -> None:
    raise NotImplementedError(
        "Implement competition-specific training logic in src/agents/model_trainer.py."
    )
