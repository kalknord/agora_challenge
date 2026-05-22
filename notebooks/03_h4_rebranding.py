"""03 - H4: Rebranding statt Buzzword-Inflation.

Befund: Die ursprueglich vermutete Buzzword-Inflation laesst sich datenseitig
nicht belegen. Stattdessen zeigt sich politisches Rebranding - vor allem das
vollstaendige Verschwinden der Hightech-Strategie (Merkel-Aera) und das
Erscheinen der Zukunftsstrategie (Ampel) bei vergleichbarem Volumen.

Drilldowns:
  1. ZEW-Schlagwoerter aus titel_text extrahieren (eckige Klammern)
  2. Treffer- und Volumen-Trends 2019 vs. 2024 je Schlagwort
  3. Wachstumsvergleich n vs. Volumen (Inflations-Indikator)

Outputs: figures/h4_rebranding_slope.png
"""
# %% Imports
import sys
import re
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.load import load

df = load('data/raw/Digitalhaushalt_Open_Data.xlsx')


def clean_tag(s):
    """Tag normalisieren: geschweifte Sub-Marker raus, lowercase, trim."""
    s = re.sub(r'\{|\}', '', s).strip().lower()
    s = re.sub(r'\s+', ' ', s)
    return s


def extract_tags(text):
    if not isinstance(text, str):
        return []
    return [clean_tag(t) for t in re.findall(r'\[([^\]]+)\]', text)]


# %% Tags extrahieren
df['tags'] = df['titel_text'].apply(extract_tags)
print(f"Titel mit mindestens einem ZEW-Tag: "
      f"{df['tags'].apply(len).gt(0).sum():,} von {len(df):,}")

# %% Globale Haeufigkeit
all_tags = Counter()
for t in df['tags']:
    all_tags.update(t)

print("\n=== Top-20 ZEW-Schlagwoerter, alle Jahre kumuliert ===")
for tag, n in all_tags.most_common(20):
    print(f"  {n:>5}  {tag}")

# %% Treffer und Volumen je Tag und Jahr
top_tags = [t for t, _ in all_tags.most_common(25)]
res = []
for tag in top_tags:
    has_tag = df['tags'].apply(lambda lst: tag in lst)
    row = {'tag': tag}
    for j in sorted(df['jahr'].unique()):
        sub = df[has_tag & (df['jahr'] == j)]
        row[f'n_{j}'] = len(sub)
        row[f'v_{j}_Mio'] = round(sub['digi_soll_eng'].sum() / 1e3, 1)
    res.append(row)
out = pd.DataFrame(res)

# %% Wachstumsvergleich
print("\n=== Wachstum Treffer vs. Volumen 2019 -> 2024 ===")
print(f"{'Tag':<35} {'n19':>4} {'n24':>4} {'n_x':>5} "
      f"{'v19_Mio':>9} {'v24_Mio':>9} {'v_x':>6}")
print("-" * 80)
for _, r in out.iterrows():
    n19, n24 = r['n_2019'], r['n_2024']
    v19, v24 = r['v_2019_Mio'], r['v_2024_Mio']
    n_fac = f"{n24/n19:.1f}x" if n19 > 0 else 'neu'
    v_fac = f"{v24/v19:.1f}x" if v19 > 0 else 'neu'
    print(f"{r['tag'][:34]:<35} {n19:>4} {n24:>4} {n_fac:>5} "
          f"{v19:>9.0f} {v24:>9.0f} {v_fac:>6}")

# %% Rebranding-Befund: Hightech-Strategie vs. Zukunftsstrategie
print("\n=== Rebranding-Befund: Politisches Etikett wechselt, Inhalt bleibt ===")
for tag in ['hightech-strategie', 'zukunftsstrategie']:
    has_tag = df['tags'].apply(lambda lst, t=tag: t in lst)
    for j in sorted(df['jahr'].unique()):
        sub = df[has_tag & (df['jahr'] == j)]
        n, v = len(sub), sub['digi_soll_eng'].sum() / 1e6
        print(f"  {tag:<22} {j}: n={n:>3}, V={v:>5.2f} Mrd")
    print()
