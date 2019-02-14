import re
import csv
import os
import html

# NN	noun, singular 'desk'
# NNS	noun plural	'desks'
# NNP	proper noun, singular	'Harrison'
# NNPS	proper noun, plural	'Americans'
# JJ	adjective	'big'
# JJR	adjective, comparative	'bigger'
# JJS	adjective, superlative	'biggest'


# K-grams
# one-gram
# noun
# bi-grams
# noun noun , adjective noun
# tri-grams
# noun noun noun , adjective noun noun, noun adjective noun, adjective adjective noun
# quad-grams
# noun noun noun noun, adjective noun noun noun, noun adjective noun noun, noun noun adjective noun
# adjective adjective noun noun, adjective noun adjective noun, noun adjective adjective noun,
# adjective adjective adjective noun

dir = "/transient/viru/TopicAnalysisFiles/Tweets/"
result_dir = "/transient/viru/TopicAnalysisFiles/Tweets_cleaned/"
files = os.listdir(dir)

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

for file in files:
    if file != ".DS_Store":
        # filename = str(os.path.basename(file).split('.')[0])
        with open(dir + file, 'r') as f, open(result_dir+file, 'w') as f_o:
            # reader = csv.reader(x.replace('\0', '') for x in f)
            # next(reader)
            for row in f:
                if row.strip() != "":
                    try:
                        emoticons_str2 = r"(?:[:=;][oO\-]*[D\)\]\(\]/\\OpP])" # looking for emoticon in the tweet
                        html_tags = r'<[^>]+>'  # looking for html tag
                        user_mentions = r'(?:@[\w_]+)'  # looking for user mentions in the tweet
                        urls = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
                        # looking for urls
                        nums = r'(?:(?:\d+,?)+(?:\.?\d+)?)'
                        emails = r'(?:[\w_]+@[\w_]+)'   # looking for emails
                        # hash_tags = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"    # looking for hashtags
                        # regex_ascii = r'[^\x00-\x7F]+'  # looking for non ascii characters

                        # tweet = html.unescape(row)   # converting to unicode characters
                        tweet = row.lower()   # converting to lower case
                        # tweet = re.sub(hash_tags,"1hashtag", tweet) # replacing hashtags
                        tweet = re.sub(nums,"1number",tweet)
                        tweet = re.sub(urls, "2url", tweet,
                                       re.VERBOSE | re.IGNORECASE)  # replacing urls
                        tweet = re.sub(emails, "3email", tweet, re.VERBOSE | re.IGNORECASE)
                        # replacing email
                        tweet = re.sub(user_mentions, "4username", tweet, re.VERBOSE | re.IGNORECASE)
                        # replacing username
                        tweet = re.sub(emoticons_str2, "5emoticon", tweet, re.VERBOSE | re.IGNORECASE)
                        # replacing emoticons
                        tweet = re.sub(html_tags, "6htmltag", tweet, re.VERBOSE | re.IGNORECASE)    # replacing html tag
                        # tweet = re.sub(regex_ascii, "7ascii", tweet)    # replacing non ascii characters

                        # r = ""
                        # for t in tweet.split(' '):
                        #     x = re.sub(r"^[^a-zA-Z0-9 ]*|[^a-zA-Z0-9 ]*$", '', t)
                        #     r = r + " " + x

                        tweet = re.sub('[^A-Za-z0-9]+', ' ', tweet)
                        # getting rid of special characters keeping only alpha numeric characters

                        tweet = re.sub("^rt ", "", tweet)  # getting rid of "rt" as in retweet
                        tweet = re.sub(" rt ", " ", tweet)
                        tweet = ' '.join([w for w in tweet.split() if len(w) > 1])
                        # tweet = re.sub(" [A-Za-z]{1} |^[A-Za-z]{1} | [A-Za-z]{1}$", " ", tweet)
                        # removing one character words from tweet

                        # tweet = nltk.word_tokenize(tweet)
                        # tweet = nltk.pos_tag(tweet)
                        #
                        # tweet = [nltk.tuple2str(t, sep='_') for t in tweet]
                        # tweet = " ".join(str(x) for x in tweet)

                        f_o.write(tweet.strip()+"\n")
                    except Exception as e:
                        print(row)
                        print(e)


