"""00 - Profiling: Replikation der ZEW-Eckwerte und Konsistenzpruefung.

Phase-0-Output. Laeuft in unter 10 Sekunden, dient als Smoke-Test der
gesamten Pipeline. Fuer Jupyter Lab: als .py mit jupytext oeffnen oder
direkt python ausfuehren.

    python notebooks/00_profiling.py
"""
# %% Imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.load import load

import pandas as pd

# %% Laden
df = load('data/raw/Digitalhaushalt_Open_Data.xlsx')
print(f"Zeilen: {len(df):,}")
print(f"Jahre: {sorted(df['jahr'].unique())}")
print(f"Unique Titel-IDs: {df['id'].nunique():,}\n")

# %% Replikation der ZEW-Eckwerte (digi_soll_eng in Mrd.)
print("=== Replikation ZEW-Eckwerte (digi_soll_eng in Mrd. EUR) ===")
agg = df.groupby('jahr').agg(
    soll_mrd=('soll', lambda x: x.sum() / 1e6),
    eng_mrd=('digi_soll_eng', lambda x: x.sum() / 1e6),
    weit_mrd=('digi_soll_weit', lambda x: x.sum() / 1e6),
    n_titel=('id', 'count'),
).round(2)
print(agg)

erwartet = {2019: 8.5, 2021: 16.6, 2023: 19.2, 2024: 17.9}
print("\nAbweichung digi_soll_eng (Replikation - erwartet):")
for j, e in erwartet.items():
    actual = agg.loc[j, 'eng_mrd']
    delta = actual - e
    print(f"  {j}: {actual:.2f} vs. {e}  Delta = {delta:+.2f} Mrd ({delta/e*100:+.1f}%)")

# %% Konsistenzpruefungen
print("\n=== Konsistenzpruefungen ===")
viol_ew = (df['digi_soll_eng'] > df['digi_soll_weit']).sum()
# weit > soll ist trivial verletzt, wenn soll < 0 (Globale Minderausgaben).
# Pruefen nur fuer nicht-negative soll-Werte:
viol_ws = ((df['digi_soll_weit'] > df['soll']) & (df['soll'] >= 0)).sum()
dup = df.duplicated(subset=['id', 'jahr']).sum()
neg_soll = (df['soll'] < 0).sum()
print(f"  Verletzungen eng > weit: {viol_ew}")
print(f"  Verletzungen weit > soll (ohne Globale Minderausgaben): {viol_ws}")
print(f"  Doppelte (id, jahr): {dup}")
print(f"  Negative soll (Globale Minderausgaben): {neg_soll}")

# %% ID-Stabilitaet
print("\n=== ID-Stabilitaet ueber Jahre ===")
id_jahr = df.groupby('id')['jahr'].nunique()
print(f"  Titel-IDs gesamt: {df['id'].nunique():,}")
for k in [4, 3, 2, 1]:
    n = (id_jahr == k).sum()
    pct = n / df['id'].nunique() * 100
    print(f"  in {k} Jahr(en): {n:,} ({pct:.1f}%)")

# %% Eng-vs-Weit-Spreizung
print("\n=== Eng-Weit-Spreizung des Gesamthaushalts ===")
sp = df.groupby('jahr').agg(
    eng=('digi_soll_eng', lambda x: x.sum() / 1e6),
    weit=('digi_soll_weit', lambda x: x.sum() / 1e6),
)
sp['delta'] = sp['weit'] - sp['eng']
sp['delta_pct'] = (sp['delta'] / sp['weit'] * 100).round(1)
print(sp.round(2))
