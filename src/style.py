"""Zentrales Design-System fuer alle Hero-Charts der Studie.

Eine matplotlib-Style-Funktion und ein Farbsystem. Alle Charts importieren
hier - so bleibt das visuelle Erscheinungsbild konsistent.

Verwendung:

    from src.style import apply_style, COLORS, KATEGORIE_FARBEN
    apply_style()
"""
import matplotlib as mpl
import matplotlib.pyplot as plt

# Basisfarben
COLORS = {
    'akzent': '#534AB7',       # zentrale Aussage
    'akzent_2': '#1D9E75',     # zweite wichtige Linie/Kategorie
    'neutral': '#888780',      # Vergleichswerte, Hintergrund-Serien
    'highlight': '#D85A30',    # Hervorhebung einzelner Datenpunkte
    'rueckgang': '#A32D2D',    # rote Note (Rueckgang, Verschwinden)
    'aufstieg': '#3B6D11',     # gruene Note (Wachstum, Auftauchen)
    'text': '#222220',
    'text_secondary': '#555550',
    'text_tertiary': '#888780',
    'grid': '#E8E6DD',
    'background': '#FAF9F4',
}

# Profilfarben fuer die 9 Kategorien (H1)
KATEGORIE_FARBEN = {
    'Infrastruktur': '#534AB7',
    'Wirtschaft':    '#BA7517',
    'Verwaltung':    '#1D9E75',
    'Kompetenzen':   '#D4537E',
    'Kultur':        '#9B7BB8',
    'Forschung':     '#D85A30',
    'Gesundheit':    '#3B8FA5',
    'Bundeswehr':    '#444441',
    'Unteilbar':     '#B4B2A9',
}

# Ressort-Kuerzel fuer Achsenbeschriftung
RESSORT_KURZ = {
    4: 'BPA', 5: 'AA', 6: 'BMI', 7: 'BMJ', 8: 'BMF', 9: 'BMWK',
    10: 'BMEL', 11: 'BMAS', 12: 'BMDV', 14: 'BMVg', 15: 'BMG',
    16: 'BMUV', 17: 'BMFSFJ', 23: 'BMZ', 25: 'BMWSB', 30: 'BMBF',
    60: 'AllgFin',
}


def apply_style():
    """Wendet das hauseigene Designsystem auf matplotlib an."""
    plt.rcParams.update({
        # Schrift
        'font.family': 'sans-serif',
        'font.sans-serif': ['Inter', 'Helvetica Neue', 'Arial', 'DejaVu Sans'],
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.titleweight': 'medium',
        'axes.labelsize': 10,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 13,

        # Farben und Linien
        'axes.edgecolor': COLORS['text_secondary'],
        'axes.linewidth': 0.6,
        'axes.labelcolor': COLORS['text'],
        'xtick.color': COLORS['text_secondary'],
        'ytick.color': COLORS['text_secondary'],
        'text.color': COLORS['text'],

        # Hintergrund und Grid
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.grid': True,
        'grid.color': COLORS['grid'],
        'grid.linewidth': 0.6,
        'grid.alpha': 1.0,
        'axes.grid.axis': 'y',

        # Spines: nur unten, links
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': True,
        'axes.spines.bottom': True,

        # Ticks: nur an Achse, keine Strichelung
        'xtick.major.size': 0,
        'ytick.major.size': 0,
        'xtick.major.pad': 6,
        'ytick.major.pad': 4,

        # Speichern
        'savefig.dpi': 200,
        'savefig.bbox': 'tight',
        'savefig.facecolor': 'white',
        'pdf.fonttype': 42,  # Editable in vector tools
        'svg.fonttype': 'none',
    })


def add_quelle(ax, text='Quelle: Digitalhaushalt Open Data (ZEW/Agora), eigene Berechnung'):
    """Quellen- und Methodennotiz unten links."""
    ax.figure.text(
        0.02, 0.02, text,
        fontsize=8, color=COLORS['text_tertiary'], style='italic',
    )


def kernaussage(ax, text, x=0.02, y=0.93):
    """Kernaussage als Titel-Untertitel ueber dem Chart."""
    ax.figure.text(
        x, y, text,
        fontsize=11, color=COLORS['text'], weight='medium',
    )
