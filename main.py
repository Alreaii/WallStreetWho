from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import praw
import os
import datetime
import pandas
import yfinance as yf
import matplotlib.pyplot as plt

reddit = praw.Reddit(    
    client_id = os.environ['clientid'],
    client_secret = os.environ['clientsecret'],
    user_agent = "linux:com.replit.vader:v0.01 (by u/Tomtidee)",
)
subreddits = ['StockMarket', "WallStreetBets"] #add subreddits to scrape from here

#lists 
threadnames = []
dates = []
compounds = []

def sentiment_scores(sentence):
  sid = SentimentIntensityAnalyzer()
  sentiment_dict = sid.polarity_scores(sentence)
  # print("Overall sentiment dictionary is : ", sentiment_dict)
  compounds.append(sentiment_dict["compound"])
	# print(sentiment_dict['neg']*100, "% Negative")
	# print(sentiment_dict['neu']*100, "% Neutral")
	# print(sentiment_dict['pos']*100, "% Positive")

def redditscraper(): 
  for newthreads in reddit.subreddit("stockmarket").new(limit = 200):
    threadnames.append(newthreads.title)
    newtimestamp = str(datetime.date.fromtimestamp(newthreads.created_utc))
    dates.append(newtimestamp)

  # for topthreads in reddit.subreddit("stockmarket").top(limit = 25): # Only if you want to scrape from top threads as well!! this doesn't necessarily corrolate with date 
  #   threadnames.append(topthreads.title)
  #   toptimestamp = str(datetime.date.fromtimestamp(topthreads.created_utc))
  #   dates.append(toptimestamp) 

def stockscraper():
  data = yf.download("SPY", start = dates[len(dates)-1], end = dates[0]) 
  print(data)
  return data
  #since dates is already sorted the 0th index is the most recent while the last index is the oldest


def determinemood(meanCompound):
  if meanCompound >= 0.025:
    return "Positive"
  elif meanCompound <= - 0.025 :
    return "Negative"
  else:
    return "Neutral"

if __name__ == "__main__" :
  redditscraper()
  print(dates)
  data = stockscraper()
  data = data.reset_index(level=0)
  for titles in range(len(threadnames)):
    vaderfeeder = threadnames[titles]
    sentiment_scores(vaderfeeder)
    meanCompound = sum(compounds) / len(compounds) #finds mean of all compound scores from vader algorithm
  determinemood(meanCompound)

# plt.plot(dates, meanCompound, label = "Sentiments")
# plt.plot(data.iloc[:, 0], data.iloc[:, 4])
# plt.show()
