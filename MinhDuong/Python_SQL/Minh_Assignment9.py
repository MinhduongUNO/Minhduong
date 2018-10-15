# -*- coding: utf-8 -*-
"""

Data Frames and SQL allow us to store our data very efficiently on a database, and to quickly retrieve and 
work with that data to solve real research questions. 
In this lab, we will work with raw data to practice importing data into Data Frames, and use SQL (via pandasql) to clean that data.
1. Import the data from assignment7.csv into a dataframe
2. Using pandasql, create an aggregated dataset, taking averages over the area variable
3. Which area code has the highest value for churn?
4. Without using pandasql, reduce the dataset to the following data:
• Accounts in California (CA)
• Accounts with accLen greater than 100
• Only keep the area, vmMessages, dayCalls, eveCalls, night- Calls, intlCalls, and churn columns
• Create a new column called allCalls, which is the sum of day- Calls, nightCalls, and intlCalls
• Restric the dataset one more time to only contain the area, vmMessages, allCalls, and churn columns
5. Print the head of all three datasets, so that I can verify your results
"""
import pandas as pd #import pandas
from pandasql import sqldf  #importing pandasql
pysqldf = lambda q: sqldf(q, globals()) #create first pysqldf to translate sql code into data frame

"""read the csv into a dataframe"""
data = pd.read_csv('/Users/camapcon/Box Sync/Tools for Data Analysis/assignment9.csv')

select = """SELECT area, AVG(vmMessages) AS avg_vmMessages, AVG(dayMinutes) AS avg_dayMinutes, AVG(dayCalls) AS avg_dayCalls, AVG(dayCharge), AVG(eveMinutes), AVG(eveCalls), AVG(eveCharge), AVG(nightMinutes), AVG(nightCalls), AVG(nightCharge), AVG(intlMinutes), AVG(intlCalls), AVG(intlCharge), AVG(churn) as churn FROM data GROUP BY area;
        """ #Using pandasql, create an aggregated dataset, taking averages over the area variable. Only a few columns are named to save time :D
averagedata = pysqldf(select) 
print(averagedata)

#looking for the area code that has the highest value for churn
select1 = """SELECT area FROM averagedata WHERE churn = (SELECT MAX(churn) FROM averagedata);"""
#select1 = """SELECT TOP 1 churn FROM averagedata"""
highest_churn = pysqldf(select1)
print(highest_churn)

"""This part is to answer question number #4 above"""
newdata = data.loc[data['state'] =='CA',['state', 'accLen','area', 'vmMessages', 'dayCalls', 'eveCalls', 'nightCalls', 'intlCalls', 'churn']]  #choose only rows whose state value is CA
newdata = newdata.loc[newdata['accLen'] >100,['state', 'accLen','area', 'vmMessages', 'dayCalls', 'eveCalls', 'nightCalls', 'intlCalls', 'churn']] #choose only rows whose accLen is bigger than 100

newdata['allCalls'] = newdata['dayCalls'] + newdata['nightCalls'] + newdata['intlCalls'] #Create a new column called allCalls, which is the sum of day- Calls, nightCalls, and intlCalls
newdata = newdata.loc[:,['area', 'vmMessages', 'allCalls', 'churn']] #Restrict the dataset one more time to only contain the area, vmMessages, allCalls, and churn columns
#print all the three dataset head

data.head()
averagedata.head()
newdata.head()

