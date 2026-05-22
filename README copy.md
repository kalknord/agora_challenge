# Was kann ein BMDS steuern? Eine datenbasierte Vermessung des Digitalhaushalts 2019-2024

Beitrag zur Daten-Challenge Digitalhaushalt der Agora Digitale Transformation
(Datenpartner ZEW Mannheim), Kategorie: Beste Erkenntnisse (mit visueller
Begleitung).

## Worum es geht

Mit der Gruendung des Bundesministeriums fuer Digitales und Staatsmodernisierung
(BMDS) im Jahr 2025 ist die Frage zurueck auf der politischen Agenda, ob
und wie der deutsche Digitalhaushalt zentral steuerbar ist. Wir nehmen die
erstmals oeffentlich verfuegbaren Daten von ZEW und Agora und vermessen
drei Dinge: wo das Digital-Geld tatsaechlich liegt (Akt 1, Hypothese H1),
was damit gemacht wird (Akt 2, Hypothese H2) und wie sich die politische
Sprache um den Digitalhaushalt verschiebt (Akt 3, Hypothese H4).

Kernbefund: Eine zentrale Steuerung durch das BMDS ist auf 21 bis 23 Prozent
des Digital-Solls begrenzt. Der Bund baut zudem nicht selbst auf, sondern
verteilt zunehmend Investitionsmittel an Laender und Private. Das limitiert
auch ein BMDS strukturell auf eine Koordinations- und Foerder-Rolle.

## Schnellstart

```bash
git clone <repo-url> digitalhaushalt-challenge
cd digitalhaushalt-challenge
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Datensatz von https://agoradigital.de/projekte/digitalhaushalt herunterladen
# und unter data/raw/Digitalhaushalt_Open_Data.xlsx ablegen
jupyter lab notebooks/
```

## Repo-Struktur

```
.
|-- README.md                  Dieses Dokument
|-- METHODOLOGY.md             Datenbasis, Abgrenzungen, Aggregationen, Limits
|-- requirements.txt
|-- src/                       Lade- und Analysetools (importiert aus Notebooks)
|   |-- __init__.py
|   `-- load.py
|-- notebooks/                 Eine Analyseschiene pro Datei
|   |-- 00_profiling.py          Replikation der ZEW-Eckwerte, Konsistenzchecks
|   |-- 01_h1_polyzentrik.py     Wo liegt das Geld? Konzentration + Profile
|   |-- 02_h2_transfer_vs_aufbau.py  Was passiert damit? HG/UG-Drilldown
|   `-- 03_h4_rebranding.py      Wie wird darueber geredet? ZEW-Tags ueber Zeit
|-- data/raw/                  Datensatz manuell ablegen (nicht im Repo)
|-- figures/                   Generierte Charts
|-- docs/                      Story-Arc, Lese-Tabelle, Phase-2-Befunde
`-- outputs/                   Essay-PDF, Pitch-Deck, Policy-Brief
```

## Story-Arc (Kurzfassung)

**Leitfrage.** Was kann das BMDS tatsaechlich steuern, was nicht?

**Akt 1 - Wo liegt das Geld? (H1).** Der Digitalhaushalt ist polyzentrisch
ueber sechs Ressorts mit fundamental verschiedenen Aufgaben-Profilen verteilt.
HHI 1.612 (2024), Top-Ressort 23 Prozent. Bei realistischer Buendelung kann
ein BMDS 21 bis 23 Prozent des Digital-Solls zentral steuern - der Rest ist
ressortgebunden (Bundeswehr, Forschung, Verkehrsinfrastruktur, Industrie).

**Akt 2 - Was passiert damit? (H2).** Eigene Bundes-Investitionen stagnieren
absolut und schrumpfen anteilig von 10,9 auf 6,0 Prozent. Investitions-
Zuschuesse an Laender und Private verdoppeln ihren Anteil von 15,9 auf 31,8
Prozent. Der Bund verteilt zunehmend, baut nicht selbst.

**Akt 3 - Wie wird darueber geredet? (H4 + Spin-offs).** Politisches
Rebranding: Die Hightech-Strategie der Merkel-Aera verschwindet vollstaendig,
ersetzt durch die Zukunftsstrategie der Ampel-Regierung - gleicher Inhalt,
neues Label, hoeheres Volumen. Industriepolitik laeuft ueber EP 60
(Allgemeine Finanzverwaltung) als Schatten-Foerderkanal.

**Implikation.** Ein Digitalbudget muss zwei Bewegungen unterscheiden, die
im politischen Diskurs derzeit vermischt werden: zentrale Klassifikations-
und Transparenzhoheit (machbar) und operative Steuerungshoheit ueber die
Mittel (nur sehr begrenzt machbar).

## Datenquellen

- **Primaerdaten:** Digitalhaushalt Open Data (ZEW/Agora), Stand 2025.
  https://agoradigital.de/projekte/digitalhaushalt
- **Externe Validierung (Auswahl):**
  - IT-Grossprojekte-Bericht des Bundes (jaehrlich, BMI)
  - Bundesrechnungshof, Bemerkungen zu IT-Vorhaben
  - Bundeshaushaltsplaene 2019, 2021, 2023, 2024
- **Kontext-Dokumente:**
  - ZEW/Agora-Studie zum Digitalhaushalt 2025
  - Policy Paper "Vom Digitalhaushalt zum Digitalbudget"

## Lizenzen

- **Code** (alles in `src/` und `notebooks/`): MIT, siehe `LICENSE-CODE`.
- **Inhalte** (alles in `docs/`, `figures/`, `outputs/`, sowie die README und
  METHODOLOGY): Creative Commons BY 4.0, siehe `LICENSE-CONTENT`.
- **Primaerdaten** (`data/raw/`) werden NICHT in diesem Repo redistribuiert.
  Lizenz beim Datenanbieter pruefen (https://agoradigital.de).

## Team und Kontakt

Studierende im Masterstudiengang Digitale Transformation, HWR Berlin.
Beitrag zur Agora-Daten-Challenge 2026.
