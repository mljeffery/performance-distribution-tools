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
from gst_tools import gst_utils


# ======================

def recent_trends_plot(df_emis):

    # drop missing data
    df_emis = df_emis.dropna(axis=1, how='all')

    # not needed, already only years / countries?
    #df_emis = gst_utils.set_non_year_cols_as_index(df_emis)

    years = df_emis.columns

    # calculate % changes
    df_emis_perc_change = df_emis.pct_change(axis='columns') * 100


    # calculate trends
    num_years_trend = 5

    df_rolling_average = df_emis_perc_change.rolling(window=num_years_trend, axis='columns').mean()

    gst_tools.make_simple_histogram(df_rolling_average['2016'], 'trend (%)')
    # for the one below, need to selet fewer years.
    #gst_tools.make_overlapping_kde_plots(df_rolling_average, '%', 'emissions trends')
    gst_tools.make_ridge_plot(df_rolling_average, '%', 'emissions trend')

    print('check')
    print('check')
