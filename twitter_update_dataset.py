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
from twitter_limit_check import *

deleted_users=0 #count of how many users have been deleted
users_remaining=800 #used to not exceed twitter API limit
file=open('varol-2017.dat')
new_file=open('varol-2017_updated.dat','w')
for line in file:
	if users_remaining==0:
		time.sleep(900) #wait for limit to reset
		users_remaining=800 #reset count
	user_id=line.split()[0]
	bot_or_not=line.split()[1]
	try: #try to add user to new file
		#tweets=twitter.statuses.user_timeline(user_id=user_id, count=1)
		#print user_id, tweets[0]['user']['name']
		user=twitter.users.show(user_id=user_id)
		print user_id, user['screen_name']
		new_file.write(user_id+"\t"+bot_or_not+"\n")
	except Exception as err: #if user doesn't exist, print error
		print "User with ID " + user_id + " not found."
		print err
		deleted_users+=1 #increment deleted user count
		print deleted_users #196 DELETED/SUSPENDED ACCOUNTS
	users_remaining-=1
print deleted_users  
