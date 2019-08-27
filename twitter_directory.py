try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter REST API
twitter = Twitter(auth=oauth)

import time
import os
import codecs

try: 
    os.makedirs('data/bot')
    os.makedirs('data/bot_retweets')
    os.makedirs('data/human')
    os.makedirs('data/human_retweets')
except OSError:
    if not os.path.isdir('data/bot'):
        raise
    if not os.path.isdir('data/human'):
    	raise

errors=0
users_remaining=800
file=open('varol-2017_updated.dat')
for line in file:
	if users_remaining==0:
		time.sleep(900)
		users_remaining=800
	user_id=line.split()[0]
	bot_or_not=line.split()[1]
	try:
		tweets=twitter.statuses.user_timeline(user_id=user_id, count=200, tweet_mode='extended')
		print 'success'
	except Exception as err:
		print err
		errors+=1
		print errors 
		continue

	if bot_or_not=='1':
		temp_file=codecs.open('data/bot/'+user_id,'w','utf-8')
		temp_file_1=codecs.open('data/bot_retweets/'+user_id,'w','utf-8')
		print 'bot'
	elif bot_or_not=='0':
		temp_file=codecs.open('data/human/'+user_id,'w','utf-8')
		temp_file_1=codecs.open('data/human_retweets/'+user_id,'w','utf-8')
		print 'human'
	
	i=0
	for tweet in tweets:
		try:#if it's a retweet, print retweeted text
			temp_file_1.write(tweets[i]['retweeted_status']['full_text'])
		except KeyError: #if it's not a retweet, print the text
           	#print json.dumps(tweets[j],indent=4)
			temp_file.write(tweets[i]['full_text'])
		except Exception as err:
			print err
		i+=1

	temp_file.close()
	temp_file_1.close()

	users_remaining-=1
print errors  #184 TIMELINES UNAVAILABLE
