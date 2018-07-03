import pymongo
from pymongo import MongoClient
import csv
import os
import json
import pandas as pd

# db = client.tweets

# csvfile = open('9-28-2017_english_filtered.csv', 'r')
# reader = csv.DictReader( csvfile )
# mongo_client = MongoClient('localhost', 27017)
# db = mongo_client.tweets
# collection = db.collection

# db.segment.drop()
#
header = ["source_file", "created_at", "retweeted_status_created_at", "tweet_id", "tweet_text", "user_id", "user_name", "user_screen_name", "user_location",
         "user_time_zone", "user_lang", "coordinates", "place_bounding_box", "place_country_code", "place_country", "place_full_name",
         "place_name", "hashtags", "media_url_https", "extended_url_type", "type", "lang", "retweeted_status_tweet_id",
         "retweeted_status_user_screen_name", "tweet_link"]

header_1 = ["source_file", "created_at", "retweeted_status_created_at", "tweet_id", "tweet_text", "user_id", "user_name", "user_screen_name", "user_location",
         "user_time_zone", "user_lang", "coordinates", "place_bounding_box", "place_country_code", "place_country", "place_full_name",
         "place_name", "hashtags", "media_url_https", "extended_url_type", "type", "lang", "retweeted_status_tweet_id",
         "retweeted_status_user_screen_name", "tweet_link"]
dir_path = ""
# files = os.listdir('')


def import_content():

    client = MongoClient('127.0.0.1', 27017, connect=False )

    db = client['topicAnalysis']
    coll = db['original_tweets']
    # coll.remove()

    with open('/transient/viru/ClassificationFiles/DisasterFiles_Classified_filtered/Harvey_filtered.csv', 'r') as f:
        open('/transient/viru/harvey_twitter_dataset/Hurricane_Harvey_all_original_tweets.csv', 'a') as f_out:
        # reader = csv.DictReader((x.replace('\0', '') for x in f), fieldnames=header)
        reader = csv.DictReader(f)
        writer = csv.DictWriter(f_out, fieldnames=header, extrasaction='ignore')
        writer.writeheader()
        next(reader)
        try:
            for row in reader:
                    # payload = json.dumps(row)
                    # payload = json.loads(row.to_json(orient='records'))

            # data = pd.read_csv('9-28-2017_english_filtered.csv')
            # payload = json.loads(data.to_json(orient='records'))
            #         coll.remove()
                    try:
                        # coll.create_index("tweet_id", name='index', background=True, unique=True)
                        coll.insert(row)
                        # writer.writerow(row)
                    except pymongo.errors.DuplicateKeyError:
                        continue
                    except Exception as ex:
                        print(ex)
                        print(row)
        except Exception as e:
            print(e)

    return coll.count()


if __name__ == '__main__':
    # filepath = '9-28-2017_english_filtered.csv'
    print(import_content())


    # remove duplicates from the new files
    # add tweets to topic analysis files taking care of the same tweets
    # 7041866
