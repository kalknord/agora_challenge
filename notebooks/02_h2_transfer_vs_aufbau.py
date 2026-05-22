"""02 - H2: Transfer statt Aufbau - Hauptgruppen-Drilldown.

Hauptbefund: Eigene Bundes-Investitionen (UG 81/82) stagnieren. Investitions-
zuschuesse an Dritte (UG 83/86/87/88/89) verdoppeln ihren Anteil.

Drilldowns:
  1. Konsumtiv vs. Investiv ueber Jahre
  2. Investiv-Detail: eigene vs. Transfer
  3. Treiber-Identifikation (welche Einzelplaene, welche Titel)
  4. Robustheit weite Abgrenzung
  5. HG-6-Spin-off: Mikroelektronik-Peak 2023

Outputs: figures/h2_schere_eigene_vs_transfer.png
"""
# %% Imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.load import load, KATS

df = load('data/raw/Digitalhaushalt_Open_Data.xlsx')

# Nur digitale Titel mit eng>0
d = df[(df['any_tag'] == 1) & (df['digi_soll_eng'] > 0)].copy()

# %% Drilldown 1: Konsumtiv vs. Investiv
print("=== Konsumtiv (HG 4-6) vs. Investiv (HG 7-8) - digi_soll_eng (Mrd) ===")
d['typ_kons_inv'] = d['hg'].map(
    lambda x: 'konsumtiv' if x in ['4', '5', '6']
    else ('investiv' if x in ['7', '8'] else 'sonstiges')
)
agg = d.groupby(['jahr', 'typ_kons_inv'])['digi_soll_eng'].sum().div(1e6).unstack()
agg['Sigma'] = agg.sum(axis=1)
for c in ['konsumtiv', 'investiv', 'sonstiges']:
    if c in agg.columns:
        agg[f'{c}_%'] = (agg[c] / agg['Sigma'] * 100).round(1)
print(agg.round(2))

# %% Drilldown 2: Investiv-Detail nach Obergruppe
print("\n=== HG 8 Detail: eigene vs. Transfer-Investitionen (Mrd) ===")
hg8 = d[d['hg'] == '8']
piv = hg8.groupby(['ug', 'jahr'])['digi_soll_eng'].sum().div(1e6).unstack('jahr').fillna(0)
piv['Delta_19_24'] = piv[2024] - piv[2019]
piv = piv.sort_values(2024, ascending=False)
print(piv.round(3).to_string())

# Aggregiert nach Invest-Typ
print("\n=== Aggregiert: eigene Invest (UG 81/82) vs. Transfer-Invest (UG 83/86/87/88/89) ===")
inv_agg = (
    d[d['typ_invest'].notna()]
    .groupby(['jahr', 'typ_invest'])['digi_soll_eng']
    .sum().div(1e6).unstack().fillna(0)
)
inv_agg['Sigma_Digital'] = d.groupby('jahr')['digi_soll_eng'].sum().div(1e6)
inv_agg['eigene_%'] = (inv_agg['A_eigene_Invest'] / inv_agg['Sigma_Digital'] * 100).round(1)
inv_agg['transfer_%'] = (inv_agg['B_Transfer_Invest'] / inv_agg['Sigma_Digital'] * 100).round(1)
print(inv_agg.round(2).to_string())

# %% Drilldown 3: Wer traegt den Transfer-Boom?
print("\n=== Top-Treiber des Transfer-Booms (UG 88+89, Delta 2019->2024 Mrd) ===")
tr = d[d['ug'].isin(['88', '89'])]
piv2 = (
    tr.groupby(['einzelplan', 'einzelplantext', 'jahr'])['digi_soll_eng']
    .sum().div(1e6).unstack('jahr').fillna(0)
)
piv2['Delta_19_24'] = piv2[2024] - piv2[2019]
print(piv2.sort_values('Delta_19_24', ascending=False).head(6).round(2).to_string())

# %% Drilldown 4: Robustheit mit weiter Abgrenzung
print("\n=== Robustheit: gleiche Struktur unter digi_soll_weit ===")
dw = df[(df['any_tag'] == 1) & (df['digi_soll_weit'] > 0)].copy()
dw['typ_fein'] = dw['ug'].map(
    lambda x: 'A_eigene' if x in ['81', '82']
    else ('B_transfer' if x in ['83', '86', '87', '88', '89']
          else ('konsumtiv' if x[:1] in ['4', '5', '6'] else 'sonstiges'))
)
agg_w = dw.groupby(['jahr', 'typ_fein'])['digi_soll_weit'].sum().div(1e6).unstack().round(2)
print(agg_w.to_string())

# %% Drilldown 5: HG-6-Peak 2023 verstehen
print("\n=== HG-6-Peak 2023: Was steckt dahinter? ===")
hg6 = d[d['hg'] == '6'].copy()
# Mikroelektronik-Titel isolieren
is_mikro = (
    (hg6['einzelplan'] == 60)
    & (hg6['gruppe'] == 686)
    & (hg6['titel_text'].fillna('').str.contains('Mikroelektronik', case=False))
)
print(f"Mikroelektronik-Titel (EP 60, Gruppe 686): {is_mikro.sum()} Zeilen")
print("Volumen je Jahr (Mrd):")
print(hg6[is_mikro].groupby('jahr')['digi_soll_eng'].sum().div(1e6).round(3).to_string())

print("\nHG 6 mit/ohne Mikroelektronik-Titel (Mrd):")
total_hg6 = hg6.groupby('jahr')['digi_soll_eng'].sum().div(1e6)
ohne = hg6[~is_mikro].groupby('jahr')['digi_soll_eng'].sum().div(1e6)
out = pd.DataFrame({'HG6_total': total_hg6, 'HG6_ohne_Mikro': ohne}).round(2)
print(out.to_string())
