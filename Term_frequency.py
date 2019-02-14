from collections import defaultdict
import gensim
import numpy as np

import json


dir = ""
result_dir = ""
filename = ""


def sent_to_words(sentences):
    for sentence in sentences:
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


freq = defaultdict(int)
data = np.genfromtxt(dir + filename+".txt", dtype=str, delimiter='\n')

tweets = np.array(list(sent_to_words(data)))

for tweet in tweets:
    for token in tweet:
        freq[token] += 1

# writing
json.dump(freq, open(result_dir+filename+".csv", 'w'))


