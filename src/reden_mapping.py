"""Mapping fuer die Reden-Verschneidung (Hypothese H5).

Stellt das Vokabular und Ressort-Mapping bereit, damit die Reden-Analyse mit der ZEW-Klassifikation kompatibel
bleibt.

Verwendung:
    from src.reden_mapping import RESSORT_BEGRIFFE, DIGITAL_BEGRIFFE
"""

# Digitale Schlagwoerter, abgeleitet aus den ZEW-Tags in titel_text
# (die wir in H4 bereits analysiert haben). Reine Lowercase-Begriffe,
# wir wenden sie ueber re.findall(r'\bbegriff\b', text, re.IGNORECASE) an.
DIGITAL_BEGRIFFE = [
    # Querschnitt
    'digital', 'digitalisierung', 'digitale',
    # Schluesseltechnologien
    'informationstechnik', 'software', 'plattform',
    'kuenstliche intelligenz', 'ki ', ' ki,', ' ki.',  # KI mit Wortgrenzen
    'algorithm', 'cloud', 'cyber', 'quanten',
    'mikroelektronik', 'halbleiter',
    # Politik-Etiketten
    'hightech-strategie', 'zukunftsstrategie', 'digitalstrategie',
    'digitalbudget', 'digitalministerium',
    # Infrastrukturen
    'breitband', 'glasfaser', '5g', 'mobilfunk',
    # Verwaltung
    'onlinezugangsgesetz', 'ozg', 'verwaltungsdigitalisierung',
    'e-government', 'egovernment', 'digitalfunk',
    'itzbund', 'bundescloud',
    # Bildung und Kompetenzen
    'digitalpakt', 'digitale bildung', 'medienkompetenz',
    # Souveraenitaet
    'digitale souveraenitaet', 'open source',
]

# Ressort-typische Begriffe (Sachthemen, die das Mapping ermoeglichen)
# Wir nutzen Begriffe, die in Drucksachen typischerweise auftauchen,
# wenn das Thema dieses Ressorts angesprochen wird.
RESSORT_BEGRIFFE = {
    # EP 06 BMI - Inneres, Verwaltung, BSI
    'BMI': [
        'bundesministerium des innern', 'innenministerium',
        'bsi', 'bundesamt fuer sicherheit', 'cyber-sicherheit',
        'cybersicherheit', 'digitalfunk', 'verwaltungsdigitalisierung',
        'onlinezugangsgesetz', 'ozg',
    ],
    # EP 08 BMF - Finanzen, Zoll, ITZBund
    'BMF': [
        'bundesministerium der finanzen', 'finanzministerium',
        'zoll', 'zollverwaltung', 'itzbund', 'steuerverwaltung',
    ],
    # EP 09 BMWK - Wirtschaft, Foerderprogramme
    'BMWK': [
        'bundesministerium fuer wirtschaft', 'wirtschaftsministerium',
        'zim ', 'mittelstandsfoerderung', 'innovationsfoerderung',
        'wirtschaftsfoerderung',
    ],
    # EP 12 BMDV (vormals BMVI) - Verkehr, digitale Infrastruktur
    'BMDV': [
        'bundesministerium fuer digitales und verkehr',
        'bundesministerium fuer verkehr',
        'verkehrsministerium', 'breitbandausbau', 'breitbandfoerderung',
        'glasfaserausbau', 'mobilfunkversorgung', '5g-ausbau',
        'etcs', 'schienenwege', 'bundesfernstrassen',
    ],
    # EP 14 BMVg - Verteidigung, Bundeswehr-IT
    'BMVg': [
        'bundesministerium der verteidigung', 'verteidigungsministerium',
        'bundeswehr', 'cyberkommando', 'cir-truppe', 'bwi ',
    ],
    # EP 15 BMG - Gesundheit, Telematikinfrastruktur
    'BMG': [
        'bundesministerium fuer gesundheit', 'gesundheitsministerium',
        'gematik', 'telematikinfrastruktur', 'elektronische patientenakte',
        'epa', 'e-rezept', 'digitale gesundheits-anwendungen', 'diga',
    ],
    # EP 30 BMBF - Bildung, Forschung
    'BMBF': [
        'bundesministerium fuer bildung und forschung',
        'bildungsministerium', 'forschungsministerium',
        'digitalpakt', 'digitalpakt schule', 'bildungsplattform',
        'forschungsfoerderung', 'hochschuldigitalisierung',
    ],
    # EP 60 Allgemeine Finanzverwaltung - Industriepolitik
    'EP60': [
        'allgemeine finanzverwaltung', 'chips-act', 'eu-chips',
        'intel magdeburg', 'esmc dresden', 'mikroelektronik-foerderung',
    ],
}

# Mapping Ressort-Kuerzel <-> Einzelplan-Nummer
RESSORT_TO_EP = {
    'BMI': 6, 'BMF': 8, 'BMWK': 9, 'BMDV': 12, 'BMVg': 14,
    'BMG': 15, 'BMBF': 30, 'EP60': 60,
}

EP_TO_RESSORT = {v: k for k, v in RESSORT_TO_EP.items()}
