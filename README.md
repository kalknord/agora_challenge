# Was kann ein BMDS steuern?

Eine datenbasierte Vermessung des Digitalhaushalts 2019–2024.

Beitrag zur Daten-Challenge Digitalhaushalt der Agora Digitale
Transformation (Datenpartner ZEW Mannheim). Kategorie: Beste
Erkenntnisse, mit visueller Begleitung.

## Worum es geht

Mit der Gründung des Bundesministeriums für Digitales und
Staatsmodernisierung (BMDS) im Jahr 2025 ist die Frage zurück auf der
politischen Agenda, ob und wie der deutsche Digitalhaushalt zentral
steuerbar ist. Wir nutzen die erstmals öffentlich verfügbaren Daten von
ZEW und Agora und vermessen drei Dinge: wo das Digital-Geld tatsächlich
liegt, was damit gemacht wird, und wie sich die politische Sprache um
den Digitalhaushalt verschiebt.

**Kernbefund.** Eine zentrale Steuerung durch das BMDS ist auf 21 bis
23 Prozent des Digital-Solls begrenzt. Der Bund baut zudem nicht selbst
auf, sondern verteilt zunehmend Investitionsmittel an Länder und
Private. Das limitiert auch ein BMDS strukturell auf eine Koordinations-
und Förder-Rolle.

## Story-Arc

**Akt 1 - Wo liegt das Geld?** Der Digitalhaushalt ist polyzentrisch
über sechs Ressorts mit fundamental verschiedenen Aufgaben-Profilen
verteilt. HHI 1.612 (2024), Top-Ressort 23 Prozent. Bei realistischer
Bündelung kann ein BMDS 21 bis 23 Prozent des Digital-Solls zentral
steuern.

**Akt 2 - Was passiert mit dem Geld?** Eigene Bundes-Investitionen
stagnieren absolut und schrumpfen anteilig von 10,9 auf 6,0 Prozent.
Investitions-Zuschüsse an Länder und Private verdoppeln ihren Anteil
von 15,9 auf 31,8 Prozent. Der Bund verteilt zunehmend, baut nicht
selbst.

**Akt 3 - Wie wird darüber geredet?** Politisches Rebranding statt
Buzzword-Inflation. Die Hightech-Strategie der Merkel-Ära verschwindet
vollständig, ersetzt durch die Zukunftsstrategie der Ampel-Regierung,
gleicher Inhalt, neues Label, höheres Volumen.

**Politische Implikation.** Ein Digitalbudget muss zwei Bewegungen
unterscheiden, die im aktuellen Diskurs vermischt werden: zentrale
Klassifikations- und Transparenzhoheit (machbar) und operative
Steuerungshoheit über die Mittel (sehr begrenzt machbar). Wer beides
verspricht, verspricht zu viel.

## Schnellstart

```bash
git clone https://github.com/kalknord/agora_challenge.git digitalhaushalt-challenge
cd digitalhaushalt-challenge
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Datensatz von https://agoradigital.de/projekte/digitalhaushalt
# herunterladen und unter data/raw/Digitalhaushalt_Open_Data.xlsx ablegen
jupyter lab notebooks/
```

Empfohlene Reihenfolge:

1. `notebooks/00_profiling.ipynb` - Replikation der ZEW-Eckwerte
2. `notebooks/01_h1_polyzentrik.ipynb` - Akt 1
3. `notebooks/02_h2_transfer_vs_aufbau.ipynb` - Akt 2
4. `notebooks/03_h4_rebranding.ipynb` - Akt 3
5. `notebooks/99_synthese.ipynb` - Zusammenführung und politische Implikation
6. `notebooks/chart_*.ipynb` - Hero-Charts und Anhang-Chart

**Ergebnisdokument generieren** (Quarto ≥ 1.4 und LaTeX/TinyTeX erforderlich):

```bash
# TinyTeX einmalig installieren (falls LaTeX fehlt)
quarto install tinytex

# Aus dem Repo-Root:
quarto render outputs/ergebnis.qmd --to pdf    # -> outputs/ergebnis.pdf
quarto render outputs/ergebnis.qmd --to html   # -> outputs/ergebnis.html (ohne LaTeX)
```

## Wo finde ich was?

| Wofür | Wo |
|-------|-----|
| Technische Doku, Repo-Aufbau, src-API, Konventionen | `DOC.md` |
| Inhaltliche Analyse | `notebooks/` |
| Library-Code | `src/` |
| Generierte Charts | `figures/` |
| Essay-Manuskript, Pitch, Brief | `outputs/` |
| **Ergebnisdokument (Quarto-Quelle)** | **`outputs/ergebnis.qmd`** (→ `outputs/ergebnis.pdf`) |

## Datenquellen

- **Primärdaten:** Digitalhaushalt Open Data (ZEW/Agora), Stand 2025.
  https://agoradigital.de/projekte/digitalhaushalt
- **Externe Validierung (geplant):** IT-Großprojekte-Bericht des Bundes,
  Bundesrechnungshof-Bemerkungen, Bundeshaushaltspläne 2019/2021/2023/2024
- **H5-Verschneidung:** Bundestag-Korpora CPP-BT und CDRS-BT
  (Sean Fobbe, Zenodo, Public Domain)

## Team

Finn Kegel, Jannis Köhler und Moritz Hammes aus dem berufsbegleitenden Master „Digitale Transformation",
HWR Berlin. Beitrag zur Agora-Daten-Challenge.
