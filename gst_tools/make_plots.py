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
import matplotlib.pyplot as plt
import seaborn as sns

# ======================

def make_simple_histogram(df, variable, unit):

    # set a style
    sns.set(style="darkgrid")  #, rc={"axes.facecolor": (0, 0, 0, 0)})

    fig, axs = plt.subplots()

    # bin_edges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    #             11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    #             21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    #             35, 40, 45, 50, 55, 60, 100]

    # Make default histogram
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
