# global-stocktake-tools

Tools developed in the context of the UBA Global Stocktake project to assess and monitor collective progress toward the Paris Agreement Goals. 

Author: Louise Jeffery  
Contact: louise.jeffery@pik-potsdam.de

Project begin: August, 2018  
Last Update: February 2019

====================================

## set-up and installation

The analysis can all be run using Jupyter notebooks. Jupyter notebooks run in a browser and are easy and convenient ways to run, visualise and document your code. Jupyter notebooks run on all platforms and can be installed following the instructions [here](https://jupyter.org/install). 


## Toolbox Description

### Data

All data is stored in the data folder and should comply with the basic shape required by the toolbox[^1].

Current data available includes:  

* PRIMAP-hist dataset 
* UN population data
* ...


### Tools

Most of the tools in this toolbox aim at displaying 'aggregate' data in a meaningful way. To do so, some pre-processing is required to get the data in the right format, to create some new combined metrics (e.g. energy intensity), and to calculate trends and averages. 


### Output



 
 
## Development

### Data
* need to get a standardised data format (and export system from PRIMAP-emmod). Check work computer and work with others to get this prepared. 
* Need to define what data will be included. In all cases, want to have as many countries or regions as possible. Grouping countries by region / NDC type / ??? might also be good.
	* emissions by sector / gas
	* population
	* GDP (PPP and MER?)
	* GVA by sector
	* energy supply / demand??
	* primary enegy / final energy
	* non-fossil share of energy supply
* Possbile additional data to include 
	* detailed industry data?
	* detailed forestry data

	
	
### Plots

#### histograms

The histogram plots could summarise a range of different types of information. They lend themselves to metrics that are somewhat normalised, e.g. intensities, per capita, %, that are more comparable across countries and don't get dominated by large economies. Not forgetting, of course, that large economies have a big influence and are important! 

Recent trends could also be captured in such an analysis. 

?? what about % share of a sector in total emissions?

#### coverage
The coverage plots are designed to show the extent to which a matrix of information is covered. This could be, for example, the years of data available for different gases / countries / sectors, or the number of countries that have policies in a given area (see the country factsheets). 

#### bidirectional scatter plots, with sizes?

The IPCC AR5, for example, has some scatter plots of Emissions / capita vs GDP / capita, where the dots are sized by total emissions. These plots could show more information and are quite cool, but also complex. Maybe show some examples for visualisation? Ch5 of the AR5 report is pretty nice for this!  
**TODO** - is the AR6 Ch5 going to be similar?

#### global
Assessing single countries, regions, or global totals allows different types of plots to be used. Such as shares of different sectors and gases. (Again see AR5 Ch5). 


### Utility functions
	
These are standard functions that can be used for mutltiple metrics. Some for data organisation and rearranging, others for a standardised approach for calculating trends etc. 

	
	
### capabilities?
* highlight a specific country within a distribution (for the factsheets)
* 



===

[^1]: A basic shape is defined so that the input reading and processing can be kept simple. This toolbox is designed to focus on the analysis and presentation of results, and not on data preparation. Currently, the PRIMAP emissions module is the primary data preparation tool, but other tools should be capable of writing this data format. For more information, please see more detailed documentation. **TODO**. 
 
