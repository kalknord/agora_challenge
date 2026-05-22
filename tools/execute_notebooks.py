"""Führt alle notebooks/*.ipynb aus und speichert Outputs inplace.

Setzt den Kernel-CWD explizit auf das Projekt-Root, damit relative Pfade
(data/raw/...) und sys.path-Setup korrekt aufgelöst werden.

Ausführen (von Projekt-Root):
    python tools/execute_notebooks.py
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

PROJECT_ROOT = Path(__file__).parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"


def execute(nb_path: Path) -> None:
    nb = nbformat.read(nb_path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=300,
        kernel_name="python3",
        resources={"metadata": {"path": str(PROJECT_ROOT)}},
    )
    client.execute()
    nbformat.write(nb, nb_path)
    print(f"  OK  {nb_path.name}")


if __name__ == "__main__":
    ipynb_files = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))
    if not ipynb_files:
        print("Keine .ipynb-Dateien gefunden.")
        sys.exit(0)
    print(f"Führe {len(ipynb_files)} Notebooks aus (Kernel-CWD = Projekt-Root) …\n")
    failed = []
    for nb_file in ipynb_files:
        try:
            execute(nb_file)
        except Exception as exc:
            print(f"  FEHLER  {nb_file.name}: {exc}")
            failed.append(nb_file.name)
    if failed:
        print(f"\nFehlgeschlagen: {', '.join(failed)}")
        sys.exit(1)
    print("\nAlle Notebooks erfolgreich ausgeführt.")
