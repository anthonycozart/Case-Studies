import pandas as pd
import numpy as np
zips = pd.read_csv('geo.csv')

# split up geojson object, by the first bracket ('[')
for i in range(1000):
    zips['pair'+str(i)] = zips['geojson'].str.split('[').str[i]
# get rid of trailing bracket (']'), starting at pair4
for i in range(4,1000):
    zips['pair'+str(i)] = zips['pair'+str(i)].str.split(']').str[0]

# create list of all lat/lon pair columns
pairs = []
for i in range(4,1000):
    pairs.append('pair'+str(i))

# reshape wide to long, using pd.melt
zips_long = pd.melt(zips, id_vars=['postal_code'], value_vars=list(pairs))

zips_long.shape
zips_long.dropna(axis=0, inplace=True)
zips_long.shape
zips_long.head(5)
type(zips_long.value)

# split value variable, into separate columns for lat and for lon
latlon = zips_long['value'].apply(lambda x: pd.Series(x.split(',')))
latlon.columns = ['Lat','Lon']

zips_long['Lat'] = latlon['Lat']
zips_long['Lon'] = latlon['Lon']

zips_long.drop(['variable','value'],axis=1,inplace=True)

# zips_long now contains just postal code, lat, and lon