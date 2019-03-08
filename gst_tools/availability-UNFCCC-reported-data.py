#!/usr/bin/env python
# coding: utf-8

# # Summary of data availability under the UNFCCC

# modules

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

# intitialise some general settings
boldfont = {'fontsize': 13,
            'fontweight': 'bold',
            'verticalalignment': 'baseline'}


# these countries will be used in the same plot - all shown together

# UBA-GST project +
countries_of_interest = ['EU', 'China', 'India', 'Mexico', 'Viet nam', 'Ethiopia',
                         'Brazil', 'Argentina', 'Canada', 'Morocco', 'Peru', 'Saudi arabia']

# nice for 1996
# countries_of_interest = ['Switzerland', 'Australia', 'Belarus',
#        'Russian federation',
#        'United arab emirates', 'Argentina',
#        'Bangladesh', 'Bolivia', 'Brazil', 'Chile',
#        'Colombia', 'Ghana', 'Indonesia',  'Korea, republic of',
#        'Mauritius', 'Peru', 'South africa',  'Singapore'];

# ==================
# Get data

# select data to read in -
#datafile = "UNFCCC2006data.csv"
#dataSource = 'UNFCCCC2006'

#datafile = "UNFCCC1996DATAdata.csv"
#dataSource = 'UNFCCC1996'

datafile ='PRIMAPHIST20-data-all.csv'
dataSource = 'PRIMAPhist'

# actually read the data
data = pd.read_csv('../data/' + datafile)

# set here the order that we want the sectors to be plotted in
if dataSource == 'UNFCCC1996':
    sectorOrder = ['Energy', 'Industrial Processes', 'Solvents/Product Use',
                   'Agriculture', 'Land Use', 'Waste', 'Other']
elif dataSource == 'UNFCCC2006':
    sectorOrder = ['Energy', 'IPPU', 'AFOLU', 'Agriculture', 'Land Use', 'Waste', 'Other']
elif dataSource == 'PRIMAPhist':
    sectorOrder = ['Energy', 'IPPU', 'AFOLU', 'Agriculture', 'Land Use', 'Waste', 'Other']

# ===================
# DATA CLEANING

# Tidy up dataframe (e.g. all years to numbers, drop extra columns, set index)

# convert all years to numbers
for col in data.columns:
    if col.startswith('Y'):
        data = data.rename(columns={col: col[1:]})

# drop extraneous columns
if 'Unnamed: 34' in data.columns:
    data = data.drop('Unnamed: 34', axis=1)


# convert country names to lower case (makes the plots nicer for later...)
def make_lowercase(old_name):

    new_name = old_name[0] + old_name[1:].lower()
    return new_name

data['countries'] = data['countries'].apply(make_lowercase)

data.loc[data['countries'] == 'European union (28)', ['countries']] = 'EU'
data.loc[data['countries'] == 'Bolivia, the plurinational state of', ['countries']] = 'Bolivia'

# convert category names to something shorter
category_dict = {
        'Other': 'Other',
        'Energy': 'Energy',
        'TotalEnergy': 'Energy',
        'LULUCF': 'Land Use',
        'NationalTotal': 'Total',
        'IndustrialProcessesAndProductUse': 'IPPU',
        'Waste': 'Waste',
        'Agriculture': 'Agriculture',
        'AFOLU': 'AFOLU',
        'SolventAndOtherProductUse' : 'Solvents/Product Use',
        'IndustrialProcesses': 'Industrial Processes'
    }

data['sector'] = data['sector'].apply(category_dict.get)

# don't need these two
data = data.loc[data['entity'] != 'KYOTOGHGAR4']
data = data.loc[data['sector'] != 'Total']

# ================================
# DATA PREP
# counting! find data available by country for each sector /gas (? groupby)

# first, make things clean by making a data availability mask - all data just ones or zeros
year_columns = [y for y in data[data.columns] if (re.match(r"[0-9]{4,7}$", str(y)) is not None)]

# now make a true / false map
mask_data = data.copy()
mask_data[year_columns] = mask_data[year_columns].notnull()
mask_data

# get list of data available
gases = data.entity.unique()
sectors = data.sector.unique()
countries = data.countries.unique()

# count the number of data points available for each country
country_results = mask_data.groupby('countries').sum()
country_results = country_results.reset_index()

#country_results


# ===================
# DATA ANALYSIS AND PLOTS

# Prepare a sub-set of data to plot
results_to_plot = country_results.loc[country_results['countries'].isin(countries_of_interest)]

# set the index so it's automatically a y axis label
results_to_plot = results_to_plot.set_index('countries')


# actually make a plot

ax = sns.heatmap(results_to_plot[year_columns], linewidths=.25, annot=False, cmap="YlGnBu") #, fmt='d')
ax.set_ylabel('')
ax.set_xlabel('')
ax.set_title('Data availability by year \n (number of sectors and gases covered)', fontdict=boldfont)
plt.tight_layout()

# save figure to file
figname = '../output/data-availability/years-of-data-by-country' + dataSource

#plt.savefig((figname + '.png'), format='png', dpi=800)
plt.savefig((figname + '.pdf'), format='pdf', dpi=800)
#plt.savefig((figname + '.eps'), format='eps')

plt.close()

# ============================
# Plot 2 - plot sectors and gases by country...

sns.set(style="darkgrid")

sectors = data.sector.unique()
gases = data.entity.unique()

# get the data for this country
country_data = mask_data.loc[mask_data['countries'].isin(countries_of_interest)]
country_data = country_data.drop(['sectorCode', 'unit', 'ISO'], axis=1)

# convert format to a matrix of available data, counting the number of years with data
data_matrix = country_data.set_index(['countries', 'sector', 'entity'])
data_matrix['yearsOfData'] = data_matrix.sum(axis=1)
data_matrix = data_matrix.drop(year_columns, axis=1)
data_matrix = data_matrix.unstack('entity')
data_matrix.columns = data_matrix.columns.droplevel()

# drop unwanted columns, and reorder columns for tidier plot
#data_matrix = data_matrix[['CO2', 'CH4', 'N2O']]
data_matrix = data_matrix[['CO2', 'CH4', 'N2O', 'HFCS', 'PFCS', 'SF6', 'NF3']]

data_matrix

# reorder the index...
# data_matrix = data_matrix.reindex(sectorOrder, level='sector')
#data_matrix = data_matrix.drop(index='AFOLU')

for selected_country in countries_of_interest:

    if selected_country in data_matrix.index:

        # Use to build new dataframe for selected country
        data_available = data_matrix.loc[selected_country, :]
        data_available = data_available.reindex(sectorOrder)

        # replace some of the NaNs by zeros where data is expected??
        #data_available = data_available.where(data_available.notnull(), 0)
        #data_available = data_available.where(no_data_expected, 'NaN')

        # make a plot
        ax = sns.heatmap(data_available, linewidths=.25, annot=True, cmap="viridis_r", vmin=0,
                         vmax=28, cbar_kws={'label': 'Years of data'})
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_title(selected_country, fontdict=boldfont)
        plt.tight_layout()

        # and save to file
        figname = '../output/data-availability/gas-sector-availability-' + selected_country + '-' + dataSource

    #    plt.savefig((figname + '.png'), format='png', dpi=800)
        plt.savefig((figname + '.pdf'), format='pdf', dpi=800)
    #    plt.savefig((figname + '.eps'), format='eps')

        # clear so no further problems?
        plt.close()
        
    else:
        print('sorry, ' + selected_country + ' is not available.')
    

