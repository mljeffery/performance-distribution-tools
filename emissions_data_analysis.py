# Project and Title

# Author(s): Louise Jeffery
# Contact: louise.jeffery@pik-potsdam.de; mlouise@posteo.de 
# Date: **MONTH, YYYY**

# Copyright License:
# 

# Purpose:
# 

# =====================================================

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import gst_tools

# set a style
sns.set(style="darkgrid")  #, rc={"axes.facecolor": (0, 0, 0, 0)})

# ======================
# Get data

variable_selected = 'KYOTOGHGAR4'
sector_selected = 'IPCM0EL'


# ** emissions **
df_emis, unit_emis = gst_tools.read_historic_emissions_data(variable_selected, sector_selected)

# ======================

# first - reduction relative to base year

emis_rel_1990 = 100 * (df_emis['2016'] - df_emis['1990']) / df_emis['1990']
emis_rel_1990 = emis_rel_1990.dropna()
emis_rel_1990 = emis_rel_1990[emis_rel_1990 < 1000]

emis_rel_2005 = 100 * (df_emis['2016'] - df_emis['2005']) / df_emis['2005']
emis_rel_2005 = emis_rel_2005.dropna()
emis_rel_2005 = emis_rel_2005[emis_rel_2005 < 1000]

# ======================
# plot the results


# straight up histogram!
def make_histogram(df, label, yearstr):

    fig, axs = plt.subplots()

    # if bin edges are specified, it's not so easily generalised!
    bin_edges = [-100, -80, -60, -40, -20,
                 0, 20, 40, 60, 80,
                 100, 120, 140, 160, 180,
                 200, 220, 240, 260, 280,
                 300, 320, 340, 360, 380,
                 400, 420, 440, 460, 480,
                 500, 520, 540, 560, 580,
                 600]

    # Make default histogram of sepal length
    sns.distplot(df, kde=False,
                 bins=bin_edges)
#                 rug=True)
                 #rug_kws={"color": "rebeccapurple", "alpha": 0.5, "linewidth": 0.5, "height": 0.1})

    # set xlim - otherwise too squished to read...
    # plt.xlim(left=0)

    plt.xlabel('% reduction since ' + yearstr)
    plt.ylabel('Number of countries')

    # save to file
    outputdir = 'output/plots/'
    plt.savefig((outputdir + 'histogram-' + label + '.pdf'),
                format='pdf')
    plt.close()


make_histogram(emis_rel_1990, 'emissions-relative-1990', '1990')
make_histogram(emis_rel_2005, 'emissions-relative-2005', '2005')


# ======================
# recent historic trend

# TODO - easier with google!

# want to calculate average trend over last 10 years, where data available (use the NE source!
# 2006 - 2016

# also for 5 years -> financial crisis issue!!



