"""When attempting to model text, it is important to be able to ex- tract features of the text for analysis. 
A powerful tool for extracting text features (as well as for searching, replacing, and performing other text-based tasks) is Regular Expression (regex). 
For this assignment, your job is to process features of emails sent and received by Enron employees during the investigation into fraud- ulent activity by Enron executives in the early 2000’s using regular ex- pressions. 
Given emails from a single employee, generate the following information for each email:
Extract the text of the email into one feature
Create a column labelled “worry” containing the following values: 1 if some form of the word “worry” is contained in the text of the email, 0 otherwise
Create a column labelled “trouble” with the following values: 1 if some form of the word “trouble” is contained in the text of the email, 0 otherwise
Create a column containing the number of recipients of the email
Create a column labelled “sent” with the following values: 1 if the email was sent by the user, 0 otherwise Submit your code, as well a csv containing the new columns, to Canvas when you complete this assignment."""

"""import the necessary packages"""
import pandas as pd 
import re


# In[59]:


"""read the file into the main dataframe"""
data = pd.read_csv('Link to the file') #download the file in the same repo. Insert the local link to the file here
data = data.loc[:,'text'] #choose only the text column
length = len(data)
length #get the length of the dataframe


# In[60]:


"""To get only the text of the email. I noticed the pattern that the real text starts after nsf or PST, followed by \n\n"""
text = [] #a placeholder array
for i in range (0,length):
    try:
        temp = re.search(r'(?:(nsf\n\n|PST\n\n).*)((?:\n?).*)+(.*)', data[i], re.IGNORECASE).group()[5:] 
    except:
        temp = None
    #temp = re.search(r'(?:(nsf\n\n).*)((?:\n).*)+(.*)',data[i])
    #temp = temp.group()
    #temp = temp[5:]    
    text.append(temp)
Text = pd.DataFrame(text, columns = ['Text']) #turn it into a dataframe and name the column Text


# In[61]:


"""Check if the text has any variation of the word 'worry'"""
worry = []
for i in range (0,length):
    test = 0
    patterns = ["worry", "worried", "worrying", "worrisome"]
    for pattern in patterns:
        if re.search(pattern, text[i], re.IGNORECASE): #search any of the item in the patterns array
            test += 1
    if test == 0:
        worry.append(0)
    else:
        worry.append(1)
        
Worry = pd.DataFrame(worry, columns = ['Worry']) #turn it into a dataframe and name the column 'Worry'


# In[62]:


"""Check if the text has any variation of the word 'trouble'"""
trouble = []
for i in range (0,length):
    test = 0
    patterns = ["trouble", "troublesome", "troubling", "troubled"]
    for pattern in patterns:
        if re.search(pattern, text[i], re.IGNORECASE): #search any of the item in the patterns array
            test += 1
    if test == 0:
        trouble.append(0)
    else:
        trouble.append(1)
Trouble = pd.DataFrame(trouble, columns = ['Trouble']) #turn it into a dataframe and name the column 'Trouble'


# In[63]:


"""check if the sender is Stacey White"""
testfrom = []
for i in range (0,length):
    try:
        temp = re.search(r'(?:(From:).*)', data[i], re.IGNORECASE).group()[6:] #get the From part of the emails
    except:
        temp = None
    testfrom.append(temp)
senttest = []
for i in range (0, len(testfrom)):
    test = 0
    patterns = "stacey.white@enron.com" 
    if testfrom[i] == patterns: #check if the sender is Stacey White
        test += 1
    if test == 0:
        senttest.append(0)
    else:
        senttest.append(1)
Sent = pd.DataFrame(senttest, columns = ['Sent']) #turn it into a dataframe and name the column Sent


# In[64]:


"""Count how many emails there are in to, Cc and Bcc areas"""
testemail = [] #placeholder array
for i in range (0,length):
    """This part is to get all text from To to X-From.
    There can be no '\n\ between To and X-From. That's why the formula has two parts"""
    try: 
        temp = re.search(r'(?:(To:).*)(?:(X-From:))|(?:(To:).*)((?:\n).*)+(?:(X-From:))', data[i]).group()[4:][:-8]
    except:
        temp = None
    testemail.append(temp)
result = []
for i in range (0, length):
    try:
        result.append(len(re.findall(r'@\w+.\w+',testemail[i]))) #count how many emails there are in the whole part
    except:
        result.append(0)
EmailCount = pd.DataFrame(result, columns = ['SentEmailCount']) #turn it into a dataframe and name the column SentEmailCount


# In[68]:


df = pd.concat([Text, Worry, Trouble, EmailCount, Sent ], axis=1) #concatenate the dataframes
df.to_csv('text.csv') #export to a csv

