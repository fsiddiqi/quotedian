#!/usr/bin/env python
#
#
import webapp2
import tweepy
import ConfigParser
from tweepy import *
from time import ctime, gmtime, mktime, strftime
import csv
import random

class BotHandler(webapp2.RequestHandler):
    def runBot(self):
        config = ConfigParser.RawConfigParser()
        config.read('settings.cfg')

        # http://dev.twitter.com/apps/myappid
        CONSUMER_KEY = config.get('Twitter', 'CONSUMER_KEY')
        CONSUMER_SECRET = config.get('Twitter', 'CONSUMER_SECRET')
        # http://dev.twitter.com/apps/myappid/my_token
        ACCESS_TOKEN_KEY = config.get('Twitter', 'ACCESS_TOKEN_KEY')
        ACCESS_TOKEN_SECRET = config.get('Twitter', 'ACCESS_TOKEN_SECRET')

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        # If the authentication was successful, you should
        # see the name of the account print out
        #Iam = api.me().name
        
        # Frequency calc
        freq = random.randint(1, 100)
        #freq = 3
        if freq <= 5:   
            # Tweet a random quote
            self.tweetQuote(api)
            # Follow back a follower
            ##self.followBackFollower(api)
        elif freq <= 20: 
            # Unfollow a non-follower
            self.dropNonFollower(api)
        elif freq <= 50: 
            # Add a random follower
            self.addNewFollower(api)
        else:           
            # RT 
            self.searchRT(api, config)
        self.response.write(freq)
        
        
    def tweet(self, api, theTweet):
        api.update_status(theTweet)
        
    def searchRT(self, api, config):
        searchTerms = config.get('Twitter', 'SEARCH_TERMS')
        termsList = searchTerms.split(",")
        term = random.choice(termsList)
        self.response.write(term)
        results = api.search(term, "en")
        resultsSorted = sorted(results, key=lambda tweet: tweet.retweet_count, reverse=True)
        if resultsSorted[0]:
            theTweet = resultsSorted[0].text
            #print(theTweet)
            self.response.write(theTweet)
            self.tweet(api, theTweet)
        
    def tweetQuote(self, api):
        # read csv
        with open('quotes.csv', 'rU') as f:
            reader = csv.reader(f)
            quotes = list(reader)
            randQuoteNum = random.randint(0, len(quotes))
            quote = quotes[randQuoteNum]
        
        # Format quote
        quoteText = quote[0]
        quoteAuthor = quote[1]
        # QuoteSource: Quote
        quoteSource = ", "+ quote[2] 
        quoteWho = quote[3] +": " if quote[3] else ""
        quoteHandle = quote[4]
        theTweet = "\""+ quoteWho + quoteText +"\""+ quoteSource
            
        # Tweet a quote
        if len(theTweet) < 140:
            self.tweet(api, theTweet)
        self.response.write(theTweet)

    def dropNonFollower(self, api):
        myID = api.me().id
        # Get followers
        followersList = api.followers_ids(myID)
        # Get friends
        friendsList = api.friends_ids(myID)
        # non-friend list
        nonFollowerList = list(set(friendsList) - set(followersList))
        if len(nonFollowerList) > 0:
            #self.response.write(nonFollowerList)
            # Get non-followers in descending order and pick the last one
            nonFollowerID = nonFollowerList[-1]
            #nonFollower = api.get_user(nonFollowerID)
            if nonFollowerID:
                nonFollower = api.destroy_friendship(nonFollowerID)
            self.response.write(nonFollower)

    def followBackFollower(self, api):
        myID = api.me().id
        # Get followers
        followersList = api.followers_ids(myID)
        # Get friends
        friendsList = api.friends_ids(myID)
        # non-friend list
        nonFollowingList = list(set(followersList) - set(friendsList))
        # Find non-follwers and pick a random one
        randNonFollowingID = random.choice(nonFollowingList)
        #randNonFollowingID = nonFollowingList[random.randint(0, len(nonFollowingList)-1)]
        #randNonFollowing = api.get_user(randNonFollowingID)
        if randNonFollowingID:
            randNonFollowing = api.create_friendship(randNonFollowingID)
        self.response.write(randNonFollowing)

    def addNewFollower(self, api):
        myID = api.me().id
        # Get followers
        followerList = api.followers_ids(myID)
        # Get a random follower
        randFollowerID = followerList[random.randint(0, len(followerList)-1)]
        # Get list of riends of the random follower
        friendList = api.friends_ids(randFollowerID)
        #newFollowerID = friendList[random.randint(0, len(friendList)-1)]
        newFollowerID = random.choice(friendList)
        #newFollower = api.get_user(newFollowerID)
        if newFollowerID:
            newFollower = api.create_friendship(newFollowerID)
        self.response.write(newFollower)
        
    
    def log(self, message):
        timestamp = strftime("%Y %b %d %H:%M:%S UTC: ", gmtime())
        print (timestamp + message + '\n')
    
    def get(self):
        try:
            self.runBot()
            print("Ran Bot")
        except TweepError as te:
            print te.message
        

app = webapp2.WSGIApplication([
    ('/bot', BotHandler)
], debug=False)
