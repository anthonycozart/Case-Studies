# data from: http://www.crowdflower.com/data-for-everyone
# quick plotting of twitter sentiment and stock price

import pandas as pd
from pandas import Series,DataFrame,to_datetime
import numpy as np

from datetime import date
from pandas.io.data import DataReader

import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# load data
url = 'http://cdn2.hubspot.net/hub/346378/file-2545951097-csv/DFE_CSVs/Airline-Sentiment-2-w-AA.csv?t=1458080228879'
dframe = pd.read_csv(url)

# convert tweet_created to datetime object
dframe['tweet_created'] = to_datetime(dframe['tweet_created'])
dframe['tweet_date'] = dframe['tweet_created'].values.astype('datetime64[D]')

# convert airline_sentiment to indicators
dframe['positive'] = np.where(dframe['airline_sentiment']=='positive',1,0)
dframe['neutral'] = np.where(dframe['airline_sentiment']=='neutral',1,0)
dframe['negative'] = np.where(dframe['airline_sentiment']=='negative',1,0)

# grab just key columns
to_keep = ['airline', 'tweet_date', 'positive', 'neutral', 'negative']
clean_dframe = dframe[to_keep]

# collapse to day level
by_day = clean_dframe.groupby(['tweet_date'],as_index=False).mean()
by_day_airline = clean_dframe.groupby(['tweet_date','airline'],as_index=False).mean()

# pivot
bda_negative = by_day_airline.pivot('tweet_date','airline','negative')

# plot
airlines = ['Delta','Southwest','US Airways','United','Virgin America']
bda_negative.plot(bda_negative.index,airlines,linestyle='--',figsize=(12,9))
plt.ylabel('% Negative')
plt.xlabel('Date')
plt.title('% of Tweets with Negative Sentiment, by Airline')
plt.savefig('airline_sentiment.pdf', bbox_inches='tight')

# grab stock data for all in list of airlines
start = date(2015,2,17)
end = date(2015,2,24)
tickers = ['DAL','LUV','AAL','UAL','VA']
prices = DataReader(tickers,'yahoo',start,end)['Adj Close']

# rename columns, so that they are airline names, not tickers
prices.columns = ['US Airways Price','Delta Price','Southwest Price','United Price','Virgin America Price']

# join stock data to twitter sentiment data
joined = pd.merge(bda_negative,prices,left_index=True,right_index=True)

# plot to see co-movements
united = ['United', 'United Price']
joined.plot(joined.index,united,linestyle='--',figsize=(12,9))

# use broken axis?
# with more days of data, create normalized variables, calculated as deviation from all airline average sentiment levels
