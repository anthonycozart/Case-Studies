import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns

# import raw data (in Stata format) used in Senior Honors Thesis
dframe = pd.read_stata('Python/wn_0512_pool1.dta')

# count the size of routes of airlines, following mergers
dframe = dframe[dframe['carrier'].isin(['AA', 'UA', 'WN', 'US', 'DL', 'NW'])]

# check for duplicates
dframe.shape
dframe.drop_duplicates(['dep_airp','arr_airp','id_period','carrier'],inplace=True)
dframe.shape

# there aren't any duplicate 'dep_airp','arr_airp' pairs
dframe['number_of_routes'] = 1
gp_airp = dframe.groupby(['id_period','carrier'],as_index=False)['number_of_routes'].count()

# build datetime object
gp_airp['quarter'] = gp_airp['id_period'] % 10
gp_airp['year'] = (gp_airp['id_period']-gp_airp['quarter'])/10

# plot with lines highlighting date of merger
# DL-NW: Q1 2010
# UA-C0: Q4 2010
