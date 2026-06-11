"""Digitalhaushalt-Challenge Analysetools."""
from .load import (
    load,
    kategorien_allokation,
    hhi,
    panel_titel,
    REPO_ROOT,
    DEFAULT_DATA_PATH,
    GELD,
    TAGS,
    KATS,
    KAT_KURZ,
    HG_LABEL,
    UG_INVEST_TYP,
)

# Convenience: Pfad zum figures-Verzeichnis im Repo-Root, unabhaengig
# vom Working Directory. Notebooks und Skripte nutzen FIGURES_DIR,
# damit Outputs konsistent landen.
FIGURES_DIR = REPO_ROOT / 'figures'
OUTPUTS_DIR = REPO_ROOT / 'outputs'

__all__ = [
    'load', 'kategorien_allokation', 'hhi', 'panel_titel',
    'REPO_ROOT', 'DEFAULT_DATA_PATH', 'FIGURES_DIR', 'OUTPUTS_DIR',
    'GELD', 'TAGS', 'KATS', 'KAT_KURZ', 'HG_LABEL', 'UG_INVEST_TYP',
]
