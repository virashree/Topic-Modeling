import csv
import os
import time
import re
import html
import nltk

# dir = "/transient/viru/TopicAnalysisFiles/Tweets_byDate_byLanguage_english_filtered/"
# result_dir = "/transient/viru/TopicAnalysisFiles/TA_Collection/"
dir = "/transient/viru/harvey_twitter_dataset/Harvey_withoutDuplicates_english_merged.csv/"
result_dir = "/transient/viru/harvey_twitter_dataset/Harvey_withoutDuplicates_english_byDate/"

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

files = os.listdir(dir)

# distributing the tweets per unit
# for file in files:
#     filename = str(os.path.basename(file).split('.')[0])
file = "Harvey_withoutDuplicates_english_merged.csv"

with open(dir + file, 'r') as f:
    reader = csv.reader(x.replace('\0', '') for x in f)
    next(reader)
    for row in reader:
        created_at = time.strptime(row[1], '%a %b %d %H:%M:%S +0000 %Y')
        # hour = str(created_at.tm_hour)
        date = str(created_at.tm_mday)
        mon = str(created_at.tm_mon)
        year = str(created_at.tm_year)
        # dir_name = mon+"-"+date+"-"+year+"/"
        file_name = mon+"-"+date+"-"+year+".csv"
        with open(result_dir+file_name,'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)

# cleaning the tweets
#
# dirs = os.listdir(result_dir+"Tweets/")
# result_dir_1 = result_dir+"Tweet_text/"
#
# if not os.path.exists(result_dir_1):
#     os.makedirs(result_dir_1)
#
# for dir in dirs:
#     files = os.listdir(result_dir+"Tweets/"+dir)
#     for file in files:
#         tweet_ids = {}
#         filename = str(os.path.basename(file).split('.')[0])
#
#         if not os.path.exists(result_dir_1+dir):
#             os.makedirs(result_dir_1+dir)
#
#         with open(result_dir+"Tweets/"+dir + "/" + file, 'r') as f, open(result_dir_1+dir+"/"+filename+'_tweets.txt','w') as f_o:
#             reader = csv.reader(x.replace('\0', '') for x in f)
#             next(reader)
#             for row in reader:
#                 try:
#                     id = int(row[23]) if row[23] != ' ' or '' or None else int(row[4])
#
#                     if id not in tweet_ids:
#                         tweet_ids[id] = ''  # checking for the original tweet
#                         emoticons_str2 = r"(?:[:=;][oO\-]*[D\)\]\(\]/\\OpP])"  # looking for emoticon in the tweet
#                         html_tags = r'<[^>]+>'  # looking for html tag
#                         user_mentions = r'(?:@[\w_]+)'  # looking for user mentions in the tweet
#                         urls = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
#                         # looking for urls
#
#                         # nums = r'(?:(?:\d+,?)+(?:\.?\d+)?)'
#
#                         emails = r'(?:[\w_]+@[\w_]+)'  # looking for emails
#                         hash_tags = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"  # looing for hashtags
#
#                         regex_ascii = r'[^\x00-\x7F]+'  # looking for non ascii characters
#
#                         tweet = html.unescape(row[5])  # converting to unicode characters
#                         tweet = tweet.lower()  # converting to lower case
#                         tweet = re.sub(hash_tags, "1hashtags", tweet)  # replacing hashtags
#                         tweet = re.sub(urls, "2url", tweet,
#                                        re.VERBOSE | re.IGNORECASE)  # replacing urls
#                         tweet = re.sub(emails, "3email", tweet, re.VERBOSE | re.IGNORECASE)  # replacing email
#                         tweet = re.sub(user_mentions, "4username", tweet,
#                                        re.VERBOSE | re.IGNORECASE)  # replacing usename
#                         tweet = re.sub(emoticons_str2, "5emoticon", tweet, re.VERBOSE | re.IGNORECASE)
#                         # replacing emoticons
#                         tweet = re.sub(html_tags, "6htmltag", tweet, re.VERBOSE | re.IGNORECASE)  # replacing html tag
#                         tweet = re.sub(regex_ascii, "7ascii", tweet)  # replcing non ascii characters
#
#                         # r = ""
#                         # for t in tweet.split(' '):
#                         #     x = re.sub(r"^[^a-zA-Z0-9 ]*|[^a-zA-Z0-9 ]*$", '', t)
#                         #     r = r + " " + x
#
#                         tweet = re.sub('[^A-Za-z0-9]+', ' ', tweet)
#                         # getting rid of special characters keeping only alpha numeric characters
#
#                         tweet = re.sub("^rt | rt ", "", tweet)  # getting rid of "rt" as in retweet
#                         tweet = re.sub(" [A-Za-z]{1} |^[A-Za-z]{1} | [A-Za-z]{1}$", "", tweet)
#                         # removing one character words from tweet
#
#                         # tweet = nltk.word_tokenize(tweet)
#                         # tweet = nltk.pos_tag(tweet)
#                         #
#                         # tweet = [nltk.tuple2str(t, sep='_') for t in tweet]
#                         # tweet = " ".join(str(x) for x in tweet)
#
#                         f_o.write(tweet + "\n")
#                 except Exception as e:
#                     print(row, row[4], row[23])
#                     print(e)
#
# # k-grams
#
# dirs = os.listdir(result_dir_1)
# result_dir_2 = result_dir+"K-grams/"
# if not os.path.exists(result_dir_2):
#     os.makedirs(result_dir_2)
#
# for dir in dirs:
#     files = os.listdir(result_dir_1 + dir)
#     for file in files:
#         filename = str((os.path.basename(file).split('.')[0])).split('_tweets')[0]
#
#         if not os.path.exists(result_dir_2 + dir):
#             os.makedirs(result_dir_2 + dir)
#
#         with open(result_dir_1 + dir + "/" + file, 'r') as f, open(result_dir_2 + dir + "/" + filename+'_K-grmas.txt', 'w') as f_pos:  # , \
#             for tweet in f:
#                 tweet = nltk.word_tokenize(tweet)  # tokenizing the string
#                 tweet = nltk.pos_tag(tweet)  # pos tags
#
#                 # recognizing NOUN and ADJ sequences
#                 pattern = """
#                 chunk: {<N.*|JJ.*>+}
#                 """
#
#                 cp = nltk.RegexpParser(pattern)  # looking for the pattern
#                 tree = cp.parse(tweet)  # parsing the string for the pattern
#                 # print(tree)
#                 temp = []
#                 temp_pos = []
#                 for node in tree:
#                     if type(node) is nltk.tree.Tree:
#                         if node.label():
#
#                             leaves = node.leaves()
#                             temp_pos.append(node.leaves())
#
#                 k_grams = []
#                 for item in temp_pos:
#                     # words = phrase.split(' ')
#                     n = len(item)
#                     for i in range(n):
#                         for j in range(i + 1, n + 1):
#                             k_gram = item[i:j]
#                             x = k_gram[-1][1]
#                             if "JJ" not in x and len(k_gram) <= 4:
#                                 # removing K-grams ending with adj, and of length greater than 4
#                                 k_grams.append(item[i:j])
#
#                 for item in k_grams:
#                     z = ""
#                     for word in item:
#                         y = word[0]
#                         if z == "":
#                             z = word[0]
#                         else:
#                             z = z + " " + word[0]
#                     f_pos.write(z)
#                     f_pos.write(",")
#                 f_pos.write("\n")
#
#
#


