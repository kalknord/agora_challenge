"""Zentrale Lade- und Aggregations-Funktionen fuer den Digitalhaushalt-Datensatz.

Die Funktionen hier kapseln drei Entscheidungen, die in der Studie konsequent
gelten:

1. NA-Behandlung: NA in Geld- und Tag-Spalten wird als 0 gelesen. Das ist
   konsistent mit der Sparse-Struktur des Datensatzes (nicht-digitale Titel
   haben systematisch NA in den Digital-Spalten).
2. Primaer-Abgrenzung: digi_soll_eng. weit als Robustheitscheck.
3. Haushaltsgruppen-Logik: erste Ziffer = Hauptgruppe, erste zwei = Obergruppe.
   Mapping nach Bundeshaushaltsordnung.
"""
from pathlib import Path
import pandas as pd

GELD = ['soll', 'digi_soll_eng', 'digi_soll_weit']
TAGS = ['any_tag', 'large_soll_tag', 'texan_tag', 'ml_tag']
KATS = [
    '_1_infra', '_2_dig_wirtschaft', '_3_dig_verwaltung', '_4_dig_kompetenzen',
    '_5_dig_kultur', '_6_forschung_inno', '_7_gesundheitswesen',
    '_8_bundeswehr', '_9_unteibare_ausg',
]
KAT_KURZ = {
    '_1_infra': 'Infrastruktur',
    '_2_dig_wirtschaft': 'Wirtschaft',
    '_3_dig_verwaltung': 'Verwaltung',
    '_4_dig_kompetenzen': 'Kompetenzen',
    '_5_dig_kultur': 'Kultur',
    '_6_forschung_inno': 'Forschung',
    '_7_gesundheitswesen': 'Gesundheit',
    '_8_bundeswehr': 'Bundeswehr',
    '_9_unteibare_ausg': 'Unteilbar',
}

# Hauptgruppen-Mapping nach Bundeshaushaltsordnung
HG_LABEL = {
    '4': 'Personalausgaben',
    '5': 'Saechliche Verwaltungsausgaben',
    '6': 'Zuweisungen und Zuschuesse (laufend)',
    '7': 'Baumassnahmen',
    '8': 'Sonstige Investitionsausgaben',
    '9': 'Besondere Finanzierungsausgaben',
}

# Investiv-Klassifikation auf Obergruppen-Ebene
UG_INVEST_TYP = {
    '81': 'A_eigene_Invest',  # Erwerb beweglicher Sachen
    '82': 'A_eigene_Invest',  # Erwerb unbeweglicher Sachen
    '83': 'B_Transfer_Invest',  # Zuweisungen Laender (oeff. Bereich)
    '86': 'B_Transfer_Invest',  # Zuweisungen Sozialversicherungen
    '87': 'B_Transfer_Invest',  # Investitionsdarlehen an Sonstige
    '88': 'B_Transfer_Invest',  # Zuschuesse an Sonstige im Inland
    '89': 'B_Transfer_Invest',  # Investitionszuschuesse Sonstige
}


def _find_repo_root():
    """Findet das Repo-Root, indem es vom Modul-Standort aus aufwaerts sucht."""
    here = Path(__file__).resolve().parent
    for parent in [here, *here.parents]:
        if (parent / 'data' / 'raw').exists() and (parent / 'src').exists():
            return parent
    # Fallback: Modul-Verzeichnis-Parent (klassisches src/-Layout)
    return here.parent


REPO_ROOT = _find_repo_root()
DEFAULT_DATA_PATH = REPO_ROOT / 'data' / 'raw' / 'Digitalhaushalt_Open_Data.xlsx'


def load(path=None):
    """Laedt den Datensatz mit konsistenter NA-Behandlung und Hilfsspalten.

    Parameters
    ----------
    path : str or Path, optional
        Pfad zur xlsx-Datei. Default: data/raw/Digitalhaushalt_Open_Data.xlsx
        im Repo-Root. Der Repo-Root wird automatisch gefunden, unabhaengig
        vom aktuellen Working Directory (wichtig fuer Jupyter-Notebooks).

    Returns
    -------
    pd.DataFrame
        Mit zusaetzlichen Spalten:
        - hg, ug: erste / erste zwei Ziffern der gruppe (string)
        - hg_label: ausgeschriebene Hauptgruppe
        - typ_invest: A_eigene_Invest / B_Transfer_Invest / None
        - soll_mrd, digi_soll_eng_mrd, digi_soll_weit_mrd: in Mrd. Euro
    """
    p = Path(path) if path is not None else DEFAULT_DATA_PATH
    if not p.exists():
        raise FileNotFoundError(
            f"Datensatz nicht gefunden: {p.resolve()}.\n"
            "Originaldatei von https://agoradigital.de/projekte/digitalhaushalt\n"
            "herunterladen und unter data/raw/Digitalhaushalt_Open_Data.xlsx ablegen."
        )
    df = pd.read_excel(p, sheet_name='Daten')

    df[GELD] = df[GELD].fillna(0)
    df[TAGS + KATS] = df[TAGS + KATS].fillna(0).astype(int)

    df['gruppe_str'] = df['gruppe'].astype(str).str.replace('.0', '', regex=False)
    df['hg'] = df['gruppe_str'].str[0]
    df['ug'] = df['gruppe_str'].str[:2]
    df['hg_label'] = df['hg'].map(HG_LABEL).fillna('keine_HG')
    df['typ_invest'] = df['ug'].map(UG_INVEST_TYP)

    for col in GELD:
        df[col + '_mrd'] = df[col] / 1e6

    return df


def kategorien_allokation(df, jahr=None, geld_col='digi_soll_eng'):
    """Anteilige Allokation: Titel mit n Kategorien -> jede bekommt 1/n des Volumens.

    Returns long-format DataFrame mit Spalten:
    einzelplan, kategorie, volumen
    """
    d = df.copy()
    if jahr is not None:
        d = d[d['jahr'] == jahr]
    d['n_kat'] = d[KATS].sum(axis=1)
    d_k = d[d['n_kat'] >= 1].copy()

    rows = []
    for k in KATS:
        contrib = d_k[d_k[k] == 1].copy()
        contrib['v'] = contrib[geld_col] / contrib['n_kat']
        ag = contrib.groupby('einzelplan')['v'].sum().reset_index()
        ag['kategorie'] = KAT_KURZ[k]
        ag = ag.rename(columns={'v': 'volumen'})
        rows.append(ag)
    return pd.concat(rows, ignore_index=True)


def hhi(df, jahr, groupby='einzelplan', geld_col='digi_soll_eng'):
    """Herfindahl-Hirschman-Index, Skala 0-10000.

    <1500 = fragmentiert, 1500-2500 = maessig konzentriert, >2500 = stark.
    """
    s = df[df['jahr'] == jahr].groupby(groupby)[geld_col].sum()
    s = s[s > 0]
    shares = s / s.sum()
    return float((shares ** 2).sum() * 10000)


def panel_titel(df, jahre=None):
    """Filtert auf Titel-IDs, die in allen angegebenen Jahren auftauchen.

    Default: in allen 4 Jahren des Datensatzes (2019, 2021, 2023, 2024).
    Nuetzlich fuer ID-stabile Trendvergleiche.
    """
    if jahre is None:
        jahre = sorted(df['jahr'].unique())
    counts = df[df['jahr'].isin(jahre)].groupby('id')['jahr'].nunique()
    stable_ids = counts[counts == len(jahre)].index
    return df[df['id'].isin(stable_ids)].copy()
