# METHODOLOGY

Methodische Entscheidungen, Abgrenzungen und Limitationen der Studie.
Lesegeraete fuer die Befunde, nicht nur Anhang.

## 1. Datenbasis

Primaerdatensatz: `Digitalhaushalt_Open_Data.xlsx` (ZEW/Agora, Stand 2025).
Aufbau:

- 21.358 Beobachtungen (Haushaltstitel x Jahr) ueber 6.240 unique Titel-IDs
- Jahre 2019, 2021, 2023, 2024 - keine durchgaengige Jahresreihe
- 25 Spalten: drei Geldspalten (in Tsd. Euro), neun Kategorie-Indikatoren,
  vier Detektions-Tags, sieben Strukturfelder, zwei IDs
- Quelle: https://agoradigital.de/projekte/digitalhaushalt

## 2. Replikation der ZEW-Eckwerte

Aggregierte `digi_soll_eng`-Summen unserer Lade-Pipeline gegen die in der
ZEW-Studie publizierten Werte (Mrd. Euro):

| Jahr | Erwartet | Replikation | Abweichung |
|------|----------|-------------|------------|
| 2019 | 8,5      | 8,51        | +0,1 %     |
| 2021 | 16,6     | 16,55       | -0,3 %     |
| 2023 | 19,2     | 19,19       | -0,1 %     |
| 2024 | 17,9     | 17,94       | +0,2 %     |

Alle Abweichungen unter 0,3 Prozent. Die Pipeline kann als valide gelten.

## 3. Konventionen fuer NA und Konsistenz

**NA-Logik.** Nicht-digitale Titel haben systematisch NA in den drei
Geld-Digitalspalten und in den neun Kategorie-Indikatoren. Wir lesen NA in
diesen Spalten konsequent als 0 - das ist die haushaltsoekonomisch korrekte
Interpretation (kein Beitrag) und macht Aggregationen verlustfrei.
Implementation in `src/load.py`.

**Konsistenzpruefung.** Beim Laden geprueft:
- `digi_soll_eng <= digi_soll_weit`: 0 Verletzungen
- `digi_soll_weit <= soll`: 0 Verletzungen
- Doppelte (id, jahr): 0
- Negative `soll`: 121 Titel (Globale Minderausgaben in Einzelplan 60,
  haushaltsrechtlich zulaessig, alle nicht-digital - fuer unsere Analyse
  irrelevant)

## 4. Eng- und Weit-Abgrenzung

Der ZEW-Datensatz unterscheidet zwei Detektions-Strenge:

- `digi_soll_eng`: konservativ - nur Titel mit eindeutig digitalem Zweck
- `digi_soll_weit`: einschliesslich Mischausgaben mit digitalem Anteil

Wir verwenden `digi_soll_eng` als Primaer-Mass aller Befunde. `digi_soll_weit`
dient ausschliesslich als Robustheitscheck. Diese Wahl folgt der ZEW-Logik
und ist konservativ: Wenn ein Befund nur in der weiten Abgrenzung trueggt,
verzichten wir auf ihn.

Die Eng-Weit-Spreizung des Gesamthaushalts sinkt ueber die Jahre (11,7 % ->
7,0 % -> 6,6 % -> 6,0 %), was wir als wachsende sprachliche Eindeutigkeit
digitaler Titel interpretieren.

## 5. Panel- vs. Aggregations-Filter bei Trendvergleichen

Von 6.240 Titel-IDs erscheinen 4.449 (71 %) in allen vier Jahren, 531 IDs
nur in einem einzigen Jahr. Diese ID-Fluktuation kann Trendvergleiche
verzerren.

Wir verwenden zwei Filter je nach Frage:

- **Aggregations-Filter** (Default): Aggregation auf `einzelplan`, `kapitel`
  oder `funktion` absorbiert ID-Wechsel innerhalb der Aggregations-Einheit.
  Verwendet fuer H1 (Polyzentrik), H2 (Hauptgruppen-Trends).
- **Panel-Filter**: Nur IDs in allen Vergleichsjahren. Verwendet, wo wir
  Aussagen ueber den "stabilen Kern" des Digitalhaushalts treffen
  (z. B. HG-6-Robustheitscheck).

Filterwahl wird in jeder Befundtabelle explizit ausgewiesen.

## 6. Hauptgruppen-Mapping (H2)

Bundeshaushaltsordnung-Logik, erste Ziffer der `gruppe`:

- HG 4-6: Konsumtive Ausgaben (Personal, sachlich, laufende Zuweisungen)
- HG 7-8: Investive Ausgaben (Bau, sonstige Investitionen)
- HG 9: Besondere Finanzierungsausgaben (Globalansaetze)

Investiv weiter aufgeteilt nach Obergruppe (erste zwei Ziffern):

- UG 81/82: A_eigene_Invest (Bund selbst beschafft)
- UG 83/86/87/88/89: B_Transfer_Invest (Bund foerdert Dritte)

Mapping in `src/load.py`, `UG_INVEST_TYP`.

## 7. Anteilige Kategorien-Allokation (H1)

Viele Titel haben mehrere Kategorie-Indikatoren gleichzeitig markiert
(z. B. ein Bildungs-Forschungs-Titel: `_4_dig_kompetenzen=1`,
`_6_forschung_inno=1`). Fuer Profil-Analysen muss das Volumen aufgeteilt
werden.

Vereinfachung: Wenn n Kategorien markiert sind, erhaelt jede Kategorie
1/n des Titelvolumens. Diese Gleichverteilung ist eine bewusste, einfache
Wahl - alternative gewichtete Allokationen (z. B. nach `digi_klasse`) waeren
moeglich, fuegen aber zusaetzliche Annahmen ein, die in der ZEW-Studie nicht
hinterlegt sind. Implementiert in `src/load.py`, `kategorien_allokation()`.

## 8. Konzentrationsmass HHI (H1)

Herfindahl-Hirschman-Index ueber Einzelplaene, Skala 0-10.000.

- Unter 1.500: fragmentiert
- 1.500-2.500: maessig konzentriert
- Ueber 2.500: stark konzentriert

Berechnung in `src/load.py`, `hhi()`. Wir berichten HHI je Jahr und im
Zeitvergleich.

## 9. Schlagwort-Extraktion (H4)

Der `titel_text` enthaelt vom ZEW vormarkierte Schlagworte in eckigen
Klammern `[...]`, optional mit Sub-Markern in geschweiften Klammern
`{...}`. Wir extrahieren die eckigen Marker per Regex,
normalisieren (lowercase, Whitespace) und zaehlen Treffer- und
Volumen-Trends je Schlagwort.

Wir verzichten bewusst auf zusaetzliche eigene Begriffslisten, weil die
ZEW-Markierung die nachvollziehbare Datenbasis ist. Eigene Begriffsuchen im
Fliesstext haben wir explorativ getestet, ergeben aber Verzerrungen durch
Komposita und Schreibvarianten.

## 10. Limitationen

**Soll, nicht Ist.** Alle Geldspalten sind Haushalts-Sollwerte, nicht
tatsaechliche Auszahlungen. Bekannt ist, dass Digital-Mittel haeufig nicht
ausgeschoepft werden. Eine Soll-Ist-Analyse wuerde Haushaltsrechnungs-Daten
benoetigen, die in maschinenlesbarer Form nicht vollstaendig vorliegen.

**Verpflichtungsermaechtigungen verzerren Soll-Jahresreihen.** Eine
mehrjaehrige Foerderzusage erscheint im Bewilligungs-Jahr als hoher
Sollansatz, in Folgejahren als Null - ohne dass die Politik gestoppt
wurde. Konkretes Beispiel: 2,74 Mrd. Euro Mikroelektronik-Foerderung
in EP 60 (Gruppe 686) erscheinen 2023 und verschwinden 2024 vollstaendig.
Sieben der acht groessten HG-6-Rueckgaenge 2023-2024 enthalten das Wort
"Verpflichtungsermaechtigung" im Titeltext.

Wir behandeln das auf drei Wegen:
- Soll-Sprunghaftigkeit wird in Trendgrafiken explizit benannt
- Wo moeglich, Panel-stabile Titel als Robustheitscheck
- VE-Hinweis im Methoden-Anhang (dieser Abschnitt)

**Klassifikation Mikroelektronik = digital.** Die ZEW-Klassifikation
ordnet die Chips-Act-Foerderung dem Digitalhaushalt zu. Das ist eine
politische Setzung, ueber die man streiten kann - die zugrundeliegende
Foerderung dient Industriepolitik, nicht primaer digitaler Transformation.
Wir uebernehmen die ZEW-Klassifikation, weisen aber im Spin-off-Befund zu
EP 60 darauf hin.

**Drei Jahres-Luecken.** Die Jahre 2020 und 2022 fehlen im Datensatz.
Das limitiert Aussagen ueber Krisen- und Konjunkturreaktionen
(Corona 2020/2021, Energiekrise 2022). Wir beschraenken uns auf
2019-2024-Strukturvergleiche.

**Politische Aktualitaet 2025+.** Der Datensatz endet 2024. BMDS-Gruendung,
neue Koalition und Sondervermoegen-Effekte fallen ausserhalb. Wir
projizieren die strukturellen Befunde auf die laufende Debatte, ohne sie
empirisch in die Zukunft zu verlaengern.

## 11. Reproduzierbarkeit

Alle Analyseschritte sind als Python-Skripte in `notebooks/` abgelegt und
nutzen die zentralen Funktionen aus `src/load.py`. Mit `requirements.txt`
und dem Datensatz unter `data/raw/` sind alle Tabellen und Charts der
Studie reproduzierbar.

Versionierung: Geschrieben gegen Python 3.11, pandas 2.x, openpyxl. Keine
exotischen Abhaengigkeiten.
