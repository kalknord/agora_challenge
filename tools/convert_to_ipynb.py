"""Konvertiert alle notebooks/*.py zu notebooks/*.ipynb via nbformat.

Logik:
  - Modul-Docstring am Dateianfang  → erste Markdown-Zelle
  - Zellgrenzen: '# %%' -Marker (Marker-Zeile selbst wird nicht in die Zelle übernommen)
  - Keine '# %%'-Marker → eine Code-Zelle für den gesamten Code
  - Notwendige Kernel-Anpassung: Path(__file__) → kompatibel mit Jupyter-Kernel
    (NameError-Guard, CWD-Fallback)

Ausführen:
    python tools/convert_to_ipynb.py
"""
import re
import sys
from pathlib import Path

import nbformat

NOTEBOOKS_DIR = Path(__file__).parent.parent / "notebooks"

# Notwendige Kernel-Anpassung: __file__ ist im Jupyter-Kernel nicht definiert.
# Zusätzlich: os.chdir(_root) stellt sicher, dass relative Datenpfade
# (data/raw/...) unabhängig vom Kernel-Startverzeichnis funktionieren.
# Bewahrt das Skript-Verhalten via __file__-Guard.
_FILE_ORIG = "sys.path.insert(0, str(Path(__file__).parent.parent))"
_FILE_FIX = (
    "_root = (\n"
    "    Path(__file__).parent.parent if '__file__' in globals() else\n"
    "    next(p for p in [Path.cwd(), Path.cwd().parent] if (p / 'src').exists())\n"
    ")\n"
    "sys.path.insert(0, str(_root))\n"
    "__import__('os').chdir(_root)"
)


def extract_docstring(source: str) -> tuple[str | None, str]:
    """Gibt (docstring, restlicher_code) zurück."""
    m = re.match(r'^"""(.*?)"""\s*', source, re.DOTALL)
    if m:
        return m.group(1).strip(), source[m.end():]
    return None, source


def split_on_percent_markers(source: str) -> list[str]:
    """Zerlegt Code an '# %%'-Zeilen; leere Blöcke werden verworfen."""
    parts = re.split(r"^# %%[^\n]*\n?", source, flags=re.MULTILINE)
    return [p.rstrip("\n") for p in parts if p.strip()]


def convert(py_path: Path) -> Path:
    source = py_path.read_text(encoding="utf-8")

    docstring, code = extract_docstring(source)
    code = code.replace(_FILE_ORIG, _FILE_FIX)

    code_cells = split_on_percent_markers(code)

    nb = nbformat.v4.new_notebook()
    if docstring:
        nb.cells.append(nbformat.v4.new_markdown_cell(docstring))
    for block in code_cells:
        nb.cells.append(nbformat.v4.new_code_cell(block))

    out = py_path.with_suffix(".ipynb")
    with open(out, "w", encoding="utf-8") as fh:
        nbformat.write(nb, fh)
    print(f"  OK  {py_path.name}  →  {out.name}  "
          f"({len(nb.cells)} Zellen: "
          f"{'1 MD + ' if docstring else ''}{len(code_cells)} Code)")
    return out


if __name__ == "__main__":
    py_files = sorted(NOTEBOOKS_DIR.glob("*.py"))
    if not py_files:
        print("Keine .py-Dateien in notebooks/ gefunden.")
        sys.exit(0)
    print(f"Konvertiere {len(py_files)} Dateien …\n")
    for f in py_files:
        convert(f)
    print("\nFertig.")
