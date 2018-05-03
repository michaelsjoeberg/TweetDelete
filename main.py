#!/usr/bin/env python
 
import tweepy
from datetime import datetime, timedelta

TEST_MODE = False
DELETE_TWEETS = True
DELETE_LIKES = True
DAYS_TO_KEEP = 30

TWEETS_TO_SAVE = [
    930128769112780800,             # tweet id
]
LIKES_TO_SAVE = [
    930128769112780800,             # tweet id
]

CONSUMER_KEY = 'CONSUMER_KEY_HERE'
CONSUMER_SECRET = 'CONSUMER_SECRET_HERE'
ACCESS_TOKEN = 'ACCESS_TOKEN_HERE'
ACCESS_SECRET = 'ACCESS_SECRET_HERE'

# authenticate
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# set cutoff date using UTC to match twitter
cutoff_date = datetime.utcnow() - timedelta(days=DAYS_TO_KEEP)

# delete old tweets
if DELETE_TWEETS:

    # get all timeline tweets
    print "Retrieving timeline tweets..."
    timeline = tweepy.Cursor(api.user_timeline).items()
    
    deleted_count = 0
    ignored_count = 0
 
    for tweet in timeline:
        # delete tweet if not in saved list and older than cutoff
        if tweet.id not in TWEETS_TO_SAVE and tweet.created_at < cutoff_date:
            if not TEST_MODE:
                print ("Deleting %d: [%s] %s" % (tweet.id, tweet.created_at, tweet.text))
                api.destroy_status(tweet.id)
             
            deleted_count += 1

        else:
            ignored_count += 1
 
    print "Deleted %d tweets and ignored %d." % (deleted_count, ignored_count)

# unliking old likes
if DELETE_LIKES:

    # get all likes
    print "Retrieving liked tweets..."
    favorites = tweepy.Cursor(api.favorites).items()

    unliked_count = 0
    ignored_count = 0
 
    for tweet in favorites:
        # where tweets are not in save list and older than cutoff date
        if tweet.id not in LIKES_TO_SAVE and tweet.created_at < cutoff_date:
            if not TEST_MODE:
                print ("Unliking %d: [%s] %s" % (tweet.id, tweet.created_at, tweet.text))
                api.destroy_favorite(tweet.id)
             
            unliked_count += 1

        else:
            ignored_count += 1
 
    print "Unliked %d tweets and ignored %d." % (unliked_count, ignored_count)

print ("Done.")
