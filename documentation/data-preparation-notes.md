# Data preparation 

Author: Louise Jeffery, March 2019
Last Updated: November, 2019

Content: Notes on code and options taken for data preparation.

## PRIMAP-hist

One of the key datasets for the perfomrnace distribution tools is [PRIMAP-hist](www.pik-potsdam.de/paris-reality-check/primap-hist/). As this dataset could be updated multiple times, we suggest that users download the latest version of the dataset available online. The notebooks provided with this package can be used to extract the desired data and put it in the correct format. 


### countrygroups

The countrygroups module from open_climate_data is a useful tool for reducing the country list to UNFCCC members only.

Some useful code snippets for reference are

``` python

# get a list of groups (full list includes other things)
dir(countrygroups)

# reduce to just the country groups (all caps)
[item for item in dir(countrygroups) if item.upper() == item]

```

A dependency of countrygrouops is 'shortcountrynames which contains a mapping for ISO codes to longer countrynames. 

```python
[In]  : shortcountrynames.to_name('AFG')
[Out] : 'Afghanistan'
```

# Alternative datasets

There are many different data sources that could be used with the performance distribution tools. We do not provide them here because we think that it's improtant that the users (1) Know where the original data is from, and (2) have the most up to date versions of the data. 

We acknowledge that this implies additional work in data processing. To make it a bit easier, we provide an example data output and endeavour to keep the work minimal. 

A key challenge with country data is in converting inconsistent names to country codes. Some tools are available to do this, but not all work on all platforms. 

If you have further suggestions to improve this aspect of the code, please contribute an edit or open an issue on github. 
