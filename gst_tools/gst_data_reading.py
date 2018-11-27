
# Written by Louise Jeffery
# October, 2018

# Copyright License
# Creative Commons?

# Purpose:
# read data


# =========================
# Load modules etc.

import re

import pandas as pd
import seaborn as sns
import sys

# =========================
# Read or load data

current_PRIMAPhist_filename = 'PRIMAP-hist_no_extrapolation_v1.1_06-Mar-2017.csv'
current_socioeconomic_data_filename = ''
current_population_data_filename = 'UN-population-data-2017.csv'


def read_historic_emissions_data(variable, sector):

    """
    This function will read in the PRIMAP-hist dataset from the correctly formatted file.
    From that data it will extract the selected variable and unit to pass back to the
    calculation functions."
    The data should all be in CO2e, but the exact unit can be requested, e.g. tCO2e
    """

    print('')
    print('===========================')
    print('Reading in historic data')
    print('===========================')
    print('')

    # locate the historic data directory
    data_folder = 'data/'
    file_to_read = (data_folder + current_PRIMAPhist_filename)
    print('reading files from: ' + file_to_read)

    # basic read-in of data
    hist_data = pd.read_csv(file_to_read)

    #columns_available = hist_data.columns

    # get specific variable
    years = [y for y in hist_data[hist_data.columns] if (re.match(r"[0-9]{4,7}$", str(y)) is not None)]
    # years_int = list(map(int, years))

    hist_data = hist_data.set_index('country')

    # identify the units in the source data
    units = hist_data.loc[(hist_data['entity'] == variable) &
                          (hist_data['category'] == sector),
                          ['unit']]
    cur_unit = units['unit'].unique()

    # extract the requested data
    hist_emis_data = hist_data.loc[(hist_data['entity'] == variable) &
                                   (hist_data['category'] == sector),
                                   years]

    # TODO - could improve this to preserve more metadata

    # convert units (to standard Mt CO2e)
    if cur_unit == 'GgCO2eq':
        new_unit = 'MtCO2eq'
        hist_emis_data /= 1000
    else:
        new_unit = cur_unit
        print('Conversion not defined. Emissions data units remain as ' + new_unit)

    print('...')
    print('emissions data reading complete')
    print('===========================')
    print('')

    return hist_emis_data, new_unit


def read_historic_population_data():

    print('')
    print('===========================')
    print('Reading in population data')
    print('===========================')
    print('')

    # locate the historic data directory
    data_folder = 'data/'
    file_to_read = (data_folder + current_population_data_filename)
    print('reading files from: ' + file_to_read)

    # basic read-in of data
    pop_data = pd.read_csv(file_to_read)

    columns_available = pop_data.columns
    print('Columns in historic UN population data are: ')
    print(columns_available)

    pop_years = [y for y in pop_data[pop_data.columns] if (re.match(r"[0-9]{4,7}$", str(y)) is not None)]
    pop_data = pop_data.set_index('country')
    pop_unit = pop_data['unit'].unique()
    pop_data = pop_data[pop_years]

    if pop_unit == 'ThousandPers':
        print('Converting population from ThousandPers to Pers')
        pop_unit = 'Pers'
        pop_data *= 1000
    else:
        print('keeping population data as ' + pop_unit)

    print('...')
    print('population data reading complete')
    print('===========================')
    print('')

    return pop_data, pop_unit

