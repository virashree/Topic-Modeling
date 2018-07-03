import nltk
import os
import csv

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
result_dir1 = "/transient/viru/TopicAnalysisFiles/K_grams/"
# result_dir2 = "/transient/viru/TopicAnalysisFiles/K-gram_files/"

# dir = "K_grams_files/"
# result_dir1 = "TfIdf/"
files = os.listdir(dir)

if not os.path.exists(result_dir1):
    os.makedirs(result_dir1)
#
# if not os.path.exists(result_dir2):
#     os.makedirs(result_dir2)

for file in files:
    filename = str(os.path.basename(file).split('.')[0])
    with open(dir+file, 'r') as f, open(result_dir1+filename+'.txt', 'w') as f_pos: #, \
        # open(result_dir2+filename+'.txt', 'w') as f_gram:
        # reader = csv.reader(x.replace('\0', '') for x in f)
        # next(reader)

        for tweet in f:

            #
            # emoticons_str2 = r"(?:[:=;][oO\-]*[D\)\]\(\]/\\OpP])"
            # html_tags = r'<[^>]+>'
            # user_mentions = r'(?:@[\w_]+)'
            # urls = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
            # nums = r'(?:(?:\d+,?)+(?:\.?\d+)?)'
            # emails = r'(?:[\w_]+@[\w_]+)'
            # hash_tags = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"
            #
            # regex_ascii = r'[^\x00-\x7F]+'
            #
            # tweet = html.unescape(row[5])
            # tweet = tweet.lower()
            # tweet = re.sub(hash_tags, "1hashtags", tweet)
            # tweet = re.sub(urls, "2url", tweet,
            #                re.VERBOSE | re.IGNORECASE)
            # tweet = re.sub(emails, "3email", tweet, re.VERBOSE | re.IGNORECASE)
            # tweet = re.sub(user_mentions, "4username", tweet, re.VERBOSE | re.IGNORECASE)
            # tweet = re.sub(emoticons_str2, "5emoticon", tweet, re.VERBOSE | re.IGNORECASE)
            # tweet = re.sub(html_tags, "6htmltag", tweet, re.VERBOSE | re.IGNORECASE)
            # tweet = re.sub(regex_ascii, "7ascii", tweet)
            #
            # # r = ""
            # # for t in tweet.split(' '):
            # #     x = re.sub(r"^[^a-zA-Z0-9 ]*|[^a-zA-Z0-9 ]*$", '', t)
            # #     r = r + " " + x
            #
            # tweet = re.sub('[^A-Za-z0-9]+', ' ', tweet)
            #
            # tweet = re.sub("^rt | rt ", "", tweet)

            tweet = nltk.word_tokenize(tweet)   # tokenizing the string
            tweet = nltk.pos_tag(tweet)     # pos tags

            # recognizing NOUN and ADJ sequences
            pattern = """
            chunk: {<N.*|JJ.*>+}
            """

            # pattern recognition
            # patterns = """
            # N-A-N-N: {<N.*> <JJ.*> <N.*> <N.*>}
            # N-N-A-N: {<N.*> <N.*> <JJ.*> <N.*>}
            # A-N-A-N: {<JJ.*> <N.*> <JJ.*> <N.*>}
            # ADJs-NOUN: {<JJ.*>{2,3} <N.*>}
            # ADJs-NOUNs: {<JJ.*>{2,2} <N.*>{2,2}}
            # ADJ-NOUNs: {<JJ.*> <N.*>{1,3}}
            # NOUN-ADJs-NOUN: {<N.*> <JJ.*>{1,2} <N.*>}
            # NOUNs: {<N.*>{1,4}}
            # """

            cp = nltk.RegexpParser(pattern)     # looking for the pattern
            tree = cp.parse(tweet)  # parsing the string for the pattern
            # print(tree)
            temp = []
            temp_pos = []
            for node in tree:
                if type(node) is nltk.tree.Tree:
                    if node.label():
                        # print(node)
                        
                        # leaves = [nltk.tuple2str(leave, sep='_') for leave in node.leaves()]
                        # # k_gram = " ".join([leave[0] for leave in node.leaves()])
                        # k_gram_pos = " ".join(leaves)   # attaching pos tags to the words
                        # temp_pos.append(k_gram_pos)
                        # # temp.append(k_gram)

                        leaves = node.leaves()
                        temp_pos.append(node.leaves())

            # f_pos.write(" ".join(temp_pos)+"\n")     /         # writing words with pos tags to a file

            # forming sub sequences/ K-grams
            k_grams = []
            for item in temp_pos:
                # words = phrase.split(' ')
                n = len(item)
                for i in range(n):
                    for j in range(i+1, n+1):
                        k_gram = item[i:j]
                        x = k_gram[-1][1]
                        if "JJ" not in x and len(k_gram) <= 4:
                            # removing K-grams ending with adj, and of length greater than 4
                            k_grams.append(item[i:j])

            for item in k_grams:
                z = ""
                for word in item:
                    y = word[0]
                    if z == "":
                        z = word[0]
                    else:
                        z = z + " " + word[0]
                f_pos.write(z)
                f_pos.write(",")
            f_pos.write("\n")

            # f_pos.writte(",".join(" ".join(word[0]) for item in k_grams for word in item))
            # joining K-grams with a white space and adding writing to the file

            # f_o.write(",".join(temp) + "\n")

            # tweet = [nltk.tuple2str(t, sep='_') for t in tweet]
            # tweet = " ".join(str(x) for x in tweet)
            #
            # writer.writerow([tweet])

