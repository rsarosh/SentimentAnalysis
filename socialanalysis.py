# -*- coding: utf-8 -*-
"""SocialAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rkwu3k-eRht0Dj7MXfih6nvWk2FB8RmA
"""

import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
from google.colab import data_table
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use ('fivethirtyeight')

#load the data
from google.colab import files
uploaded = files.upload()

#read the data
log = pd.read_csv ('twitterLogin.csv')
#print (log)

#Get the Twtitter credentials
consumerKey = log ['consumerKey'][0]
consumerSecret = log ['consumerSecret'][0]
accessToken = log ['accessToken'][0]
accessTokenSecret = log ['accessTokenSecret'][0]

#Authenticate 
auth = tweepy.OAuthHandler (consumerKey, consumerSecret)
auth.set_access_token (accessToken, accessTokenSecret)
api = tweepy.API (auth)

#get the tweets
posts = api.search (q='#MachE', lang='en', rpp=100)
#print them to check
#for tweet in posts [0:15]:
#  print (tweet.text + '\n')

#create a dataframe with a column name tweets
df = pd.DataFrame ([tweet.text for tweet in posts], columns= ['Tweets'])
df.head()

#clean the text
def cleanText (text):
  text = re.sub (r'@[A-Za-z0-9]+', '', text) #remove @ mentions
  text = re.sub(r'#','', text) #remove the # symbol
  text = re.sub(r'RT[\s]+','', text) #remove the RT symbol
  #text = re.sub(r'https:\/\/\S+','', text) #remove the hyper link
  #text = re.sub(r'Mustang','', text) #remove the hyper link
  #text = re.sub(r'Ford','', text) #remove the hyper link
  #text = re.sub(r'MachE','', text) #remove the hyper link
  return text

#clean the text
df['Tweets'] = df['Tweets'].apply (cleanText)
#show the cleaned Text
#df

#Create a funciton to get the subjectivity

def getsub(text):
    return TextBlob(text).sentiment.subjectivity

def getpol(text):
    return TextBlob(text).sentiment.polarity

#create two new columns 
df['sub'] = df['Tweets'].apply (getsub)
df['pol'] = df['Tweets'].apply (getpol)

#df

# visual word cloud
allWords = ' '.join ([twts for twts in df['Tweets']])
wordCloud = WordCloud (width = 1300, height=900, random_state = 21, max_words=40, max_font_size= 130).generate (allWords)
plt.imshow (wordCloud, interpolation='bilinear')
plt.axis ('off')
plt.show()

#Create a function to compute the negative, neutral and positive analysis
def getAnalysis (score):
    if score < 0 :
        return '-'
    elif score == 0:
        return ''
    else:
      return '+'

df ['Analysis'] = df ['pol'].apply (getAnalysis)

#show the dataframe as Data Table
data_table.DataTable(df,  num_rows_per_page=10)

# plot the polarity and subjectivity
plt.figure (figsize=(8,6))
for i in range(0, df.shape[0]):
  plt.scatter (df['pol'][i], df['sub'][i], color='Blue')

plt.title ('Sentiment Analysis')
plt.xlabel ('Pol')
plt.ylabel ('sub')
plt.show()

