# DOC — Technische Dokumentation

Vollständige technische Referenz des Repos. Dieses Dokument ist die
Antwort auf die Frage „wie funktioniert das hier unter der Haube?". Für
inhaltliche Befunde, Story-Arc oder den Stand der Hypothesen siehe
README.md und CLAUDE.md.

Inhaltsverzeichnis:

1. [Repo-Struktur](#1-repo-struktur)
2. [Daten-Schema](#2-daten-schema)
3. [src-API](#3-src-api)
4. [Notebook-Übersicht](#4-notebook-übersicht)
5. [Konventionen](#5-konventionen)
6. [Designsystem für Charts](#6-designsystem-für-charts)
7. [Reproduzierbarkeit](#7-reproduzierbarkeit)
8. [Externe Datenquellen](#8-externe-datenquellen)
9. [Entwickler-Workflow](#9-entwickler-workflow)

---

## 1. Repo-Struktur

```
digitalhaushalt-challenge/
├── README.md                 Einstieg, Schnellstart, Story-Arc
├── DOC.md                    Dieses Dokument
├── CLAUDE.md                 Projekt-Gedächtnis für KI-Sessions
├── requirements.txt          Python-Abhängigkeiten
├── .gitignore                xlsx-Daten und ipynb-Checkpoints ausgeschlossen
├── .claude/
│   └── skills/               Projekt-Skills für Claude Code
├── src/                      Library-Code, in Notebooks importiert
│   ├── __init__.py
│   ├── load.py               Lade- und Aggregations-Funktionen
│   ├── style.py              Matplotlib-Designsystem
│   └── reden_mapping.py      Vokabular und Mapping für H5-Verschneidung
├── notebooks/                Alle inhaltliche Analyse, Jupyter-Notebooks
│   ├── 00_profiling.ipynb              Replikation, Konsistenzchecks
│   ├── 01_h1_polyzentrik.ipynb         H1 vollständig
│   ├── 02_h2_transfer_vs_aufbau.ipynb  H2 vollständig
│   ├── 03_h4_rebranding.ipynb          H4 vollständig
│   ├── 04_reden_aufmerksamkeit.ipynb   H5-Verschneidung ZEW × CPP-BT
│   ├── 99_synthese.ipynb               Zusammenführung, Implikation
│   ├── chart_h1.ipynb                  Hero-Chart H1
│   ├── chart_h2.ipynb                  Hero-Chart H2
│   ├── chart_h4.ipynb                  Hero-Chart H4
│   ├── chart_h5.ipynb                  Hero-Chart H5 (Aufmerksamkeit/Volumen)
│   └── chart_anhang_a1.ipynb           Anhang-Chart HG-6-Drilldown
├── data/raw/                 ZEW-Datensatz (nicht im Repo, manuell)
├── data/external/            Externe Quellen für H5 (CPP-BT, CDRS-BT)
├── figures/                  Generierte PNG- und PDF-Charts
└── outputs/                  Essay-Manuskript und Endprodukte
```

**Wichtige Trennung:** `src/` enthält wiederverwendbaren Code. `notebooks/`
enthält die gesamte inhaltliche Analyse. Alles, was eine Aussage über
die Daten macht, lebt in einem Notebook — alles, was darüber hinaus
mehrfach verwendet wird, wandert in `src/`.

---

## 2. Daten-Schema

### 2.1 Primärdatensatz `Digitalhaushalt_Open_Data.xlsx`

Quelle: ZEW Mannheim und Agora Digitale Transformation, Stand 2025.
Bezug über https://agoradigital.de/projekte/digitalhaushalt.

**Dimensionen.** 21.358 Beobachtungen × 25 Spalten. Granularität:
Haushaltstitel × Jahr. 6.240 unique Titel-IDs, davon 4.449 in allen
vier Jahren (Panel-stabil).

**Jahre.** 2019, 2021, 2023, 2024 (keine durchgängige Reihe; 2020 und
2022 fehlen).

**Spalten.**

| Spalte | Typ | Bedeutung |
|--------|-----|-----------|
| `id` | int | Eindeutige Titel-ID, stabil über Jahre |
| `jahr` | int | Haushaltsjahr |
| `digi_klasse` | str/NA | Klasse laut ZEW-Studie Tab. 2 |
| `soll` | float | Gesamt-Sollansatz in Tausend Euro |
| `digi_soll_eng` | float/NA | Enger Digital-Anteil in Tausend Euro |
| `digi_soll_weit` | float/NA | Weiter Digital-Anteil in Tausend Euro |
| `titel_text` | str | Titelbezeichnung, inkl. markierter Schlagwörter `[…]` und `{…}` |
| `_1_infra` bis `_9_unteibare_ausg` | int/NA | 9 thematische Indikatoren (0/1) |
| `any_tag` | int | 1 wenn der Titel als digital klassifiziert wurde |
| `large_soll_tag` | int | 1 wenn das digi_soll > 100 Mio Euro |
| `texan_tag` | int/NA | Textanalyse-Detektion |
| `ml_tag` | int | Machine-Learning-Detektion |
| `einzelplan` | int | Bundes-Einzelplan-Nummer |
| `einzelplantext` | str | Ressort-Bezeichnung |
| `kapitel` | int | Haushaltskapitel |
| `gruppe` | int | Haushalts-Gruppen-Nummer (3-stellig) |
| `funktion` | int | Funktions-Klassifikation |

**NA-Logik des Datensatzes.** Nicht-digitale Titel haben systematisch NA
in `digi_soll_eng`, `digi_soll_weit` und allen 9 Kategorie-Indikatoren.
Das ist eine sparse-Struktur, kein Datenfehler. Die `load()`-Funktion
behandelt diese NAs als 0 (siehe Abschnitt 5).

### 2.2 Hilfsspalten nach `load()`

Die `load()`-Funktion fügt sechs Spalten an:

| Spalte | Typ | Berechnung |
|--------|-----|-----------|
| `gruppe_str` | str | `gruppe` als String, ohne `.0`-Endung |
| `hg` | str | Erste Ziffer von `gruppe_str` = Hauptgruppe |
| `ug` | str | Erste zwei Ziffern von `gruppe_str` = Obergruppe |
| `hg_label` | str | Klartext-Bezeichnung der Hauptgruppe |
| `typ_invest` | str/None | `A_eigene_Invest` (UG 81/82) oder `B_Transfer_Invest` (UG 83/86/87/88/89) |
| `soll_mrd`, `digi_soll_eng_mrd`, `digi_soll_weit_mrd` | float | Geldspalten in Milliarden Euro |

### 2.3 Externe Daten für H5

`data/external/` enthält den Bundestags-Korpus, sofern manuell geladen:

| Datei | Quelle | Lizenz | Stand |
|-------|--------|--------|-------|
| CPP-BT_*.csv | https://doi.org/10.5281/zenodo.4542661 | Public Domain | 2026-01-17 |
| CDRS-BT_*.csv | Zenodo (Sean-Fobbe-Korpus) | Public Domain | 2026-01-17 |

---

## 3. src-API

Alle Funktionen sind aus `src` direkt importierbar (`from src import …`)
oder aus den Untermodulen (`from src.load import …`).

### 3.1 `src.load`

#### `load(path=None) → pd.DataFrame`

Lädt den Datensatz mit konsistenter NA-Behandlung und Hilfsspalten.

- `path`: optional. Default ist `data/raw/Digitalhaushalt_Open_Data.xlsx`
  im Repo-Root. Repo-Root wird automatisch gefunden, unabhängig vom
  aktuellen Working Directory.
- Wirft `FileNotFoundError` mit Bezugs-URL, falls Datensatz nicht da.

#### `kategorien_allokation(df, jahr=None, geld_col='digi_soll_eng') → pd.DataFrame`

Anteilige Allokation von Titel-Volumen auf Kategorien. Bei n markierten
Kategorien bekommt jede 1/n des Volumens.

- Returnt Long-Format-DataFrame mit Spalten `einzelplan`, `kategorie`,
  `volumen`.

#### `hhi(df, jahr, groupby='einzelplan', geld_col='digi_soll_eng') → float`

Herfindahl-Hirschman-Index. Skala 0–10.000:

- unter 1.500: fragmentiert
- 1.500–2.500: mäßig konzentriert
- über 2.500: stark konzentriert

#### `panel_titel(df, jahre=None) → pd.DataFrame`

Filtert auf Titel-IDs, die in allen angegebenen Jahren vorkommen.
Default: alle vier Jahre des Datensatzes. Für „stabiler Kern"-Aussagen.

#### Konstanten

- `REPO_ROOT`: Path zum Repo-Wurzelverzeichnis
- `DEFAULT_DATA_PATH`: Path zum Default-Datensatz
- `FIGURES_DIR`: Path zu `figures/`
- `OUTPUTS_DIR`: Path zu `outputs/`
- `GELD`, `TAGS`, `KATS`: Spaltenlisten
- `KAT_KURZ`: Mapping interne Kategorie-Spalte → Klartext
- `HG_LABEL`: Mapping Hauptgruppen-Ziffer → Klartext
- `UG_INVEST_TYP`: Mapping Obergruppe → Investitions-Typ

### 3.2 `src.style`

Matplotlib-Designsystem. Siehe Abschnitt 6 für die Spezifikation.

#### `apply_style() → None`

Wendet das Designsystem an. Muss am Anfang jedes Chart-Notebooks
aufgerufen werden.

#### `add_quelle(ax, text='...') → None`

Quellen- und Methodennotiz unten links am Chart.

#### `kernaussage(ax, text, x=0.02, y=0.93) → None`

Untertitel-Text über dem Chart.

#### Konstanten

- `COLORS`: Dict mit Akzent-, Neutral-, Highlight-Farben (siehe Abschnitt 6)
- `KATEGORIE_FARBEN`: Dict mit Farben für die 9 ZEW-Kategorien
- `RESSORT_KURZ`: Dict mit Einzelplan-Nummer → Ressort-Kürzel

### 3.3 `src.reden_mapping`

Vokabular und Ressort-Mapping für die H5-Verschneidung mit Bundestag-
Plenarprotokollen.

- `DIGITAL_BEGRIFFE`: Liste digitaler Schlagwörter, abgeleitet aus den
  ZEW-Tags
- `RESSORT_BEGRIFFE`: Dict mit Ressort-Kürzel → Liste ressortspezifischer
  Begriffe
- `RESSORT_TO_EP`: Mapping Kürzel → Einzelplan-Nummer
- `EP_TO_RESSORT`: umgekehrtes Mapping

---

## 4. Notebook-Übersicht

Alle inhaltliche Analyse liegt in den Notebooks. Reihenfolge: erst
Profiling, dann die drei Hypothesen, dann die Charts, dann die
Verschneidung.

| Notebook | Zweck | Outputs |
|----------|-------|---------|
| `00_profiling.ipynb` | Replikation der ZEW-Eckwerte, Konsistenzprüfungen, ID-Stabilität | Konsolen-Ausgaben |
| `01_h1_polyzentrik.ipynb` | HHI, Top-Ressort-Ranking, Profile, BMDS-Szenarien | Konsolen-Ausgaben |
| `02_h2_transfer_vs_aufbau.ipynb` | Hauptgruppen-Drilldown, UG-Aufteilung, Treiber, Robustheit, HG-6-Peak | Konsolen-Ausgaben |
| `03_h4_rebranding.ipynb` | ZEW-Tag-Extraktion, Häufigkeits- und Volumen-Trends, Rebranding-Befund | Konsolen-Ausgaben |
| `04_reden_aufmerksamkeit.ipynb` | H5-Verschneidung ZEW-Daten × CPP-BT-Plenarprotokolle | Konsolen + `outputs/h5_panel.csv` |
| `99_synthese.ipynb` | Zusammenführung der vier Akte, politische Implikation, Limitationen (nicht in ergebnis.qmd eingebettet — Synthese liegt als Prosa im Dokument) | Konsolen-Ausgaben |
| `chart_h1.ipynb` | Hero-Chart Profil-Matrix | `figures/h1_ressort_profile_2024.png/.pdf` |
| `chart_h2.ipynb` | Hero-Chart Schere | `figures/h2_schere.png/.pdf` |
| `chart_h4.ipynb` | Hero-Chart Rebranding | `figures/h4_rebranding.png/.pdf` |
| `chart_anhang_a1.ipynb` | Anhang-Chart HG-6-Drilldown | `figures/anhang_a1_hg6_drilldown.png/.pdf` |
| `chart_h5.ipynb` | Bubble-Chart Akt 4 (Aufmerksamkeit vs. Volumen) | `figures/h5_quadranten.png/.pdf` |

**Konvention.** Notebook-Nummerierung: `0X_*` für Hypothesen-Analyse,
`chart_*` für Visualisierungs-Produktion. Charts laufen erst, wenn die
Hypothesen-Analyse ausgeführt wurde (sie nutzen dieselben Aggregationen).

---

## 5. Konventionen

Diese Konventionen sind in der Studie konsequent durchgehalten und in
`src/load.py` operativ verankert. Abweichungen führen zu Replikations-
Drift gegenüber den ZEW-Eckwerten.

### 5.1 NA-Behandlung

NA in den Geld-Spalten (`digi_soll_eng`, `digi_soll_weit`) und in den
Tag- und Kategorie-Spalten wird als 0 gelesen. Begründung: Die NA-Werte
markieren nicht-digitale Titel — eine 0 ist die mathematisch korrekte
Interpretation eines „kein Beitrag zur Digitalsumme".

Implementation in `load()`:

```python
df[GELD] = df[GELD].fillna(0)
df[TAGS + KATS] = df[TAGS + KATS].fillna(0).astype(int)
```

### 5.2 Primär-Abgrenzung

`digi_soll_eng` ist Primärmaß aller Hauptbefunde. `digi_soll_weit` dient
ausschließlich als Robustheits-Check und wird im Code als solcher
kommentiert. Begründung: konservative, ZEW-konforme Wahl.

### 5.3 Hauptgruppen-Logik

Die `gruppe`-Spalte folgt der Bundeshaushaltsordnung. Erste Ziffer =
Hauptgruppe, erste zwei Ziffern = Obergruppe.

| Hauptgruppe | Bedeutung | Investitions-Typ |
|-------------|-----------|------------------|
| 4 | Personalausgaben | konsumtiv |
| 5 | Sächliche Verwaltungsausgaben | konsumtiv |
| 6 | Zuweisungen und Zuschüsse (laufend) | konsumtiv |
| 7 | Baumaßnahmen | investiv |
| 8 | Sonstige Investitionsausgaben | investiv (siehe Untergruppen) |
| 9 | Besondere Finanzierungsausgaben | global |

Innerhalb der Hauptgruppe 8:

| Obergruppe | Bedeutung | Klassifikation |
|------------|-----------|----------------|
| 81 | Erwerb beweglicher Sachen (Bund-eigen) | A_eigene_Invest |
| 82 | Erwerb unbeweglicher Sachen (Bund-eigen) | A_eigene_Invest |
| 83 | Zuweisungen Länder, öffentlicher Bereich | B_Transfer_Invest |
| 86 | Zuweisungen Sozialversicherungen | B_Transfer_Invest |
| 87 | Investitionsdarlehen an Sonstige | B_Transfer_Invest |
| 88 | Zuschüsse an Sonstige im Inland | B_Transfer_Invest |
| 89 | Investitionszuschüsse Sonstige | B_Transfer_Invest |

Mapping in `src.load.HG_LABEL` und `src.load.UG_INVEST_TYP`.

### 5.4 Anteilige Kategorien-Allokation

Titel mit mehreren markierten Kategorien-Indikatoren werden bei der
Profil-Analyse anteilig aufgeteilt: bei n Kategorien bekommt jede 1/n
des Volumens. Bewusste Setzung, einfach und transparent.

Implementiert in `kategorien_allokation()`.

### 5.5 Trendvergleiche

Bei jedem 2019-vs-2024-Vergleich muss die Filter-Wahl explizit getroffen
werden:

- **Aggregations-Filter** (Default): Aggregation auf `einzelplan`,
  `kapitel` oder `funktion` absorbiert ID-Wechsel innerhalb der
  Aggregationseinheit. Für H1, H2.
- **Panel-Filter**: Nur IDs, die in allen Vergleichsjahren auftauchen.
  Für „stabiler Kern"-Aussagen. Funktion: `panel_titel()`.

Filter-Wahl wird in der Befundtabelle ausgewiesen.

### 5.6 Konsistenzprüfungen beim Laden

- `digi_soll_eng <= digi_soll_weit`: 0 Verletzungen erwartet
- `digi_soll_weit <= soll`: 0 Verletzungen erwartet, sofern `soll >= 0`
- Doppelte `(id, jahr)`: 0 erwartet
- Negative `soll` (Globale Minderausgaben): 121 in EP 60, alle
  nicht-digital

Diese Checks laufen explizit in `00_profiling.ipynb`.

---

## 6. Designsystem für Charts

Implementiert in `src/style.py`. Alle Chart-Notebooks importieren
`apply_style()` und nutzen die definierten Farbkonstanten.

### 6.1 Farbpalette

| Konstante | Hex | Verwendung |
|-----------|-----|-----------|
| `akzent` | `#534AB7` | zentrale Aussage, Primärlinie |
| `akzent_2` | `#1D9E75` | zweite wichtige Reihe, Verwaltungs-Kategorie |
| `neutral` | `#888780` | Vergleich, Hintergrund-Reihe |
| `highlight` | `#D85A30` | Hervorhebung einzelner Datenpunkte |
| `rueckgang` | `#A32D2D` | Verschwinden, fallende Linien |
| `aufstieg` | `#3B6D11` | Wachstum, aufsteigende Linien |
| `text`, `text_secondary`, `text_tertiary` | `#222220`/`#555550`/`#888780` | Texthierarchie |
| `grid` | `#E8E6DD` | Hintergrund-Linien |

Plus `KATEGORIE_FARBEN` mit dedizierten Farben für die 9 ZEW-Kategorien.

### 6.2 Typografie

- Schriftfamilie: Inter → Helvetica Neue → Arial → DejaVu Sans
- Achsen: 10pt
- Titel: 12pt, weight medium
- Beschriftungen direkt am Element: 9pt
- Kernaussage als Untertitel: 11pt, weight medium

### 6.3 Layout

- **Format.** 11×6,3 bis 11×6,8 inches Querformat. PDF vektorbasiert.
- **Spines.** Nur unten und links sichtbar, 0.6pt.
- **Grid.** Nur Y-Achse, sehr dezent in `COLORS['grid']`.
- **Hintergrund.** Hell (`#FAF9F4`), Achsen weiß.
- **Direkte Beschriftung** statt Legenden, wo möglich.
- **Quelle** unten links, klein, kursiv, via `add_quelle()`.
- **Titel** oben links als `fig.text()`, nicht `ax.set_title()`.

### 6.4 Beschriftungs-Konventionen

- Mrd. €-Einheit explizit: `4,12 Mrd. €`
- Prozent mit Leerzeichen: `21,3 %`
- Deutsche Komma-Notation: `8,51` nicht `8.51`
- Tausender-Trennung: `1.612`, `21.358`

### 6.5 Export

Pro Chart: PNG (200 DPI) und PDF (vektor).

```python
fig.savefig(FIGURES_DIR / 'chart_name.png', dpi=200)
fig.savefig(FIGURES_DIR / 'chart_name.pdf')
```

---

## 7. Reproduzierbarkeit

### 7.1 Replikation der ZEW-Eckwerte

| Jahr | Erwartet (Mrd. €) | Replikation | Abweichung |
|------|--------|----|----|
| 2019 | 8,5 | 8,51 | +0,1 % |
| 2021 | 16,6 | 16,55 | −0,3 % |
| 2023 | 19,2 | 19,19 | −0,1 % |
| 2024 | 17,9 | 17,94 | +0,2 % |

Alle Abweichungen unter 0,3 Prozent. Wenn dies plötzlich nicht mehr
trägt, ist die Pipeline gebrochen — vor jedem Commit von neuem
Analyse-Code `00_profiling.ipynb` ausführen.

### 7.2 Reihenfolge der Notebook-Ausführung

1. `00_profiling.ipynb` (Pipeline-Validierung)
2. Die drei Hypothesen-Notebooks (`01_h1`, `02_h2`, `03_h4`) — unabhängig
   voneinander, beliebige Reihenfolge
3. `99_synthese.ipynb` (führt die drei Akte zusammen, baut auf 01–03 auf)
4. Die vier Chart-Notebooks — beliebige Reihenfolge
5. `04_reden_aufmerksamkeit.ipynb` — nur wenn CPP-BT-Korpus unter `data/external/` liegt

### 7.3 Versionierung

- Python 3.11+
- `requirements.txt` listet alle Bibliotheken
- Notebooks im JSON-Format committet, einschließlich Outputs (für
  Reviewer ohne lokale Ausführung)

---

## 8. Externe Datenquellen

### 8.1 Primärquelle

ZEW Mannheim / Agora Digitale Transformation, Digitalhaushalt Open Data
(Stand 2025). Bezug: https://agoradigital.de/projekte/digitalhaushalt

### 8.2 Geplante externe Validierung (Lese-Person)

- IT-Großprojekte-Bericht des Bundes (jährlich, BMI)
- Bundesrechnungshof, Bemerkungen zu IT-Vorhaben
- Bundeshaushaltspläne 2019/2021/2023/2024

### 8.3 H5-Verschneidung (Bundestag-Korpora)

- **CPP-BT** Corpus der Plenarprotokolle des Deutschen Bundestages.
  Sean Fobbe, Zenodo, Public Domain (§ 5 Abs. 2 UrhG). Permanenter
  Link: https://doi.org/10.5281/zenodo.4542661. Aktualisierung
  mehrmals pro Wahlperiode.
- **CDRS-BT** Corpus der Drucksachen des Deutschen Bundestages, derselbe
  Maintainer, Zwillings-Korpus.

Verwendung: nur CSV-Variante, abgelegt unter `data/external/`. Lade-
Pipeline in `04_reden_aufmerksamkeit.ipynb`.

---

## 9. Entwickler-Workflow

### 9.1 Setup

```bash
git clone https://github.com/kalknord/agora_challenge.git digitalhaushalt-challenge
cd digitalhaushalt-challenge
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Datensatz manuell unter data/raw/Digitalhaushalt_Open_Data.xlsx ablegen
jupyter lab notebooks/
```

### 9.2 Neue Analyse hinzufügen

Wenn ein neues Notebook eine Hypothese oder einen Drilldown ergänzt:

1. Datei nach Konvention benennen: `0X_thema.ipynb` für Hypothesen,
   `chart_thema.ipynb` für Charts, `anhang_thema.ipynb` für Anhang-
   Material.
2. Im ersten Code-Block die Standard-Imports einfügen:

   ```python
   import sys
   sys.path.insert(0, '..')  # repo root, relativ zum notebooks/-Verzeichnis
   from src.load import load
   # ggf. weitere Imports aus src
   df = load()  # nutzt Repo-Root-Default
   ```

3. Vor jedem Commit `00_profiling.ipynb` ausführen — Smoke-Test der
   Lade-Pipeline.

### 9.3 Neuer Chart

1. `chart_*.ipynb` anlegen.
2. Designsystem importieren und anwenden:

   ```python
   from src import FIGURES_DIR
   from src.style import apply_style, COLORS, add_quelle
   apply_style()
   ```

3. Export immer als PNG und PDF unter `FIGURES_DIR`.

### 9.4 Pandoc-Build des Essays (ARCHIV)

Das manuelle Pandoc-Kommando ist durch den Quarto-Build abgelöst (§ 9.5).
Als Referenz erhalten:

```bash
pandoc outputs/essay_rohfassung.md \
  -o outputs/essay_rohfassung.pdf \
  --pdf-engine=xelatex \
  -V mainfont="DejaVu Serif" \
  -V geometry:margin=2.5cm \
  --resource-path=.:figures:outputs
```

### 9.5 Ergebnisdokument generieren (Quarto)

Das Hauptdokument `outputs/ergebnis.qmd` zieht Notebook-Outputs via
`{{< embed >}}`-Shortcodes ein. Mit `freeze: auto` werden bereits
ausgeführte Notebook-Outputs verwendet — keine erneute Ausführung bei
jedem Build. Das Quarto-Projekt ist in `_quarto.yml` (Repo-Root)
konfiguriert und gibt `outputs/` als Output-Verzeichnis vor.

```bash
# Einmalig: TinyTeX installieren (falls LaTeX fehlt)
quarto install tinytex

# PDF-Build (Primärformat, aus Repo-Root)
quarto render outputs/ergebnis.qmd --to pdf     # -> outputs/ergebnis.pdf

# HTML-Build (ohne LaTeX, für Vorschau)
quarto render outputs/ergebnis.qmd --to html    # -> outputs/ergebnis.html

# One-Pager
quarto render outputs/one_pager.qmd --to pdf
```

**Cell-Tags in den Notebooks.** Folgende Zellen sind für den Embed getaggt
(Felder `tags`, `label` in cell.metadata, `#| label:` in cell.source):

| Notebook | Zell-Index | Label | Inhalt |
|----------|-----------|-------|--------|
| `notebooks/00_profiling.ipynb` | 8 | `tbl-replikation` | ZEW-Eckwerte-Replikation |
| `notebooks/01_h1_polyzentrik.ipynb` | 5 | `tbl-hhi` | HHI-Tabelle |
| `notebooks/01_h1_polyzentrik.ipynb` | 9 | `tbl-profile` | Top-7-Ressort-Profile 2024 |
| `notebooks/01_h1_polyzentrik.ipynb` | 11 | `tbl-szenarien` | BMDS-Bündelungs-Szenarien |
| `notebooks/02_h2_transfer_vs_aufbau.ipynb` | 7 | `tbl-schere` | Eigene vs. Transfer-Invest. |
| `notebooks/02_h2_transfer_vs_aufbau.ipynb` | 9 | `tbl-treiber` | Top-Treiber Transfer-Boom |
| `notebooks/03_h4_rebranding.ipynb` | 12 | `tbl-rebranding` | Rebranding-Befund |
| `notebooks/chart_h5.ipynb` | 3 | `tbl-h5-panel` | H5-Panel (Daten aus h5_panel.csv) |
| `notebooks/chart_h5.ipynb` | 5 | `fig-h5-quadranten` | Bubble-Chart Aufmerksamkeit/Volumen |

Akt 4 (`ergebnis.qmd` §sec-akt4) nutzt für den Chart eine statische
Figur-Referenz (`../figures/h5_quadranten.pdf/png`), nicht einen
`{{< embed >}}`-Shortcode.

### 9.6 Tests

Es gibt keine Unit-Tests im klassischen Sinne. Die Validierung läuft
über die Replikation der ZEW-Eckwerte in `00_profiling.ipynb`. Vor
jedem Pull Request:

1. Alle Notebooks ausführen: `jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb`
2. Profiling-Output sichten: Replikation muss innerhalb 0,3 % Abweichung
   bleiben
3. Charts-Output sichten: PNGs in `figures/` müssen aktuell sein
4. HTML-Build prüfen: `quarto render outputs/ergebnis.qmd --to html`
