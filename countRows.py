import json
import csv
import os
cnt = 0
id = []

# dir = "transient/viru/Tweets_byDate_byLanguage/"
# files = os.listdir(dir)

# for file in files:
with open('/transient/viru/TopicAnalysisFiles/Tweets_byDate_byLanguage_english_filtered/8-26-2017_english_filtered_merged.csv','r') as tweet_csv:
    reader = csv.reader(x.replace('\0', '') for x in tweet_csv)
    row_count = sum(1 for row in reader)
    print(row_count)

# with open('../RawData/stream__Harvey.json', 'r') as tweets_file:
#     for line in tweets_file:
#         try:
#             tweet = json.loads(line)
#             id.append(tweet['id'])
#         except:
#             print(line)
#     print(len(id))


