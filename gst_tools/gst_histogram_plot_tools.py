# Written by Louise Jeffery
# October, 2018

# Copyright License
# Creative Commons?

# Purpose:
# Make a histogram plot to convey 'collective' progress under the UNFCCC
# first test is a trial version with per capita emissions

# =========================
# Load modules etc.

import pandas as pd
import seaborn as sns

import sys
import re
import math

import matplotlib.pyplot as plt

# gst specific


# ================
# PLOTTING
# ================

# define a function to make a ridge plot
def make_ridge_plot(data, thisunit, thisvar):

    # set a style
    sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

    # get some info about data
    years_available = data.columns
    new_var = (thisvar + ' (' + thisunit + ')')

    # get only the years you want for the plot
    cols_to_get = ['1950', '1970', '1990', '2000', '2010']
    cols_to_drop = list(set(years_available) - set(cols_to_get))
    data = data.drop(cols_to_drop, axis=1)

    # reorganise the data to two columns, one with the data, and one with the year label
    data = data.unstack()
    data = data.reset_index()
    data = data.rename(columns={'level_0': 'years', 0: new_var})

    # Initialize the FacetGrid object
    pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
    g = sns.FacetGrid(data, row="years", hue="years", aspect=15, size=0.5, palette=pal)  #height=0.5 - for any seaborn updates...

    # Draw the densities in a few steps
    g.map(sns.kdeplot, new_var, clip=[0, 20], clip_on=True, shade=True, alpha=0.8, lw=1.5, bw=.1)
    g.map(sns.kdeplot, new_var, clip=[0, 20], clip_on=True, color="k", lw=1, bw=.1)
    g.map(plt.axhline, y=0, lw=2, clip_on=True)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .05, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes, fontsize=8)


    g.map(label, new_var)

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-.5)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)

    g.set_xlabels(color='midnightblue', fontweight='bold', fontsize=10)

    # save to file
    outputdir = 'output/plots/'
    plt.savefig((outputdir + 'kde_ridges_' + thisvar + '.pdf'),
                format='pdf')
    plt.close()


def make_histograms_by_years(df, unit, label):

    # set a style
    sns.set(style="darkgrid") #, rc={"axes.facecolor": (0, 0, 0, 0)})

    year_cols = df.columns
    years_int = list(map(int, year_cols))

    nplots = len(years_int)
    needed_rows = math.ceil(math.sqrt(nplots))

    fig, axs = plt.subplots(nrows=needed_rows, ncols=needed_rows, sharex=True, sharey=True)

    iplot = -1

    bin_edges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                 35, 40, 45, 50, 55, 60, 100]

    for year in years_int:

        iplot = iplot + 1
        ix = math.floor(iplot / needed_rows)
        iy = iplot - (ix * needed_rows)

        cur_ax = axs[ix, iy]

        # Make default histogram of sepal length
        sns.distplot(df[str(year)],
                     kde=False,
                     #rug=True, rug_kws={"color": "rebeccapurple", "alpha": 0.5, "linewidth": 0.5, "height": 0.1},
                     bins=bin_edges,
                     ax=cur_ax)

        # set xlim - otherwise too quished to read...
        plt.xlim(right=50, left=0)

        # save to file
    outputdir = 'output/plots/'
    plt.savefig((outputdir + 'basic_histogram.pdf'),
                format='pdf')
    plt.close()


def make_overlapping_kde_plots(df, unit, label):

    # set a style
    sns.set(style="darkgrid") #, rc={"axes.facecolor": (0, 0, 0, 0)})
    #sns.set_palette(sns.cubehelix_palette(2, start=2, rot=0, dark=0, light=.95, reverse=True))

    year_cols = df.columns
    years_int = list(map(int, year_cols))

    fig, axs = plt.subplots(1, 1)

    #colours = [ ]
    #colours = ['mediumseagreen', 'dodgerblue', 'rebeccapurple', 'orange', 'midnightblue']
    nplot = -1

    bin_edges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                 35, 40, 45, 50, 55, 60, 100]

    for year in year_cols:

#        # Plotting hist without kde
#        ax = sns.distplot(df[str(year)], bins=bin_edges,
#                          hist_kws={"linewidth": 2,
#                          "alpha": 0.5}, kde=False)
#
#        # Creating another Y axis
#        second_ax = ax.twinx()
#
#        # Plotting kde without hist on the second Y axis
#        sns.distplot(df[str(year)], ax=second_ax, kde=True, hist=False)
#
#        # Removing Y ticks from the second axis
#        second_ax.set_yticks([])
#
        nplot = nplot + 1

        # Make histogram of each year requested (overlapping)
        sns.distplot(df[str(year)],
                     kde=True,
                     rug=False,
                     bins=bin_edges,
                     hist_kws={"linewidth": 2,
                               "alpha": 0.5},
                     label=year)
                        #"color": colours[nplot]},
#                        #"histtype": "step",   - for outline only
    # add a legend
    plt.legend()

    # set xlim - otherwise too quished to read...
    plt.xlim(right=40, left=0)

    # save to file
    outputdir = 'output/plots/'
    plt.savefig((outputdir + 'basic_histogram_overlapping.pdf'),
                format='pdf')


# straight up histogram!
def make_simple_histogram(df, label):

    # set a style
    sns.set(style="darkgrid")  #, rc={"axes.facecolor": (0, 0, 0, 0)})

    fig, axs = plt.subplots()

    # if bin edges are specified, it's not so easily generalised!
    # bin_edges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    #             11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    #             21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    #             35, 40, 45, 50, 55, 60, 100]

    # Make default histogram of sepal length
    sns.distplot(df, kde=False)
#                 rug=True)
                 #rug_kws={"color": "rebeccapurple", "alpha": 0.5, "linewidth": 0.5, "height": 0.1})

    # set xlim - otherwise too squished to read...
    # plt.xlim(left=0)

    # save to file
    outputdir = 'output/plots/'
    plt.savefig((outputdir + 'basic_histogram_' + label + '.pdf'),
                format='pdf')
    plt.close()


