"""
AfterCare — STI trend charts
Generates chart-sti-general.png and chart-sti-msm.png from ECDC surveillance data.

Requirements:
    pip install matplotlib

Data source:
    ECDC surveillance atlas — https://www.ecdc.europa.eu/en/surveillance-atlas-infectious-diseases
    Download confirmed-case CSVs for Gonorrhoea, Syphilis, and Chlamydia infection
    (both "Confirmed cases" and "Men who have sex with men" populations).
    Place them in DATA_DIR below.

Fonts:
    Poppins-Regular.ttf and Poppins-SemiBold.ttf must be present in FONT_DIR.
    Download from https://fonts.google.com/specimen/Poppins (OFL licence).

Usage:
    python generate-charts.py
    Output files are written next to this script.
"""

import os
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ── paths ─────────────────────────────────────────────────────────────────────
HERE     = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, 'ecdc-sti')
FONT_DIR = os.path.join(HERE, 'fonts')

FONT_REG = os.path.join(FONT_DIR, 'Poppins-Regular.ttf')
FONT_SB  = os.path.join(FONT_DIR, 'Poppins-SemiBold.ttf')

fm.fontManager.addfont(FONT_REG)
fm.fontManager.addfont(FONT_SB)
POPPINS    = fm.FontProperties(fname=FONT_REG)
POPPINS_SB = fm.FontProperties(fname=FONT_SB)

# ── data files ────────────────────────────────────────────────────────────────
FILES = {
    'gon_gen': 'Gonorrhoea - Confirmed cases - Reported cases.csv',
    'gon_msm': 'Gonorrhoea - Disease surveillance|Confirmed cases - Men who have sex with men - Reported cases.csv',
    'syp_gen': 'Syphilis - Confirmed cases - Reported cases.csv',
    'syp_msm': 'Syphilis - Confirmed cases - Men who have sex with men - Reported cases.csv',
    'chl_gen': 'Chlamydia infection - Confirmed cases - Reported cases.csv',
    'chl_msm': 'Chlamydia infection - Confirmed cases - Men who have sex with men - Reported cases.csv',
}

# ── palette (matches website CSS tokens) ──────────────────────────────────────
BG    = '#0a0a10'
BG2   = '#0f0f17'
WHITE = '#f4f4f6'
TEAL  = '#2dd4bf'
BLUE  = '#60a5fa'
GRAY  = '#9ca3af'
GRID  = '#1a1a28'

SOURCE = 'Source: European Centre for Disease Prevention and Control'
REGION = 'EUEEA30_21'
YEARS  = list(range(2015, 2025))


def load(key, region=REGION, year_range=range(2015, 2025)):
    data = {}
    path = os.path.join(DATA_DIR, FILES[key])
    with open(path) as f:
        for row in csv.DictReader(f):
            if row['RegionCode'] == region and int(row['Time']) in year_range:
                try:
                    data[int(row['Time'])] = float(row['NumValue']) / 1000
                except ValueError:
                    pass
    return data


def vals(d):
    return [d.get(y) for y in YEARS]


def style_ax(ax):
    ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis='both', which='both', length=0, colors=GRAY)
    ax.set_xticks(YEARS)
    ax.set_xticklabels([str(y) for y in YEARS],
                       fontproperties=POPPINS, fontsize=8.5, color=GRAY)
    for lbl in ax.get_yticklabels():
        lbl.set_fontproperties(POPPINS)
        lbl.set_color(GRAY)
    ax.set_xlim(2014.5, 2024.5)
    ax.set_ylim(bottom=0)
    ax.set_ylabel('')


def make_fig(title, subtitle):
    fig, ax = plt.subplots(figsize=(6.6, 4.2), dpi=160)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG2)
    fig.text(0.065, 0.97, title,
             fontproperties=POPPINS_SB, fontsize=13, color=WHITE, va='top', ha='left')
    fig.text(0.065, 0.90, subtitle,
             fontproperties=POPPINS, fontsize=9, color=GRAY, va='top', ha='left')
    fig.text(0.065, 0.025, SOURCE,
             fontproperties=POPPINS, fontsize=8, color=GRAY, va='bottom', ha='left')
    return fig, ax


def finish(fig, ax, filename, ncol=3):
    ax.legend(loc='upper left', frameon=False, prop=POPPINS, fontsize=9.5,
              labelcolor=GRAY, ncol=ncol, columnspacing=1.2,
              handlelength=1.8, handletextpad=0.5)
    plt.subplots_adjust(left=0.07, right=0.97, top=0.82, bottom=0.13)
    out = os.path.join(HERE, '..', 'visual-assets', filename)
    fig.savefig(out, dpi=160, facecolor=BG)
    plt.close()
    print('saved', out)


LW = dict(lw=2.0, ms=3.5, mew=0)


# ── Chart 1: general population ───────────────────────────────────────────────
gon_gen = load('gon_gen')
syp_gen = load('syp_gen')
chl_gen = load('chl_gen')

fig, ax = make_fig(
    'Bacterial STIs at record highs in Europe',
    'Confirmed cases, EU/EEA, thousands',
)
ax.plot(YEARS, vals(gon_gen), color=WHITE, marker='o', label='Gonorrhoea', **LW)
ax.plot(YEARS, vals(syp_gen), color=TEAL,  marker='o', label='Syphilis',   **LW)
ax.plot(YEARS, vals(chl_gen), color=BLUE,  marker='o', label='Chlamydia',
        linestyle='dashed', **LW)
style_ax(ax)
finish(fig, ax, 'chart-sti-general.png')


# ── Chart 2: MSM ──────────────────────────────────────────────────────────────
gon_msm = load('gon_msm')
syp_msm = load('syp_msm')
chl_msm = load('chl_msm')

chl_years = [y for y in YEARS if chl_msm.get(y) is not None]
chl_vals  = [chl_msm[y] for y in chl_years]

fig, ax = make_fig(
    'Chlamydia and gonorrhoea are rising faster among MSM',
    'Confirmed cases among men who have sex with men, EU/EEA, thousands',
)
ax.plot(YEARS,     vals(gon_msm), color=WHITE, marker='o', label='Gonorrhoea', **LW)
ax.plot(YEARS,     vals(syp_msm), color=TEAL,  marker='o', label='Syphilis',   **LW)
ax.plot(chl_years, chl_vals,      color=BLUE,  marker='o', label='Chlamydia',
        linestyle='dashed', **LW)
style_ax(ax)
ax.annotate('data from 2020',
            xy=(2020, chl_msm[2020]),
            xytext=(2017.8, 5),
            fontproperties=POPPINS, fontsize=7.5, color=GRAY,
            arrowprops=dict(arrowstyle='-', color=GRAY, lw=0.8))
finish(fig, ax, 'chart-sti-msm.png')
