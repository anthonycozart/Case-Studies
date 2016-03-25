import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# import raw data (in Stata format) used in Senior Honors Thesis
dframe = pd.read_stata('Python/wn_0512_pool1.dta')
dframe.shape
dframe.info()

# import airport code list (also in Stata format)
airport_list = pd.read_stata('Python/airport_lst.dta')

# rename airport_list columns, and merge on dep_airp
airport_list.columns = ['dep_cod_num','dep_airp_name']
dframe = pd.merge(dframe,airport_list,left_on=['dep_airp'],right_on=['dep_cod_num'])

# rename airport_list columns, and merge on arr_airp
airport_list.columns = ['arr_cod_num','arr_airp_name']
dframe = pd.merge(dframe,airport_list,left_on=['arr_airp'],right_on=['arr_cod_num'])

# keep just flights from SFO
def SFO(dep,arr):
	if dep == 'SFO':
		return 1
	elif arr == 'SFO':
		return 1
	else return 0

dframe['SFO'] = dframe.apply(lambda x: SFO(x['dep_airp_name'], x['arr_airp_name']), axis=1)
dframe = dframe[dframe.SFO == 1]

# keep just observations with direct flights
dframe = dframe[dframe.fare_dir != 0]

# let's look at LAX-SFO, which Southwest entered in 2010
sfo_lax = dframe[dframe.dep_airp == 4]

to_keep = ['id_period','carrier','fare_dir','passenger']
sfo_lax = sfo_lax[to_keep]

# keep if carrier = AA, UA, WN, US, DL, NW
dframe = dframe[dframe['carrier'].isin(['AA', 'UA', 'WN', 'US', 'DL', 'NW'])]

# create histogram of direct fares and passengers
sns.set_context("notebook", font_scale=1.1)
sns.set_style("ticks")

sns.lmplot('fare_dir', 'passenger', 
           data=dframe, 
           fit_reg=False, 
           hue="carrier",  
           scatter_kws={"marker": "D", 
                        "s": 25},
           size=5,
           aspect=2)

plt.title('Scatter of SFO-LAX Price & Quantity, 2005-2012')
plt.xlabel('Direct Fares')
plt.ylabel('Passengers Per Quarter')
plt.ylim(0,60000)
plt.xlim(0,1500)
plt.savefig('Python/sfo_lax_scatter.pdf')



