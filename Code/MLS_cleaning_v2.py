# Standard Imports
import pandas as pd
import numpy as np
from pandas import Series,DataFrame,to_datetime

# data from: https://github.com/openfootball/major-league-soccer

# To Do:
# games played, wins, draws, losses, for, against, goal difference, points, form
# create table for results at the end of each season. Also create for each week
# calculate likelihood of missing playoffs, using prior year's data, for each week?
# i.e., be able to say, based on x, these teams have a 25-30% of missing the playoffs.

# do this by looping through each team. For example, the first team is CD Chivas USA.
# grab all games in which it was the home team or away team
# calculate the running totals for games played, wins, draws, losses, for, against, ....
# do this for all teams, and combine together.
# this, however, does not take into account the strength of schedule of the remaining games.
# accomplish this by merging in data?


# use loop, to do the same on all data
# for year in range(2005,2014):
# filepath = 'Data/mls'+year+'.csv'	

df = pd.read_csv('Data/mls2005.csv', header=None)
df.columns = ['text']

# identify week of each row observation, extracting the first entry per group and filling down
def find_week(week,text):
    if week in text:
        num = text[4:]
        return num
    else:
        return 0

df['Week'] = df.apply(lambda x: find_week('Week',x['text']), axis=1)
df['Week'].replace(0, np.nan, inplace=True)
df['Week'].fillna(method='ffill', inplace=True)

df['Week'] = df['Week'].astype(float)

# split text into date info and game info
dateinfo = []
gameinfo = []
for row in df['text']:
    dateinfo.append(row[:15])
    gameinfo.append(row[16:])

df['dateinfo'] = dateinfo
df['gameinfo'] = gameinfo

# now drop rows that just contain 'week' and the week number
df = df[df.gameinfo != ""]

# split game info using "-"
teams = df['gameinfo'].apply(lambda x: pd.Series(x.split('-')))
teams.columns = ['home','away']

hometeam=[]
homescore=[]
for row in teams['home']:
	hometeam.append(row[:-1])
	homescore.append(row[-1])

awayteam=[]
awayscore=[]
for row in teams['away']:
	awayteam.append(row[1:])
	awayscore.append(row[0])

df['hometeam']=hometeam
df['awayteam']=awayteam
df['homescore']=homescore
df['awayscore']=awayscore

df['homescore'] = df['homescore'].astype(float)
df['awayscore'] = df['awayscore'].astype(float)

# drop unformatted columns
df.drop(['text','gameinfo'],axis=1,inplace=True)

# remove trailing spaces
df['hometeam'] = df['hometeam'].map(str.strip)
df['awayteam'] = df['awayteam'].map(str.strip)

teamz = 'CD Chivas USA'
df[(df.hometeam == teamz) | (df.awayteam == teamz)]

# use indicator for whether the team is at home to make the logical statements easier to understand
df['home'] = np.where(df.hometeam==teamz,1,0)

#### Individual Matches ####

# Win, Loss, Draw
def win_categorizer(home, homescore, awayscore):
	if home == 1 & (homescore > awayscore):
		return 1
	elif home == 0 & (homescore < awayscore):
		return 1
	else:
		return 0

def loss_categorizer(home, homescore, awayscore):
	if home == 1 & (homescore < awayscore):
		return 1
	elif home == 0 & (homescore > awayscore):
		return 1
	else:
		return 0

## XXX FIX
df['win'] = df.apply(lambda x: win_categorizer(x['home'],x['homescore'],x['awayscore']), axis=1)
df['loss'] = df.apply(lambda x: loss_categorizer(x['home'],x['awayscore'],x['homescore']), axis=1)
df['draw'] = np.where(df['homescore']==df['awayscore'],1,0)

# Goals For, Goals Against, Goal Difference
def goal_attribution(home, homescore, awayscore):
	if home == 1:
		return homescore
	else:
		return awayscore

df['goalsfor'] = df.apply(lambda x: goal_attribution(x['home'],x['homescore'],x['awayscore']), axis=1)
df['goalsagainst'] = df.apply(lambda x: goal_attribution(x['home'],x['awayscore'],x['homescore']), axis=1)
df['goalsdiff'] = df['goalsfor'] - df['goalsagainst']

# Points
def point_scoring(win,draw):
    if win == 1:
        return 3
    elif draw == 1:
        return 1
    else:
        return 0

df['points'] = df.apply(lambda x: point_scoring(x['win'],x['draw']), axis=1)


#### Cumulative Totals ####

# Team
df['Team'] = teamz

# Games Played
df['temp'] = 1
df['gamesplayed'] = df['temp'].cumsum()

# Wins, Draws, Losses
df['total_wins'] = df['win'].cumsum()
df['total_draws'] = df['draw'].cumsum()
df['total_losses'] = df['loss'].cumsum()

# Goals For, Goals Against, Goal Difference
df['total_goalsfor'] = df['goalsfor'].cumsum()
df['total_goalsagainst'] = df['goalsagainst'].cumsum()
df['total_goalsdiff'] = df['goalsdiff'].cumsum()

# Points
df['total_points'] = df['points'].cumsum()




