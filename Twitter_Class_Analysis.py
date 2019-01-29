# coding: utf-8

import tweepy
import json
import os
from datetime import datetime
import pandas as pd

class Twitter_Analysis:
    
    __consumer_key = 'PSXYFbBa8Pd8jVk6NIt1R3wlN'
    __token = '1PpSRhZHtQpq5QVjVH2CNkwA4Nr7nmspDMlbbv9iiBzXu6Jn7X'
    __api = None

    def __init__(self, dico_file, maxTweets, filename, company_name, companies_CSV_file):
        self.dico_file = self.open_dico(dico_file)
        self.max_tweets = maxTweets
        self.tweetsPerQry = 100 # Can't change that
        self.fName = filename
        self.companies_list = self.open_csv_companies(companies_CSV_file)
        self.company_name = company_name
        self.__class__.__api = self.__class__.authentificator()
        
        # This is what we're searching for :
        self.searchQuery = " OR ".join(['\"' + item + '\"' for item in self.dico_file["eco_responsable"]])
        self.searchQuery += " -filter:retweets AND -filter:replies"
        """
        if companies_CSV_file is not None:
            self.searchQuery += " AND " + " OR ".join([repr(item) for item in self.companies_list])
        """
    
    
    
    @staticmethod
    def open_dico(dico_file):
        with open(dico_file) as dico:
            return(eval(dico.read()))

    @staticmethod
    def open_csv_companies(companies_CSV_file):
        if companies_CSV_file is not None:
        	df = pd.read_csv(companies_CSV_file, encoding='utf-8', delimiter=';')
        	companies_list = df["companies"].tolist()
        	return(companies_list)
        else:
            return([])
    
    @classmethod   
    def authentificator(cls):
        try:
            auth = tweepy.AppAuthHandler(cls.__consumer_key, cls.__token)
            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            print("Authentification success !")
            return api
            #cls.__api  = api
            #return("sucess")
            
        except:
            print("Impossible to Authentifiate !")
            #return("fail")
            raise


    def search(self):
        if len(self.companies_list)>0:
            for companie in self.companies_list:
                print('\n'+repr(companie)+'\n')
                parameter = " AND " + repr(companie)
                self.twitter_retrieval(addParam=parameter)
        elif len(str(company_name))>0:
            parameter = " AND " + repr(self.company_name)
            self.twitter_retrieval(addParam=parameter)
        else:
            self.twitter_retrieval()
    
    def twitter_retrieval(self, max_id=-1, sinceId=None, addParam=None):
        # default to no upper limit, start from the most recent tweet matching the search query.
        tweetCount = 0
        ##print(max_id)
        ##if (not sinceId): print(2)
        
        print("Downloading max {0} tweets".format(self.max_tweets))
        
        with open(str(self.fName + '.json'), 'a',encoding='utf-8') as f:
            while tweetCount < self.max_tweets:
                try:
                    if (max_id <= 0):
                        if (not sinceId):
                            new_tweets = self.__class__.__api.search(q=self.searchQuery+addParam, count=self.tweetsPerQry)
                        else:
                            new_tweets = self.__class__.__api.search(q=self.searchQuery+addParam, count=self.tweetsPerQry,
                                                    since_id=sinceId)
                    else:
                        if (not sinceId):
                            new_tweets = self.__class__.__api.search(q=self.searchQuery+addParam, count=self.tweetsPerQry,
                                                    max_id=str(max_id - 1))
                        else:
                            new_tweets = self.__class__.__api.search(q=self.searchQuery+addParam, count=self.tweetsPerQry,
                                                    max_id=str(max_id - 1),
                                                    since_id=sinceId)
                    if not new_tweets:
                        print("No more tweets found")
                        break
                    
                    for tweet in new_tweets:
                        f.write(str({k:str(tweet._json.get(k, None)) for k in ('id_str', 'created_at', 'text', 'retweeted', 'user',
                                                                               'entities', 'lang', 'retweet_count', 'geo')})+"\n")
                    tweetCount += len(new_tweets)
                    print("Downloaded {0} tweets".format(tweetCount))
                    max_id = new_tweets[-1].id
                
                except tweepy.TweepError as e:
                    # Just exit if any error
                    print("some error : " + str(e))
                    break
        print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, self.fName+'.json'))

    
    def tweets_to_dataframe(self):
        ##### tweet retrieval ######
        lines = [line.rstrip('\n') for line in open(self.fName+'.json', 'r', encoding='utf-8')]
        new = [json.loads(json.dumps(eval(item))) for item in lines]
        df=pd.DataFrame(new)
        df.shape
        #final = [datetime.strptime(re.sub(r" \+[0-9]+", "", x), "%a %b %d %H:%M:%S %Y").date() for x in df.created_at.astype(str)]
        df.created_at = [datetime.strptime(x, "%a %b %d %H:%M:%S %z %Y") for x in df.created_at.astype(str)]
        df.retweeted = df.retweeted.astype(bool)
        df.id_str = df.id_str.astype(str)
        
        df['day'] = [x.day for x in df.created_at]
        df['month'] = [x.month for x in df.created_at]
        df['year'] = [x.year for x in df.created_at]
        
        #info from the tweet itself
        df['hashtags'] = list(map(lambda z: 
            [x.get('text') for x in eval(json.loads(json.dumps(z)))['hashtags']], df.entities))
        """df['hastags_occurencies'] = list(map(lambda z: 
            [len(x.get('indices')) for x in eval(json.loads(json.dumps(z)))['hashtags']], df.entities))"""
        df['user_mentions'] = list(map(lambda z: 
            [x.get('screen_name') for x in eval(json.loads(json.dumps(z)))['user_mentions']], df.entities))
            
        #info from the user who posts the tweet
        df['user_name'] = list(map(lambda z: eval(json.loads(json.dumps(z)))['name'], df.user))
        #df.where(df.user_name!=df.user_name2)
        df['user_location'] = list(map(lambda z: eval(json.loads(json.dumps(z)))['location'], df.user))
        df['user_followers_count'] = list(map(lambda z: eval(json.loads(json.dumps(z)))['followers_count'], df.user))
        df['user_friends_count'] = list(map(lambda z: eval(json.loads(json.dumps(z)))['friends_count'], df.user))
        
        df['tweet_coordinates'] = list(map(lambda z: tuple(eval(json.loads(json.dumps(z)))['coordinates']) if z != 'None' else 'None', df.geo))
        
        df['valeur_dico']  = list(map(lambda z: [x for x in ' '.join(self.dico_file['eco_responsable']).split(' ') if x.lower() in str(z)], df.text.str.lower()))
        
        del(df['entities'])
        del(df['created_at'])
        del(df['user'])
        del(df['geo'])

        df.to_csv(self.fName+'.csv', encoding='utf-8', index=False, sep=';')
        print('Go Look at your dataframe now :-) ')
        
    def strengthen_dico(self):
        #my_set = set()
        b={}
        liste_hashtags=[]
        tweetCount=0
        while tweetCount < self.max_tweets:
            new_tweets = self.__class__.__api.search(q=self.searchQuery, count=self.tweetsPerQry, lang='fr')
            for tweet in new_tweets:
                a = tweet._json.get('entities', None).get('hashtags', None)
                if len(a)>0:
                    text_each_hashtag_in_tweet = [i.get('text', None).lower() for i in a]
                    liste_hashtags.extend(text_each_hashtag_in_tweet)
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            
        for word in liste_hashtags:
            b[word] = b.get(word, 0) + 1
        sorted_dico = sorted(b.items(), key=lambda d: d[1], reverse=True)
        return(sorted_dico)

"""
analysis = Twitter_Analysis(dico_file='dico_file.txt',filename='tweets44',maxTweets=10000)
analysis.fName
dico_strengthen2 = analysis.strengthen_dico()
analysis.twitter_retrieval()
analysis.tweets_to_dataframe()
"""
