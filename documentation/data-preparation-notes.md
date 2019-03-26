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