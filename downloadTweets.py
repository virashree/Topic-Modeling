
import csv
import pandas as pd
import json
from termcolor import colored
import tweepy
import sys

#
# CONSUMER_KEY = 'VScoLsA2Ip84Gg2GpR2Imf5Fy'
# CONSUMER_SECRET = '0KUiTPhNbgb6koaspDVOHlh2e955ZPqXVNhqrLN9wdWsL4cUV3'
# OAUTH_TOKEN = '1868826828-teIYVXW5m5uS4HBTDkE7vfqa87BqlKkmaeo0X4c'
# OAUTH_TOKEN_SECRET = '1pEZ3bSj4Tbg8Xag7kvOLrXjryijbT33kfZfNtu6Bq6do'
#
auth = tweepy.AppAuthHandler('VScoLsA2Ip84Gg2GpR2Imf5Fy', '0KUiTPhNbgb6koaspDVOHlh2e955ZPqXVNhqrLN9wdWsL4cUV3')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if not api:
    print("Can't Authenticate")
    sys.exit(-1)

df = pd.read_csv('Landslides_Worldwide_fr.csv')
# tweet_ids = df.tweet_id
df['Text'] = pd.Series("", index=df.index)


with open('Landslides_Worldwide_fr_tweets.json', 'w') as jsonFile, open('Landslides_Worldwide_fr_tweets.csv', 'w') as csvFile:
    w = csv.writer(csvFile)
    for index, row in df.iterrows():
        try:
            tweet = api.get_status(id=int(row['tweet_id'].strip('\'')))
            print(tweet._json)
            json.dump(tweet._json, jsonFile)
            jsonFile.write("\n")
            text = tweet.retweeted_status.text if hasattr(tweet, "retweeted_status") and tweet.retweeted_status else tweet.text
            row['Text'] = text
            w.writerow([tweet.id, text])
        except tweepy.TweepError as te:
            print(colored(te, 'green'))
            pass
        except Exception as e:
            print(colored(e, 'green'))
            pass

df.to_csv('Landslides_Worldwide_fr.csv')

#
# if __name__ == '__main__':
#     count = 0
#     with open("2013_pakistan_eq_tweets.json" ,'r') as f:
#         for line in f:
#             tweet = json.loads(line)
#             print(tweet['id'])
#             count = count + 1
#     print(count)
#







