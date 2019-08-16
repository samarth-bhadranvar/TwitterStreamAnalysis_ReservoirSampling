# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:52:34 2019

@author: SSB
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from operator import itemgetter
from collections import defaultdict
import random


class TwitterStreamListener(StreamListener):
    tweetSequence=0
    list_hashtags=[]
    dict_hashtagCount=defaultdict(lambda: 0)
    list_hashtagLength=[]
    dict_twitterLength=dict()
    dict_hashtagText=dict()
    
    def getDecisionToKeep(self, tweetProb):
        return random.random() < tweetProb
    
    def on_status(self,tweet):
        if self.tweetSequence < 100:
            
            self.list_hashtags=tweet.entities.get('hashtags')
            
            for hashtag in self.list_hashtags:
                if len(hashtag['text']) != 0:
                    self.dict_hashtagCount[hashtag['text']] += 1
            
            self.list_hashtagLength.append(len(tweet.text))
            
            self.dict_twitterLength[self.tweetSequence] = len(tweet.text)
            
            if len(self.list_hashtags) != 0:
                for hashtag in self.list_hashtags:
                    self.dict_hashtagText[self.tweetSequence] = hashtag['text']

            self.tweetSequence += 1
            
        else:
            
            self.tweetSequence += 1
            self.tweetProb = float(100.0/self.tweetSequence)

            self.decisionToInclude = self.getDecisionToKeep(self.tweetProb)

            if self.decisionToInclude:
                
                hashtagIndex = int(random.uniform(1, 100))
                
                
                if hashtagIndex in self.dict_hashtagText:
                    hashtagToDecrement = self.dict_hashtagText[hashtagIndex]
                    self.dict_hashtagCount[hashtagToDecrement] = self.dict_hashtagCount[hashtagToDecrement] - 1

                    self.dict_hashtagText[hashtagIndex] = None

                self.list_hashtags = tweet.entities.get('hashtags')

                for hashtag in self.list_hashtags:
                    if len(hashtag['text']) != 0:
                        self.dict_hashtagCount[hashtag['text']] += 1
                        self.dict_hashtagText[hashtagIndex] = hashtag['text']
                        
                if None in self.dict_hashtagCount:
                    del self.dict_hashtagCount[None]
                    
                hashTags_sorted = sorted(self.dict_hashtagCount.items(), key=itemgetter(0),reverse=False)
                hashTags_sorted = sorted(hashTags_sorted, key=itemgetter(1),reverse=True)
                
                print("\n")
                print("The number of tweets with tags from the beginning:" + str(self.tweetSequence))
                
                twitterflag_count = 1
                text = hashTags_sorted[0][1]
                for hashtag in hashTags_sorted: 
                    if hashtag[1] < text:
                        twitterflag_count +=1
                        text = hashtag[1]
                        if twitterflag_count < 4:
                            print(hashtag[0] + ":" + str(hashtag[1]))
                    elif hashtag[1] == text:
                        if twitterflag_count < 4:
                            print(hashtag[0] + ":" + str(hashtag[1]))
                            
        return True
            
    
    def on_error(self,errorCode):
        print(errorCode)
        if errorCode == 420:
            return False
    

twitter_apiKey="XXXXXXXXXXXXXXXXXXXXXXXXX"
twitter_apiSecretKey="XXXXXXXXXXXXXXXXXXXXXXXXX"

twitter_accessToken="XXXXXXXXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXX"
twiiter_accessTokenSecret="XXXXXXXXXXXXXXXXXXXXXXXXX"

oAuthHandler = OAuthHandler(twitter_apiKey,twitter_apiSecretKey)
oAuthHandler.set_access_token(twitter_accessToken,twiiter_accessTokenSecret)

streamListener= TwitterStreamListener()

twitterStream = Stream(auth=oAuthHandler,listener=streamListener)

twitterStream.filter(track=['WorldCup2019'],languages=['en'])