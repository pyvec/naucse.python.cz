#!/usr/bin/env python

# Tested in Python 3

# Sebastian Raschka, 2014
# An interactive command line app for
# downloading your personal twitter timeline.
#
# For help, execute
# ./twitter_timeline.py --help

import twitter
from datetime import datetime
import time
import re
import sys
import pandas as pd
import pyprind as pp
import oauth_info as auth # our local file with the OAuth infos

class TimelineMiner(object):
    def __init__(self, access_token, access_secret, consumer_key, consumer_secret, user_name):
        self.access_token = access_token
        self.access_secret = access_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.user_name = user_name
        self.auth = None
        self.df = pd.DataFrame(columns=['timestamp', 'tweet'], dtype='str')


    def authenticate(self):
        self.auth = twitter.Twitter(auth=twitter.OAuth(self.access_token, 
                    self.access_secret, self.consumer_key, 
                    self.consumer_secret))
        return bool(isinstance(self.auth, twitter.api.Twitter))
        

    def get_timeline(self, max=0, keywords=[]):
        if keywords:
            self.df['keywords'] = ''
        tweet_ids = [self.auth.statuses.user_timeline(
                user_id=self.user_name, count=1
                )[0]['id']] # the ID of my last tweet
        last_count = 200
        counter = 0
        while last_count == 200:
            timeline = self.auth.statuses.user_timeline(user_id=self.user_name, count=200, max_id=tweet_ids[-1])
            for tweet in range(len(timeline)):
        
                text = timeline[tweet]['text'].replace('"', '\'')
                tweet_id = int(timeline[tweet]['id'])
                date = self.__get_date(timeline, tweet)
                
                if keywords:
                    for k in keywords:
                        if self.__check_keyword(text,k):
                            self.df.loc[counter,'tweet'] = text
                            self.df.loc[counter,'timestamp'] = date
                            try:
                                self.df.loc[counter,'keywords'].append(k)
                            except AttributeError:
                                self.df.loc[counter,'keywords'] = [k]
                    try:
                        self.df.loc[counter,'keywords'] = ';'.join(self.df.loc[counter,'keywords'])
                    except KeyError:
                        pass
                        
                    
                else:
                    self.df.loc[counter,'tweet'] = text
                    self.df.loc[counter,'timestamp'] = date
                              
                counter += 1
                if max and counter >= max:
                    break
                
                sys.stdout.flush()   
                sys.stdout.write('\rTweets downloaded: %s' %counter)   
                    
            if max and counter >= max:
                break
            last_count = len(timeline)
            tweet_ids.append(timeline[-1]['id'])
            time.sleep(1)
        print()
        
    def make_csv(self, path):
        self.df.to_csv(path, encoding='utf8')

    def __get_date(self, timeline, tweet):
        timest = datetime.strptime(timeline[tweet]['created_at'],
                                      "%a %b %d %H:%M:%S +0000 %Y")
        date = timest.strftime("%Y-%d-%m %H:%M:%S")
        return date
    
    def __check_keyword(self, s, key):
        return bool(re.search(key, s, re.IGNORECASE))
        
    
if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(
            description='A command line tool to download your personal twitter timeline.',
            formatter_class=argparse.RawTextHelpFormatter,
    epilog='\nExample:\n'\
                './twitter_timeline.py -o my_timeline.csv -k Python,Github')

    parser.add_argument('-o', '--out', help='Filename for creating the output CSV file.')
    parser.add_argument('-m', '--max', help='Maximum number (integer) of timeline tweets query (searches all by default)')
    parser.add_argument('-k', '--keywords', help='A comma separated list of keywords for filtering (optional).')
    parser.add_argument('-v', '--version', action='version', version='v. 1.0.1')
    
    args = parser.parse_args()
    
    if not args.out:
        print('Please provide a filename for creating the output CSV file.')
        quit()
    
    tm = TimelineMiner(auth.ACCESS_TOKEN, 
                       auth.ACCESS_TOKEN_SECRET,  
                       auth.CONSUMER_KEY, 
                       auth.CONSUMER_SECRET,
                       auth.USER_NAME)
                       
    if not args.max:
        max_t = 0
    else:
        max_t = int(args.max)
    if args.keywords:
        keywords = args.keywords.split(',')
    else:
        keywords = args.keywords
        
    print('Authentification successful: %s' %tm.authenticate())
    tm.get_timeline(max=max_t, keywords=keywords)
    tm.make_csv(args.out)
    
