# Project and Title: Global Stocktake Toolkit - user control script

# Author(s): Louise Jeffery
# Contact: louise.jeffery@pik-potsdam.de
# Date: November, 2018

# Copyright License
# 

# Purpose:
# This is the main user script for running the different data analyses as part of the
# Global stocktake assessment toolkit.

# Instructions


# =========================================================

import sys
import re

import pandas as pd

# gst specific
#from gst_data_reading import *
#import gst_utils
#from gst_histogram_plot_tools import *

import gst_tools

# =================================
# user options

# TODO - currently works with KGHG but not CO2!
variable_selected = 'KYOTOGHGAR4'
sector_selected = 'IPCM0EL'

#desired_years = ['1950', '1960', '1970', '1980', '1990', '2000', '2010']
desired_years = ['2000', '2015']



# =========================
# Read or load data

# ** emissions **
df_emis, unit_emis = gst_tools.read_historic_emissions_data(variable_selected, sector_selected)

# ** population **
df_pop, unit_pop = gst_tools.read_historic_population_data()

# ================
# calculate per capita emissions

# Mt / Pers
emis_per_cap = df_emis / df_pop

# convert to Mt to t
if (unit_emis == 'MtCO2eq') & (unit_pop == 'Pers'):
    emis_per_cap *= 1000000
    emis_per_cap_unit = 'tCO2eq / capita'
else:
    print('Hm, check unit conversion and read-in.')

# drop NaN rows - some countries are missing!
emis_per_cap = emis_per_cap.dropna(axis=1, how='all')
emis_per_cap = emis_per_cap.dropna(axis=0, how='all')
# TODO - return list of missing information


# --------------
# use this data to make some plots
#gst_tools.make_ridge_plot(df_emis, unit_emis, variable_selected)
#gst_tools.make_ridge_plot(emis_per_cap, emis_per_cap_unit, 'Per capita emissions')


# temp commenting!
# histograms
#gst_tools.make_histograms_by_years(emis_per_cap[desired_years],
#                                   emis_per_cap_unit,
#                                   'Per capita emissions')
#gst_tools.make_overlapping_kde_plots(emis_per_cap[desired_years],
#                                     emis_per_cap_unit,
#                                     'Per capita emissions')

# averages
gst_tools.recent_trends_plot(df_emis)

