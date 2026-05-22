"""01 - H1: Polyzentrik des Digitalhaushalts.

Drei Drilldown-Stufen:
  1. Konzentrationsmasse (HHI, Top-Anteile) je Jahr
  2. Ranglisten-Veraenderung 2019 vs. 2024
  3. Profile der Top-Ressorts ueber 9 Kategorien (Allokations-Methode)
  4. BMDS-Buendelungs-Szenarien als Volumen-Quantifizierung

Outputs: figures/h1_profile_2024.png, figures/h1_hhi_zeitreihe.png
"""
# %% Imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.load import load, kategorien_allokation, hhi, KATS, KAT_KURZ

df = load('data/raw/Digitalhaushalt_Open_Data.xlsx')

# %% Drilldown 1: Konzentrationsmasse
print("=== Konzentration ueber Einzelplaene (digi_soll_eng) ===\n")
rows = []
for j in sorted(df['jahr'].unique()):
    ep = df[df['jahr'] == j].groupby('einzelplan')['digi_soll_eng'].sum()
    ep = ep[ep > 0].sort_values(ascending=False)
    total = ep.sum()
    shares = ep / total
    n_80 = (shares.cumsum() < 0.8).sum() + 1
    rows.append({
        'jahr': j,
        'aktive_EP': len(ep),
        'HHI': round(hhi(df, j)),
        'Top1_%': round(shares.iloc[0] * 100, 1),
        'Top3_%': round(shares.iloc[:3].sum() * 100, 1),
        'Top5_%': round(shares.iloc[:5].sum() * 100, 1),
        'EP_fuer_80%': n_80,
        'Sigma_Mrd': round(total / 1e6, 2),
    })
konz = pd.DataFrame(rows)
print(konz.to_string(index=False))

# %% Drilldown 2: Ranglisten-Vergleich
print("\n=== Top-10 Ressorts 2019 vs. 2024 (Mrd. EUR) ===")
for j in [2019, 2024]:
    print(f"\n{j}:")
    ep = df[df['jahr'] == j].groupby(
        ['einzelplan', 'einzelplantext']
    )['digi_soll_eng'].sum().div(1e6)
    ep = ep[ep > 0.05].sort_values(ascending=False).head(10)
    for i, ((nr, txt), v) in enumerate(ep.items(), 1):
        print(f"  {i:>2}. EP{nr:>2}  {v:>5.2f} Mrd  {str(txt)[:55]}")

# %% Drilldown 3: Profile der Top-Ressorts 2024
print("\n=== Profile der Top-Ressorts 2024 (anteilige Allokation) ===")
alloc = kategorien_allokation(df, jahr=2024)
profile = alloc.pivot_table(
    index='einzelplan', columns='kategorie', values='volumen', fill_value=0,
)
profile = profile / 1e6  # in Mrd.
profile['Sigma'] = profile.sum(axis=1)
top7 = profile.sort_values('Sigma', ascending=False).head(7)

# In Prozentanteilen
pct = top7.drop(columns='Sigma').div(top7['Sigma'], axis=0).mul(100).round(1)
print("\nProfile (in % der Ressort-Digital-Ausgaben):")
print(pct.to_string())

# Dominantes Profil pro Ressort
print("\nTop-2-Kategorien pro Ressort:")
for ep, row in pct.iterrows():
    sorted_k = row.sort_values(ascending=False)
    vol = top7.loc[ep, 'Sigma']
    print(
        f"  EP{int(ep):>2} ({vol:.2f} Mrd): "
        f"{sorted_k.index[0]} {sorted_k.iloc[0]:.0f}% | "
        f"{sorted_k.index[1]} {sorted_k.iloc[1]:.0f}%"
    )

# %% Drilldown 4: BMDS-Buendelungs-Szenarien
print("\n=== BMDS-Buendelungs-Szenarien fuer 2024 ===")
total = df[df['jahr'] == 2024]['digi_soll_eng'].sum() / 1e6
print(f"Digital-Soll 2024 gesamt: {total:.2f} Mrd EUR\n")

# Helper: anteiliges Volumen einer Auswahl
def vol_subset(df_year, ep_list=None, kat_list=None):
    sub = df_year.copy()
    if ep_list is not None:
        sub = sub[sub['einzelplan'].isin(ep_list)]
    sub['n_kat'] = sub[KATS].sum(axis=1)
    sub = sub[sub['n_kat'] >= 1]
    if kat_list is None:
        return sub['digi_soll_eng'].sum() / 1e6
    v = 0.0
    for k in kat_list:
        part = sub[sub[k] == 1]
        v += (part['digi_soll_eng'] / part['n_kat']).sum()
    return v / 1e6

d24 = df[df['jahr'] == 2024].copy()

# Szenarien
zivile_ep = [4, 5, 6, 7, 8, 15, 16, 17, 25, 30]  # ohne EP 12 BMDV, ohne EP 14 BMVg

szen = {
    'Minimal-BMDS (Verwaltungs-IT ziviler Ressorts ohne BMDV)':
        vol_subset(d24, ep_list=zivile_ep, kat_list=['_3_dig_verwaltung']),
    'Realistisch (zusaetzlich BMI-Infrastruktur)':
        (vol_subset(d24, ep_list=zivile_ep, kat_list=['_3_dig_verwaltung']) +
         vol_subset(d24, ep_list=[6], kat_list=['_1_infra'])),
    'Maximal (alles ausser Bundeswehr & Forschung)':
        vol_subset(
            d24,
            ep_list=[4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 17, 25, 30],
            kat_list=[
                '_1_infra', '_2_dig_wirtschaft', '_3_dig_verwaltung',
                '_4_dig_kompetenzen', '_5_dig_kultur',
                '_7_gesundheitswesen', '_9_unteibare_ausg',
            ],
        ),
}
for name, v in szen.items():
    print(f"  {name}: {v:.2f} Mrd ({v/total*100:.1f}% des Digital-Solls)")
