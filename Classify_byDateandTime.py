import csv
import time
import os
import re
result_dir = "/transient/viru/TopicAnalysisFiles/_All_Text_Tweets_by_time/"

dir = "/transient/viru/TopicAnalysisFiles/All_Tweets_Indexfiles/"


# this part is for data cleaning , if tweets are already clean comment it out 

#################################################################################
user_mentions = r'(?:@[\w_]+)'  # looking for user mentions in the tweet
# urls = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
urls = r"http\S+"
nums = r'(?:(?:\d+,?)+(?:\.?\d+)?)'
emails = r'(?:[\w_]+@[\w_]+)'
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


def clean_tweet(tweet):
    # Remove Emails
    tweet = re.sub(emails, '', tweet)

    # Remove new line characters
    tweet = re.sub('\s+', ' ', tweet)

    # Remove urls
    tweet = re.sub(urls, "", tweet)

    # remove emoticons
    tweet = (emoji_pattern.sub(r'', tweet))

    # remove user mentions
    tweet = re.sub(user_mentions, "", tweet)

    # remove numbers
    tweet = re.sub(nums, "", tweet)

    # data = [' '.join(e for e in sent if e.isalnum()) for sent in data]

    tweet = re.sub('[^A-Za-z0-9]+', " ", tweet)

    # remove one character words
    tweet = ' '.join([w for w in tweet.split() if len(w) > 1])
    return tweet

#################################################################################


if not os.path.exists(result_dir):
    os.makedirs(result_dir)

files = os.listdir(dir)

# classifying by date and time 
for file in files:
    with open(dir+file, 'r') as f:
        print(file)
        reader = csv.reader(x.replace('\0', '') for x in f)
        # next(reader)
        for row in reader:
            try:
                created_at = time.strptime(row[1], '%a %b %d %H:%M:%S +0000 %Y')
                hour = str(created_at.tm_hour)
                date = str(created_at.tm_mday)
                mon = str(created_at.tm_mon)
                year = str(created_at.tm_year)
                dir_name = mon+"-"+date+"-"+year+"/"
                file_name = year+"-"+mon+"-"+date+"-"+hour+".txt"
                # if not os.path.exists(result_dir+dir_name):
                #     os.makedirs(result_dir+dir_name)
                with open(result_dir+file_name, 'a') as f:
                    # writer = csv.writer(f)
                    # writer.writerow(row)
                    if row[21] == 'en':
                        f.write(clean_tweet(row[4]) + "\n")
            except:
                print(row)
                break


