from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy  import Stream
import json
import time
import pandas as pd
import matplotlib.pyplot as plt

'''
HOW TO GET ACCESS TOKEN, ACCESS TOKEN SECRET, CONSUMER KEY, CONSUMER KEY SECRET
1. GOTO "WWW.APPS.TWITTER.COM"
2. ENTER THE REQUIRED INFORMATION
3. GENERAT ALL THE CODES I.E ACCESS AND CONSUMER TOKENS

THE BELOW USER CREDENTIALS CODE SHOULD LOOK SOMETHING LIKE THIS
access_token='1920384-JADkjnkKJKnkKKKNN'
access_token_secret='ajkdsKnlnlnLKNklnLNlnnlNLNLNlNL'
consumer_key='EkjHjkhKHkjHkjhkHkHkHKlLJf'
consumer_secret='LlJJgFYdTYUKJJFYdTRUHJiHiguygyuGu'
'''
#variable contains user credentials
access_token='ENTER YOUR ACCESS TOKEN HERE'
access_token_secret='ENTER YOUR ACCESS SECRET HERE'
consumer_key='ENTER YOUR CONSUMER KEY HERE'
consumer_secret='ENTER YOUR CONSUMER SECRET CODE HERE'

#basic listener
class StdOutListener(StreamListener):
	def __init__(self,time_limit=60):
		self.start_time=time.time()
		self.limit=time_limit
		self.saveFile=open('twitter_data.txt','w')
		super(StdOutListener,self).__init__()
	def on_data(self,data):
		if (time.time()-self.start_time) < self.limit:
			self.saveFile.write(data)
			self.saveFile.write('\n')
			return True
		else:
			self.saveFile.close()
			return False
	def on_error(self,status):
		print status

#checking for positive as well as negetive words in a tweet
def word_in_text(text):
	pos_word=0
	neg_word=0
	
	#list of positive words
	positive_words=['happy','pleasure','celebrate','free','love','fun','great','peace','haha','award','success','enjoying','hero','positive','blessed','wonderful','gift','relax','bonus','lucky','a']
	
	#list of negetive words
	negetive_words=['negetive','fail','failure','torture','terrorist','victim','torture','criminal','cry','sick','suffer','sorrow','hurt','lose','injured','unhappy','heartbreak','die','violent','slave','a']
	
	text=text.lower()
	
	for i in range(len(positive_words)):
		if positive_words[i] in text:
			pos_word=pos_word+1
	for i in range(len(negetive_words)):
		if negetive_words[i] in text:
			neg_word=neg_word+1
	if pos_word > neg_word:
		return 1
	elif pos_word < neg_word:
		return 2
	else:
		return 3
		
if __name__=='__main__':
	
	#getting a trend from user
	print ("enter a trend to check whether its positive or negetive")
	trend=raw_input()
      print ("wait for 60 seconds")
	
	
	#twitter authentication
	l=StdOutListener()
	auth=OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token,access_token_secret)
	
	stream=Stream(auth,l)
	
	#line filter
	stream.filter(track=[trend])
	
	#tweets data path
	tweets_data_path='twitter_data.txt'
	tweets_data=[]
	tweets_file=open(tweets_data_path,"r")
	for line in tweets_file:
		try:
			tweet=json.loads(line)
			tweets_data.append(tweet)
		except:
			continue

    
	tweets=pd.DataFrame()
	
	#getting the json text
	tweets['text']=map(lambda tweet:tweet['text'],tweets_data)
	
	#checking each and every tweet and adding to a series
	tweets['pos']=tweets['text'].apply(lambda tweet:word_in_text(tweet))
	
	# 1. positive 2.negetive 
	#not considering neutral ones
	positivity=tweets['pos'].value_counts()[1]
	negetivity=tweets['pos'].value_counts()[2]

	#creating a pie chart
	labels = 'positive','negetive'
	sizes=[positivity,negetivity]
	colors=['red','green']
	explode=(0,0)
	plt.pie(sizes,explode=explode,labels=labels,colors=colors)
	plt.show()
	
	

