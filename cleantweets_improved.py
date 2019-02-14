import os
import re
import csv

dir = "/transient/viru/TopicAnalysisFiles/tweets_all_uncleaned/"
result_dir = "/transient/viru/TopicAnalysisFiles/tweets_all_cleaned/"
files = os.listdir(dir)

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

user_mentions = r'(?:@[\w_]+)'  # looking for user mentions in the tweet
# urls = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
urls = r"http\S+"
nums = r'(?:(?:\d+,?)+(?:\.?\d+)?)'
emails = r'(?:[\w_]+@[\w_]+)'


for file in files:
    if file != ".DS_Store":
        with open(dir+file, "r") as f, open(result_dir+file, "a") as f_o:
            for line in f:
                # b = TextBlob(line)
                # if b.detect_language() != 'es':

                # f = open(dir+file, "r")
                # Convert to list
                # data = [line for line in f.readlines()]

                # Remove Emails
                line = re.sub(emails, '', line)

                # Remove new line characters
                line = re.sub('\s+', ' ', line)

                # Remove urls
                line = re.sub(urls, "", line)

                # Remove distracting single quotes
                # data = [re.sub("\'", "", sent) for sent in data]

                # remove emoticons
                line = (emoji_pattern.sub(r'', line))

                # remove user mentions
                line = re.sub(user_mentions, "", line)

                # remove urls
                # data = [re.sub(r'http\S+', "", sent) for sent in data]

                # remove numbers
                line = re.sub(nums, "", line)

                # data = [' '.join(e for e in sent if e.isalnum()) for sent in data]

                line = re.sub('[^A-Za-z0-9]+', " ", line)

                # remove rt
                # data = [re.sub("^rt ", " ", sent) for sent in data]
                # data = [re.sub(" rt ", "", sent) for sent in data]

                # remove one character words
                line = ' '.join([w for w in line.split() if len(w) > 1])

                if line != "":
                    f_o.write(line + "\n")