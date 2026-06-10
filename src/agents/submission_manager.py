"""Placeholder submission packaging logic for a blank competition."""
from __future__ import annotations

from pathlib import Path


def run(variant: str, label: str | None = None) -> Path:
    raise NotImplementedError(
        "Implement competition-specific submission packaging in src/agents/submission_manager.py."
    )
