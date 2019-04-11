# Data preparation 

Author: Louise Jeffery, March 2019

Content: Notes on code and options taken for data preparation.

## PRIMAP-hist

One of the key datasets is PRIMAP-hist. As this could be updated multiple times, I use the dataset available online and write a preparation script that can be used by others to get the desired data in the right format. 


### countrygroups

Robert's countrygroups module is useful for reducing the country list to UNFCCC members only. It's a bit awkward to access the lists, but if focussing on only a few options it works okay. 

Some useful code snippets for future reference...

``` python

# get a list of groups (full list includes other things)
dir(countrygroups)

# reduce to just the country groups (all caps)
[item for item in dir(countrygroups) if item.upper() == item]

```

A dependency of countrygrouops is 'shortcountrynames which contains a mapping for ISO codes to longer countrynames. Could be useful!

```python
[In]  : shortcountrynames.to_name('AFG')
[Out] : 'Afghanistan'
```


## EIA

Data from the US' Energy Information Administration is made available for plotting using the global-stocktake-tools. 

Data can be downloaded in a .csv format from the [EIA website](https://www.eia.gov/beta/international/data/browser/#/?pa=004000001000000000000000000000000000000000000000000000000fu&c=ruvvvvvfvtvnvv1urvvvvfvvvvvvfvvvou20evvvvvvvvvnvvuvs&ct=0&vs=INTL.44-1-AFG-QBTU.A&cy=2016&vo=0&v=H&end=2017) as a .csv file. 

To make it easier for the user, we have already performed some pre-processing to put the data in the correct format for the tools provided here. More specifically, we have:

* rearranged the data so that it can be read in with separate energy and sector headings
* removed the undefined and sparse values for 2017
* replaced the '--' and '(s)' values in the original data with nan
* removed some of the commas in the country names so that the data can be stored and read-in automatically as a comma separated file.
* 