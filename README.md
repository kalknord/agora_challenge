# agora_challenge

Daten-Challenge Digitalhaushalt — Agora Digitale Transformation / ZEW Mannheim.

## Schnellstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Datensatz ablegen (nicht im Repo):
# data/raw/Digitalhaushalt_Open_Data.xlsx

# Smoke-Test (Replikation der ZEW-Eckwerte)
jupyter nbconvert --to notebook --execute notebooks/00_profiling.ipynb --output /tmp/test.ipynb

# Interaktiv
jupyter lab notebooks/00_profiling.ipynb

# Hero-Charts neu generieren
jupyter nbconvert --to notebook --execute --inplace notebooks/chart_h1.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/chart_h2.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/chart_h4.ipynb
```