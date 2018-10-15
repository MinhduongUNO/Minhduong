
"""
Created on Tue Apr  3 18:36:05 2018

@author: Minh Duong
Class: ECON8320
Assignment: Semester Project

"""

import requests
import numpy as np
import plotly as py
from bs4 import BeautifulSoup
import pandas as pd 
import plotly.graph_objs as go
import statsmodels.api as sm
from pandasql import sqldf  #importing pandasql
pysqldf = lambda q: sqldf(q, globals()) #create first pysqldf to translate sql code into data frame
"""
This program is designed to scrape data for 2017 NBA season from basketball-reference.com website. 

The data taken from the website will be used to analyze the top 10 players in each category and 
find out if there is any correlation between some of the key categories and points. 

The key categories can be:
    - 3 Point %
    - 2 point %
    - Free throw %
    - Turnover
    - Assist
    
Classification by team or position can also be taken into consideration
"""
page = requests.get('https://www.basketball-reference.com/leagues/NBA_2017_totals.html') #get the URL
soup = BeautifulSoup(page.text, 'html.parser') #set up a soup. This is to get the whole's website content

with open('basketballresults.csv', 'w') as f: #set up the csv and add the header columns
    f.write("Player,Position,Age,Team,GamePlayed,MinutesPlayed,FGM,FGA,FGPct,ThreePM,ThreePA,ThreePct,TwoPM,TwoPA,TwoPct,eFGPct,FT,FTA,FTPct,ORB,DRB,Assist,Steal,Block,Turnover,Foul,Points\n")
    
table = soup.find(class_='stats_table') #get the table in question
"""The table is divided into two parts. The reason is that rows are named differently throughout the whole table. 
    - full_table
    - italic_text partial_table
    - thread. This is where they show the headers"""
    
tr_list = table.find_all('tr', attrs={'class':'full_table'}) 

with open('basketballresults.csv', 'a') as f: #this is where we parse the data

    for i in range(len(tr_list)):  #the loop used to go from one row to another
        chosen = tr_list[i] 
        name = chosen.find('td', attrs={'data-stat':'player'}) #get the name of the player
        name = name.find('a') #get the a tag
        name = name.string #get the string in the a tag since the name is tucked in there
        position = chosen.find('td', attrs={'data-stat':'pos'})
        position = position.string #get the position 
        age = chosen.find('td', attrs={'data-stat':'age'})
        age = age.string #get the age
        team = chosen.find('td', attrs={'data-stat':'team_id'})
        if (team.find('a') is None): #this is to get the team name. For the majority of the records, the team name is tucked in the a tag. However, a few records' team name is not
            team = team.string
        else:
            team = team.find('a')            
            team = team.string
        game = chosen.find('td', attrs={'data-stat':'g'})
        game = game.string #get the number of games played
        minute = chosen.find('td', attrs={'data-stat':'mp'})
        minute = minute.string #get the minutes played
        FGM = chosen.find('td', attrs={'data-stat':'fg'})
        if (FGM.string is None): #Some field goal made is blank 
            FGM = "" #"N/A"
        else:
            FGM = FGM.string #get the FG
        FGA = chosen.find('td', attrs={'data-stat':'fga'})
        if (FGA.string is None): #Some field goal attempted is blank 
            FGA = "" #"N/A"
        else:
            FGA = FGA.string #get the FG attempted
        FG = chosen.find('td', attrs={'data-stat':'fg_pct'})
        if (FG.string is None): #Some field goal percentage is blank 
            FG = "" #"N/A"
        else:
            FG = FG.string #get the FG%
        ThreePM = chosen.find('td', attrs={'data-stat':'fg3'})
        if (ThreePM.string is None): #Some three point made is blank
            ThreePM = ""
        else:
            ThreePM = ThreePM.string #get the three point made
        PA3 = chosen.find('td', attrs={'data-stat':'fg3a'})
        PA3 = PA3.string #get the 3 point attempt count    
        FG3 = chosen.find('td', attrs={'data-stat':'fg3_pct'})
        if (FG3.string is None): #Some three point percentage is blank
            FG3 = ""
        else:
            FG3 = FG3.string #get the three point %
        TwoPM = chosen.find('td', attrs={'data-stat':'fg2'})
        if (TwoPM.string is None): #some 2 point made is blank
            TwoPM = ""
        else:
            TwoPM = TwoPM.string #get the 2 point made count
        TwoPA = chosen.find('td', attrs={'data-stat':'fg2a'})
        if (TwoPA.string is None): #some 2 point attempted is blank
            TwoPA = ""
        else:
            TwoPA = TwoPA.string #get the 2 point attempted count
        FG2 = chosen.find('td', attrs={'data-stat':'fg2_pct'})
        if (FG2.string is None): #some 2 point percentage is blank
            FG2 = ""
        else:
            FG2 = FG2.string #get the 2 point field goal %
        eFG = chosen.find('td', attrs={'data-stat':'efg_pct'})
        if (eFG.string is None): #this is to get the real field goal %. Some records have it blank
            eFG = ""
        else:
            eFG = eFG.string #get the real field goal %
        FTM = chosen.find('td', attrs={'data-stat':'ft'})
        if (FTM.string is None): #some free throws made are blank
            FTM = ""
        else:
            FTM = FTM.string #get the free throw made  
        FTA = chosen.find('td', attrs={'data-stat':'fta'})
        if (FTA.string is None): #some free throws attempted are blank
            FTA = ""
        else:
            FTA = FTA.string #get the free throw attempted  
        FT = chosen.find('td', attrs={'data-stat':'ft_pct'})
        if (FT.string is None): #some free throws are blank
            FT = ""
        else:
            FT = FT.string #get the free throw
        ORB = chosen.find('td', attrs={'data-stat':'orb'})
        ORB = ORB.string #get the offensive rebounds
        DRB = chosen.find('td', attrs={'data-stat':'drb'})
        DRB = DRB.string #get the defensive rebounds
        ast = chosen.find('td', attrs={'data-stat':'ast'})
        ast = ast.string #get the assist count
        stl = chosen.find('td', attrs={'data-stat':'stl'})
        stl = stl.string #get the steal count
        blk = chosen.find('td', attrs={'data-stat':'blk'})
        blk = blk.string #get the block count
        tov = chosen.find('td', attrs={'data-stat':'tov'})
        tov = tov.string #get the turnover count
        foul = chosen.find('td', attrs={'data-stat':'pf'})
        foul = foul.string #get the foul count
        points = chosen.find('td', attrs={'data-stat':'pts'})
        points = points.string #get the number of points
        result = name + "," #add every field together and get ready for writing the values into the csv
        result += position + ","
        result += age + ","
        result += team + ","
        result += game + ","
        result += minute + ","
        result += FGM + ","
        result += FGA + ","
        result += FG + ","
        result += ThreePM + ","
        result += PA3 + ","
        result += FG3 + ","
        result += TwoPM + ","
        result += TwoPA + ","
        result += FG2 + ","
        result += eFG + ","
        result += FTM + ","
        result += FTA + ","
        result += FT + ","
        result += ORB + ","
        result += DRB + ","
        result += ast + ","
        result += stl + ","
        result += blk + ","
        result += tov + ","
        result += foul + ","
        result += points + "\n"
        f.write(result)   #write the values into csv 
    
tr_list2 = table.find_all('tr', attrs={'class':'italic_text partial_table'})
"""this is to get all the rows named italic_text partial table. The same code is being used as the code above"""
with open('basketballresults.csv', 'a') as f:
    for i in range(len(tr_list2)):
        chosen = tr_list[i] 
        name = chosen.find('td', attrs={'data-stat':'player'}) #get the name of the player
        name = name.find('a') #get the a tag
        name = name.string #get the string in the a tag since the name is tucked in there
        position = chosen.find('td', attrs={'data-stat':'pos'})
        position = position.string #get the position 
        age = chosen.find('td', attrs={'data-stat':'age'})
        age = age.string #get the age
        team = chosen.find('td', attrs={'data-stat':'team_id'})
        if (team.find('a') is None): #this is to get the team name. For the majority of the records, the team name is tucked in the a tag. However, a few records' team name is not
            team = team.string
        else:
            team = team.find('a')            
            team = team.string
        game = chosen.find('td', attrs={'data-stat':'g'})
        game = game.string #get the number of games played
        minute = chosen.find('td', attrs={'data-stat':'mp'})
        minute = minute.string #get the minutes played
        FGM = chosen.find('td', attrs={'data-stat':'fg'})
        if (FGM.string is None): #Some field goal made is blank 
            FGM = "" #"N/A"
        else:
            FGM = FGM.string #get the FG
        FGA = chosen.find('td', attrs={'data-stat':'fga'})
        if (FGA.string is None): #Some field goal attempted is blank 
            FGA = "" #"N/A"
        else:
            FGA = FGA.string #get the FG attempted
        FG = chosen.find('td', attrs={'data-stat':'fg_pct'})
        if (FG.string is None): #Some field goal percentage is blank 
            FG = "" #"N/A"
        else:
            FG = FG.string #get the FG%
        ThreePM = chosen.find('td', attrs={'data-stat':'fg3'})
        if (ThreePM.string is None): #Some three point percentage is blank
            ThreePM = ""
        else:
            ThreePM = ThreePM.string #get the three point %
        PA3 = chosen.find('td', attrs={'data-stat':'fg3a'})
        PA3 = PA3.string #get the 3 point attempt count    
        FG3 = chosen.find('td', attrs={'data-stat':'fg3_pct'})
        if (FG3.string is None): #Some three point percentage is blank
            FG3 = ""
        else:
            FG3 = FG3.string #get the three point %
        TwoPM = chosen.find('td', attrs={'data-stat':'fg2'})
        if (TwoPM.string is None): #some 2 point made is blank
            TwoPM = ""
        else:
            TwoPM = TwoPM.string #get the 2 point made count
        TwoPA = chosen.find('td', attrs={'data-stat':'fg2a'})
        if (TwoPA.string is None): #some 2 point made is blank
            TwoPA = ""
        else:
            TwoPA = TwoPA.string #get the 2 point made count
        FG2 = chosen.find('td', attrs={'data-stat':'fg2_pct'})
        if (FG2.string is None): #some 2 point percentage is blank
            FG2 = ""
        else:
            FG2 = FG2.string #get the 2 point field goal %
        eFG = chosen.find('td', attrs={'data-stat':'efg_pct'})
        if (eFG.string is None): #this is to get the real field goal %. Some records have it blank
            eFG = ""
        else:
            eFG = eFG.string #get the real field goal %
        FTM = chosen.find('td', attrs={'data-stat':'ft'})
        if (FTM.string is None): #some free throws made are blank
            FTM = ""
        else:
            FTM = FTM.string #get the free throw made  
        FTA = chosen.find('td', attrs={'data-stat':'fta'})
        if (FTA.string is None): #some free throws attempted are blank
            FTA = ""
        else:
            FTA = FTA.string #get the free throw attempted  
        FT = chosen.find('td', attrs={'data-stat':'ft_pct'})
        if (FT.string is None): #some free throws are blank
            FT = ""
        else:
            FT = FT.string #get the free throw
        ORB = chosen.find('td', attrs={'data-stat':'orb'})
        ORB = ORB.string #get the offensive rebounds
        DRB = chosen.find('td', attrs={'data-stat':'drb'})
        DRB = DRB.string #get the defensive rebounds
        ast = chosen.find('td', attrs={'data-stat':'ast'})
        ast = ast.string #get the assist count
        stl = chosen.find('td', attrs={'data-stat':'stl'})
        stl = stl.string #get the steal count
        blk = chosen.find('td', attrs={'data-stat':'blk'})
        blk = blk.string #get the block count
        tov = chosen.find('td', attrs={'data-stat':'tov'})
        tov = tov.string #get the turnover count
        foul = chosen.find('td', attrs={'data-stat':'pf'})
        foul = foul.string #get the foul count
        points = chosen.find('td', attrs={'data-stat':'pts'})
        points = points.string #get the number of points
        result = name + "," #add every field together and get ready for writing the values into the csv
        result += position + ","
        result += age + ","
        result += team + ","
        result += game + ","
        result += minute + ","
        result += FGM + ","
        result += FGA + ","
        result += FG + ","
        result += ThreePM + ","
        result += PA3 + ","
        result += FG3 + ","
        result += TwoPM + ","
        result += TwoPA + ","
        result += FG2 + ","
        result += eFG + ","
        result += FTM + ","
        result += FTA + ","
        result += FT + ","
        result += ORB + ","
        result += DRB + ","
        result += ast + ","
        result += stl + ","
        result += blk + ","
        result += tov + ","
        result += foul + ","
        result += points + "\n"
        f.write(result)   #write the values into csv    

data = pd.read_csv('/Users/camapcon/basketballresults.csv') #read the file into a data frame
data = data.dropna() #remove all rows with NaN 
data['ThreePct'] = data['ThreePct'].astype('float64') #turn the values into float
data['TwoPct'] = data['TwoPct'].astype('float64') #turn the values into float
data['eFGPct'] = data['eFGPct'].astype('float64') #turn the values into float
data['FTPct'] = data['FTPct'].astype('float64') #turn the values into float
data['FGPct'] = data['FGPct'].astype('float64') #turn the values into float
data['FGA'] = data['FGA'].astype('float64') #turn the values into float
data['ThreePA'] = data['ThreePA'].astype('float64') #turn the values into float
data['TwoPA'] = data['TwoPA'].astype('float64') #turn the values into float
data['FTA'] = data['FTA'].astype('float64') #turn the values into float


# In[8]:


"""It seems that there are duplicated values in the file. This is to remove the duplicated values"""
data = data.iloc[:439] 


# In[16]:


data.to_csv("basketball_rewrite.csv", sep='\t') #write to a csv


# In[3]:


"""top 10 in field goal percentage among shooting guards with more than 20 games played"""
data_FGpct = data.loc[data['GamePlayed'] > 20] #get players who have more than 20 games played
data_FGpct = data_FGpct.loc[data_FGpct['Position'] == 'SG'] #get Guards only
data_FGpct = data_FGpct.nlargest(10, 'FGPct') #top 10 
data_FGpct = data_FGpct.sort_values(by=['FGPct'], ascending=False) #sorting
data_FGpct.loc[:,['Player','Position','GamePlayed','Team','FGPct']] #show the data frame


# In[4]:


"""top 10 in field goal percentage among small forwards with more than 20 games played"""
data_FGpct = data.loc[data['GamePlayed'] > 20] #get players who have more than 20 games played
data_FGpct = data_FGpct.loc[data_FGpct['Position'] == 'SF'] #get the Small Forwards
data_FGpct = data_FGpct.nlargest(10, 'FGPct') #top 10 
data_FGpct = data_FGpct.sort_values(by=['FGPct'], ascending=False) #sorting
data_FGpct.loc[:,['Player','Position','GamePlayed','Team','FGPct']]


# In[5]:


"""top 10 in field goal percentage among point guards with more than 20 games played"""
data_FGpct = data.loc[data['GamePlayed'] > 20]
data_FGpct = data_FGpct.loc[data_FGpct['Position'] == 'PG']
data_FGpct = data_FGpct.nlargest(10, 'FGPct')
data_FGpct = data_FGpct.sort_values(by=['FGPct'], ascending=False)
data_FGpct.loc[:,['Player','Position','GamePlayed','Team','FGPct']]


# In[6]:


"""top 10 in field goal percentage among power forwards with more than 20 games played"""
data_FGpct = data.loc[data['GamePlayed'] > 20]
data_FGpct = data_FGpct.loc[data_FGpct['Position'] == 'PF']
data_FGpct = data_FGpct.nlargest(10, 'FGPct')
data_FGpct = data_FGpct.sort_values(by=['FGPct'], ascending=False)
data_FGpct.loc[:,['Player','Position','GamePlayed','Team','FGPct']]


# In[8]:


"""Regression for Points as dependent variable and the following as independent variables: eFGPct, ThreePA, Assist, Turnover, TwoPct, Position as a categorical"""
reg = sm.ols("Points ~ eFGPct + ThreePA + Assist + Turnover + TwoPct + C(Position)", data=data).fit()
print(reg.summary())


# In[9]:


"""Regression for Points as dependent variable and the following as independent variables: eFGPct, ThreePA, Assist, ORB, 
Position as a categorical"""
reg = sm.ols("Points ~ eFGPct + ThreePA + Assist + ORB + C(Position)", data=data).fit()
print(reg.summary())


# In[10]:


"""Get accumulated values per teams. For absolute values, take the sume and divide it by 82"""
select = """SELECT Team, SUM(Points)/82 AS AvgPoints, SUM(Assist)/82 AS AvgAssist, SUM(Steal)/82 AS AvgSteal, SUM(Block)/82 AS AvgBlock, SUM(Turnover)/82 AS AvgTO, SUM(DRB)/82 AS AvgDRB, SUM(ORB)/82 AS AvgORB, SUM(FGM) AS FGM, SUM(FGA) AS FGA, SUM(ThreePM) AS ThreePM, SUM(ThreePA) AS ThreePA, SUM(TwoPM) AS TwoPM, SUM(TwoPA) AS TwoPA, SUM(FT) AS FTM, SUM(FTA) AS FTA FROM data WHERE Team not in ('TOT') GROUP BY Team"""
df2 = pysqldf(select)
select = """SELECT Team, AvgPoints, AvgAssist, AvgSteal, AvgBlock, AvgTO, AvgDRB, AvgORB, FGM / FGA AS FGPct, ThreePM/ThreePA AS ThreePct,TwoPM/TwoPA AS TwoPct, FTM/FTA AS FTPct FROM df2"""
df2 = pysqldf(select)
df2


# In[11]:


"""Regression on the team performance. Dependent variable is Points. The following are independent variables: Assist, ORB, DRB, FGPct, ThreePct"""
reg = sm.ols("AvgPoints ~ AvgAssist + AvgORB + AvgDRB + FGPct + ThreePct", data=df2).fit()
print(reg.summary())


# In[12]:


"""show points and assists per game per team"""
trace1 = go.Bar(  #The first column - Level III Salary
    x=df2['Team'],
    y=df2['AvgPoints'],
    name='Average Points per Game'
) 
trace2 = go.Bar( #The second column - No Dependent Status
    x=df2['Team'],
    y=df2['AvgAssist'],
    name='Average Assists per Game'
)
data4 = [trace1, trace2] #read four columns into one data
layout4 = go.Layout( #starting to plot a grouped bar chart
    title='Team performance',
    barmode='group'
)

fig = go.Figure(data=data4, layout=layout4)
py.iplot(fig, filename='grouped-bar')


# In[14]:


"""look at shooting performance by team"""
trace1 = go.Bar(  #The first column - Level III Salary
    x=df2['Team'],
    y=df2['FGPct'],
    name='Average Field Goal Percentage'
) 
trace2 = go.Bar( #The second column - No Dependent Status
    x=df2['Team'],
    y=df2['ThreePct'],
    name='Average Three Pointer Percentage'
)
trace4 = go.Bar( #The third column - Pre Wage
    x=df2['Team'],
    y=df2['FTPct'],
    name='Average Free Throw Percentage'
)
trace3 = go.Bar( #The fourth column - Wage
    x=df2['Team'],
    y=df2['TwoPct'],
    name='Average Two Pointer Percentage'
)
data4 = [trace1, trace2, trace3, trace4] #read four columns into one data
layout4 = go.Layout( #starting to plot a grouped bar chart
    title='Team performance',
    barmode='group'
)

fig = go.Figure(data=data4, layout=layout4)
py.iplot(fig, filename='grouped-bar')


# In[15]:


"""Top 10 in points scored"""
select4 = """SELECT Player, Position, GamePlayed, Team, Points, Points/GamePlayed as AvgPoint From data"""
data_point = pysqldf(select4)
data_point = data_point.nlargest(10, 'AvgPoint')
data_point = data_point.sort_values(by=['AvgPoint'], ascending=False)
data_point
#data_point.loc[:,['Player','Position','GamePlayed','Team','Points']]


# In[16]:


"""top 10 in field goal percentage with more than 20 games played"""
data_FGpct = data.loc[data['GamePlayed'] >20]
data_FGpct = data_FGpct.nlargest(10, 'FGPct')
data_FGpct = data_FGpct.sort_values(by=['FGPct'], ascending=False)
data_FGpct.loc[:,['Player','Position','GamePlayed','Team','FGPct']]


# In[17]:


"""top 10 in field goal percentage with more than 20 games played"""
data_threepct = data.loc[data['ThreePA'] >200]
data_threepct = data_threepct.nlargest(10, 'ThreePct')
data_threepct = data_threepct.sort_values(by=['ThreePct'], ascending=False)
data_threepct.loc[:,['Player','Position','GamePlayed','Team','ThreePA','ThreePct']]


# In[18]:


"""top 10 in field goal percentage with more than 20 games played"""
data_ftpct = data.loc[data['GamePlayed'] >20]
data_ftpct = data_ftpct.nlargest(10, 'FTPct')
data_ftpct = data_ftpct.sort_values(by=['FTPct'], ascending=False)
data_ftpct.loc[:,['Player','Position','GamePlayed','Team','FTPct']]


# In[19]:


"""top 10 in field goal percentage with more than 20 games played"""
data_efgpct = data.loc[data['GamePlayed'] >20]
data_efgpct = data_efgpct.nlargest(10, 'eFGPct')
data_efgpct = data_efgpct.sort_values(by=['eFGPct'], ascending=False)
data_efgpct.loc[:,['Player','Position','GamePlayed','Team','FGPct','eFGPct']]


# In[20]:


"""top 10 in field goal percentage with more than 20 games played"""
data_twopct = data.loc[data['GamePlayed'] >20]
data_twopct = data_twopct.nlargest(10, 'TwoPct')
data_twopct = data_twopct.sort_values(by=['TwoPct'], ascending=False)
data_twopct.loc[:,['Player','Position','GamePlayed','Team','TwoPct']]


# In[21]:


select4 = """SELECT Player, Position, GamePlayed, Team, Points, ORB, ORB/GamePlayed as AvgORB From data"""
data_orb = pysqldf(select4)
data_orb = data_orb.nlargest(10, 'AvgORB')
data_orb = data_orb.sort_values(by=['AvgORB'], ascending=False)
data_orb.loc[:,['Player','Position','GamePlayed','Team', 'ORB','AvgORB']]


# In[22]:


select4 = """SELECT Player, Position, GamePlayed, Team, Points, DRB, DRB/GamePlayed as AvgDRB From data"""
data_drb = pysqldf(select4)
data_drb = data_drb.nlargest(10, 'AvgDRB')
data_drb = data_drb.sort_values(by=['AvgDRB'], ascending=False)
data_drb.loc[:,['Player','Position','GamePlayed','Team','DRB', 'AvgDRB']]


# In[23]:


select4 = """SELECT Player, Position, GamePlayed, Team, Points, Assist, Assist/GamePlayed as AvgAssist From data"""
data_assist = pysqldf(select4)
data_assist = data_assist.nlargest(10, 'AvgAssist')
data_assist = data_assist.sort_values(by=['AvgAssist'], ascending=False)
data_assist.loc[:,['Player','Position','GamePlayed','Team','Assist','AvgAssist']]


# In[24]:


select4 = """SELECT Player, Position, GamePlayed, Team, Points, Steal, Steal/GamePlayed as AvgSteal From data"""
data_steal = pysqldf(select4)
data_steal = data_steal.loc[data_steal['GamePlayed'] >20]
data_steal = data_steal.nlargest(10, 'AvgSteal')
data_steal = data_steal.sort_values(by=['AvgSteal'], ascending=False)
data_steal.loc[:,['Player','Position','GamePlayed','Team','Steal','AvgSteal']]


# In[25]:


select4 = """SELECT Player, Position, GamePlayed, Team, Points, Turnover, Turnover/GamePlayed as AvgTO From data"""
data_to = pysqldf(select4)
data_to = data_to.loc[data_to['GamePlayed'] >20]
data_to = data_to.nlargest(10, 'AvgTO')
data_to = data_to.sort_values(by=['AvgTO'], ascending=False)
data_to.loc[:,['Player','Position','GamePlayed','Team','Turnover','AvgTO']]


# In[26]:


select4 = """SELECT Player, Position, GamePlayed, Team, Points, Block, Block/GamePlayed as AvgBlock From data"""
data_block = pysqldf(select4)
data_block = data_block.loc[data_block['GamePlayed'] >20]
data_block = data_block.nlargest(10, 'AvgBlock')
data_block = data_block.sort_values(by=['AvgBlock'], ascending=False)
data_block.loc[:,['Player','Position','GamePlayed','Team','Block','AvgBlock']]

