# Project and Title

# Author(s): Louise Jeffery
# Contact: louise.jeffery@pik-potsdam.de; mlouise@posteo.de 
# Last updated: June, 2019


# Purpose: Make distribution plots for indicators of global progress
# 

# =====================================================

import re, sys, os

import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

from shortcountrynames import to_name

# ======================


# UBA colour scheme for all functions
def get_uba_colours():

    # UBA dict from Annika Guenther
    uba_colours = {}
    uba_colours['uba_dark_green'] = [xx / 255 for xx in (0, 118, 38)]
    uba_colours['uba_bright_green'] = [xx / 255 for xx in (97, 185, 49)]
    uba_colours['uba_bright_blue'] = [xx / 255 for xx in (0, 155, 213)]
    uba_colours['uba_dark_blue'] = [xx / 255 for xx in (18, 93, 134)]
    uba_colours['uba_bright_orange'] = [xx / 255 for xx in (250, 187, 0)]
    uba_colours['uba_dark_pink'] = [xx / 255 for xx in (131, 5, 60)]
    uba_colours['uba_bright_pink'] = [xx / 255 for xx in (206, 31, 94)]
    uba_colours['uba_dark_orange'] = [xx / 255 for xx in (215, 132, 0)]
    uba_colours['uba_bright_purple'] = [xx / 255 for xx in (157, 87, 154)]
    uba_colours['uba_dark_purple'] = [xx / 255 for xx in (98, 47, 99)]

    return uba_colours


def set_uba_palette():

    uba_palette = [
                [xx / 255 for xx in (0, 118, 38)],
                [xx / 255 for xx in (18, 93, 134)],
                [xx / 255 for xx in (98, 47, 99)],
                [xx / 255 for xx in (215, 132, 0)],
                [xx / 255 for xx in (131, 5, 60)],
                [xx / 255 for xx in (97, 185, 49)],
                [xx / 255 for xx in (0, 155, 213)],
                [xx / 255 for xx in (157, 87, 154)],
                [xx / 255 for xx in (250, 187, 0)],
                [xx / 255 for xx in (206, 31, 94)]
                  ]

    return uba_palette

# main plotting function used throughout - flexibility given so that it can cope with a range of different input!

def make_histogram(df, unit_,
                   xlabel='', title='', sourcename='unspecified',
                   remove_outliers=False, ktuk=3,
                   save_plot=False, plot_name='',
                   selected_country=''):

    """
    This is based on the make_simple_histogram function but caters to data that
    contains both positive and negative values. For the GST, it's important to be
    able to see whether or not trends etc. are positive or negative and a symmetric
    binning approach is needed.

    To calculate the bin sizes, we use a couple of conditional rules based on the data
    available, including the max and min of the data and the number of data points.
    For most plots we are expecting around 200 countries, but could also be a few regions.

    TODO - the 'outlier' calculation is helpful to see some data better BUT need to be careful.
    Proposed solution is to make BOTH plots so that it's clear to the user when data has been
    removed.

    TODO - 'df' is actually a series -> better name?

    TODO - edit selected country option to deal with ISO codes or names.
    """

    # Check the data - needs to not be, for example, all zeros
    if len(df.unique()) == 1:
        print('---------')
        print('All values in the series are the same! Exiting plotting routine for ' + str(plot_name))
        print('---------')
        return

    # get the value here in case it's excluded as an outlier
    if selected_country:
        # get value of that country
        country_value = df[selected_country]

    # set a style
    sns.set(style="darkgrid")
    sns.set_palette(set_uba_palette())

    if remove_outliers:
        # Outliers - in some cases, the date contains extreme outliers. These make for an unreadable
        # plot and in most cases arise from exceptional circumstances. These outliers are therefore removed
        # from the plots and the removal signalled to the user.
        # Example: Equatorial Guinea's emissions rose dramatically in the mid-90s due to the discovery of
        # oil. So much so, that the current emissions relative to 1990 are over 6000% higher. Including these
        # emissions in the plots would render a useless graph so we remove this country from the overview.

        # Use Tukey's fences and the interquartile range to set the bounds of the data
        # https://en.wikipedia.org/wiki/Outlier
        # For reference: kTUk default is set to 3 (above)
        # k = 1.5 -> outlier; k = 3 -> far out
        # TODO - get full and proper reference for this!!!

        print('-----------')
        print('Identifying and removing outliers')

        # calculate limits
        q75, q25 = np.percentile(df, [75, 25])
        iqr = q75 - q25
        tukey_min = q25 - ktuk * iqr
        tukey_max = q75 + ktuk * iqr
        # for testing:
        # print('tukey_min is ' + str(tukey_min))
        # print('tukey_max is ' + str(tukey_max))

        # Tell the user what the outliers are:
        lower_outliers = df[df < tukey_min]
        print('lower outliers are:')
        print(lower_outliers)
        upper_outliers = df[df > tukey_max]
        print('upper outliers are: ')
        print(upper_outliers)
        print('---')

        noutliers = len(lower_outliers) + len(upper_outliers)

        # actually remove the outliers
        df = df[(df > tukey_min) & (df < tukey_max)]

    # STATS
    # get some basic info about the data to use for setting styles, calculating bin sizes, and annotating plot
    maximum = max(df)
    minimum = min(df)
    mean = np.mean(df)
    median = np.median(df)
    npts = len(df)

    # Use data metrics to determine which approach to use for bins.
    if (minimum < 0) & (maximum > 0):

        # If both positive and negative, bins should be symmetric around 0!
        # What's the range of data?
        full_range = np.ceil(maximum - minimum)

        # Freedman–Diaconis rule
        # (need to recalculate IQR)
        q75, q25 = np.percentile(df, [75, 25])
        iqr = q75 - q25
        bin_width = int(2 * (iqr) / (npts ** (1 / 3)))

        # or the simple 'excel' rule:
        # bin_width = int(full_range / np.ceil(npts**(0.5)))

        # for nbins, need to take into account asymmetric distribution around 0
        nbins = int(np.ceil(2 * max([abs(minimum), abs(maximum)])) / bin_width)
        if not (nbins / 2).is_integer():
            nbins = nbins + 1

        # determine bin edges
        bins_calc = range(int((0 - (1 + nbins / 2) * bin_width)), int((0 + (1 + nbins / 2) * bin_width)), bin_width)
        print('bins set to ' + str(bins_calc))

    else:
        if maximum < 25:

            bin_width = 1

            # or the simple 'excel' rule:
            # bin_width = int(full_range / np.ceil(npts**(0.5)))

            # for nbins, need to take into account asymmetric distribution around 0
            nbins = np.ceil(abs(maximum))

            # determine bin edges
            bins_calc = range(0, int(1 + nbins), bin_width)
            print('bins set to ' + str(bins_calc))

        else:
            # use inbuilt Freedman-Diaconis
            # ? TODO - modify to ensure integers? or replicate above?
            bins_calc = 'fd'

    # --------------
    # MAKE THE PLOT

    # set up the figure
    fig, axs = plt.subplots()

    # make histogram
    sns.distplot(df,
                 kde=False,
                 bins=bins_calc)
                 #color='mediumseagreen',
                 #rug=False,
                 #rug_kws={"color": "rebeccapurple", "alpha": 0.7, "linewidth": 0.4, "height": 0.03})

    # get xlims
    xmin, xmax = axs.get_xlim()

    # Dynamically set x axis range to make symmetric abut 0
    if minimum < 0:

        # reset xmin or xmax
        if np.absolute(xmax) > np.absolute(xmin):
            plt.xlim(-xmax, xmax)
        else:
            plt.xlim(xmin, -xmin)

        # and add a line at 0
        axs.axvline(linewidth=1, color='k')

        # and annotate with the number of countries either side of the line
        # ARROWS!

        nbelow = len(df[df < 0])
        nabove = len(df[df > 0])

        axs.annotate(str(nbelow) + ' countries',
                     xytext=(0.31, 1.0), xycoords=axs.transAxes,
                     fontsize=9, color='black',
                     xy=(0.15, 1.01),
                     arrowprops=dict(arrowstyle="-|>", color='black'),
                     bbox=dict(facecolor='white', edgecolor='grey', alpha=0.75)
                     )
        axs.annotate(str(nabove) + ' countries',
                     xytext=(0.54, 1.0), xycoords=axs.transAxes,
                     fontsize=9, color='black',
                     xy=(0.85, 1.01),
                     arrowprops=dict(arrowstyle="-|>", color='black'),
                     bbox=dict(facecolor='white', edgecolor='grey', alpha=0.75)
                     )

    # If a country is selected for highlighting, then indicate it on the plot!
    if selected_country:

        # get value of that country
        # country_value = df[selected_country]

        if (country_value > xmin) & (country_value < xmax):
            # indicate it on the plot
            axs.axvline(x=country_value, ymax=0.9, linewidth=1.5, color='rebeccapurple')

            # annotate with country name
            ymin, ymax = axs.get_ylim()
            ypos = 0.65 * ymax
            axs.annotate((to_name(selected_country) + ' ' + "\n{:.2g}".format(country_value)) + unit_,
                         xy=(country_value, ypos), xycoords='data',
                         fontsize=9, color='rebeccapurple',
                         bbox=dict(facecolor='white', edgecolor='rebeccapurple', alpha=0.75)
                         )

        else:
            axs.annotate((to_name(selected_country) + ' ' + "\n{:.2g}".format(country_value)) + unit_,
                         xy=(.75, .65), xycoords=axs.transAxes,
                         fontsize=9, color='rebeccapurple',
                         bbox=dict(facecolor='white', edgecolor='rebeccapurple', alpha=0.75)
                         )

    # Annotate the plot with stats
    axs.annotate(("Data source: \n " + sourcename + "\n"
                  "\n maximum  = {:.2f}".format(maximum) +
                  "\n minimum   = {:.2f}".format(minimum) +
                  "\n mean        = {:.2f}".format(mean) +
                  "\n median     = {:.2f}".format(median) +
                  "\n number of \n countries  = {:.0f}".format(npts)
                  ),
                 xy=(1.05, 0.6), xycoords=axs.transAxes,
                 fontsize=9, color='black',
                 bbox=dict(facecolor='white', edgecolor='grey', alpha=0.75))

    # if some countries were removed, indicate on the plot
    if remove_outliers:
        axs.annotate(('  ' + str(noutliers) + ' outliers not shown'),
                     xy=(1.05, 0.53), xycoords=axs.transAxes,
                     fontsize=8, color='black')

    # label axes and add title
    axs.set_xlabel((xlabel + ' \n(' + unit_ + ')'), fontsize=12)
    axs.set_ylabel('number of countries', fontsize=12)
    axs.set_title((title + "\n"), fontweight='bold')

    # save to file
    if save_plot:
        filepath = os.path.join('output', 'plots')
        if selected_country:
            fname = ('basic_histogram-' + plot_name + '-' + to_name(selected_country) + '.png')
        else:
            fname = ('basic_histogram-' + plot_name + '.png')
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename = os.path.join(filepath, fname)
        plt.savefig(filename, format='png', dpi=600, bbox_inches='tight')
        plt.close()

    # show the plot
    plt.show()


def make_histogram_peaking(df, var, unit_, start_year, end_year, save_plot=False):

    """
    This function is specifically written to plot the peaking year of a variable for a range
    of countries.
    """

    # Check the data - needs to not be, for example, all zeros
    if len(df.unique()) == 1:
        print('---------')
        print('All values in the series are the same! Exiting plotting routine for ' + str(var))
        print('---------')
        return

    # set a style
    sns.set(style="darkgrid")

    # STATS
    # get some basic info about the data to use for setting styles, calculating bin sizes, and annotating plot
    maximum = int(max(df))
    minimum = int(min(df))
    mean = np.mean(df)
    median = np.median(df)
    npts = len(df)

    # determine bin edges - annual!
    bin_width = 1
    bins_calc = range((start_year - 1), (end_year + 2), bin_width)

    # --------------
    # MAKE THE PLOT

    # set up the figure
    fig, axs = plt.subplots()

    uba_colours = get_uba_colours()

    # make histogram
    N, bins, patches = axs.hist(df, bins=bins_calc,
                                edgecolor='white', linewidth=1)

    for i in range(0, len(patches)):
        patches[i].set_facecolor(uba_colours['uba_dark_purple'])
    patches[-1].set_facecolor(uba_colours['uba_bright_orange'])
    patches[-1].set_alpha(0.4)

    # Dynamically set x axis range to make symmetric abut 0
    if minimum < 0:
        # get and reset xmin or xmax
        xmin, xmax = axs.get_xlim()
        if np.absolute(xmax) > np.absolute(xmin):
            plt.xlim(-xmax, xmax)
        else:
            plt.xlim(xmin, -xmin)

        # and add a line at 0
        axs.axvline(linewidth=1, color='k')

    # number of countries in the last bin
    nlast = N[-1]

    # Annotate the plot with stats
    axs.annotate(("{:.0f} countries, ".format(npts) +
                  "\nof which {:.0f} have ".format(nlast) +
                  "\nnot yet reached a maximum (orange)"),
                 xy=(0.03, 0.82), xycoords=axs.transAxes,
                 fontsize=10, color='black',
                 bbox=dict(facecolor='white', edgecolor='grey', alpha=0.75))

    # label axes and add title
    axs.set_xlabel('year')
    axs.set_ylabel('number of countries')
    axs.set_title(('year when ' + var + ' peaked'), fontweight='bold')

    # save to file
    if save_plot:
        filepath = os.path.join('output', 'plots')
        fname = ('basic_histogram-peaking-since-' + str(start_year) + '-' + var + '.png')
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename = os.path.join(filepath, fname)
        plt.savefig(filename, format='png', dpi=450, bbox_inches='tight')
        plt.close()

    # show the plot
    plt.show()


def plot_facet_grid_countries(df, variable, value, main_title='', plot_name='', save_plot=False):

    """
    plot a facet grid of variables for a range of countries. Can be used to, e.g. assess
    which countries have emissions that have peaked, and which not.
    """

    # First, get some idea of the data so that it's easier to make clean plots
    ranges = df.max(axis=1) - df.min(axis=1)
    check = (ranges.max() - ranges.min()) / ranges.min()
    if abs(check) < 8:
        yshare = True
    else:
        yshare = False

    # set up the df for plotting
    year_cols = df.columns
    dftomelt = df.reset_index()
    dftomelt['country'] = dftomelt['country'].apply(to_name)
    dfmelt = pd.melt(dftomelt, id_vars=['country'],
                     value_vars=year_cols, var_name=variable, value_name=value)

    # set up the grid
    grid = sns.FacetGrid(dfmelt, col='country', palette="tab20c", sharey=yshare,
                         col_wrap=4, aspect=1)

    # make the actual plots
    grid.map(sns.lineplot, variable, value, color="rebeccapurple")

    # Give subplots nice titles
    grid.set_titles(col_template='{col_name}')

    # tidy up a bit
    for ax in grid.axes.flat:
        ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(4, prune="both"))
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(4, prune="both"))
        ax.axhline(0, color='k')
    if yshare:
        grid.fig.subplots_adjust(hspace=.15, wspace=.1, top=.95)
    else:
        grid.fig.subplots_adjust(hspace=.15, wspace=.25, top=.95)

    # give the whole plot a title
    grid.fig.suptitle(main_title, fontweight='bold', fontsize=15)

    if save_plot:
        filepath = os.path.join('output', 'plots')
        # grid.map(horiz_zero_line)
        fname = ('facetgrid-' + plot_name + '-' + value + '.pdf')
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename = os.path.join(filepath, fname)
        plt.savefig(filename, format='pdf', bbox_inches='tight')
        plt.close()


def peaking_barplot(summary_data, variable, max_year, save_plot=False):

    uba_palette = set_uba_palette()
    sns.set_palette(uba_palette)
    sns.set(style="darkgrid", context="paper")

    # make histogram
    fig, ax = plt.subplots()

    splot = sns.barplot(x=summary_data['category'], y=summary_data['count'])

    for p in splot.patches:
        splot.annotate(format(p.get_height(), '.0f'),
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                  ha = 'center', va = 'center',
                  xytext = (0, 10), textcoords = 'offset points')

    plt.tight_layout
    plt.xlabel('')
    plt.ylabel('number of countries')
    plt.title("Status of " + variable + "\nin " + max_year)

    if save_plot:
        filepath = os.path.join('output', 'plots')
        fname = ('peaking-categories-' + variable + '.png')
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename = os.path.join(filepath, fname)
        plt.savefig(filename, format='png', dpi=600, bbox_inches='tight')
        plt.close()

