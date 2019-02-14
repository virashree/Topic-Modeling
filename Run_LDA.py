import gensim
from gensim.models import CoherenceModel
from gensim.test.utils import datapath
import csv
import pprint
import numpy as np
import logging
logging.basicConfig(filename='gensim.log',
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    level=logging.INFO)
import sys

# corpus_filepath = 'Tweet_cleaned/disasterTweets.mm'
# dictionary_path = '/Users/vira/Downloads/disasterTweets.dict'
# corpus = gensim.corpora.MmCorpus(corpus_filepath)
# print(corpus[:1])
# id2word = gensim.corpora.Dictionary.load(dictionary_path)
# vocab = id2word.token2id
# print(vocab)
# with open('dict.csv', 'w') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in vocab.items():
#        writer.writerow([key, value])

# give the name of the result directory where you want to save LDA model and other files 
result_dir = ""

# loading streming corpus created by build_corpus.py and TweetCorpus_byTweets.py
corpus = gensim.corpora.MmCorpus('Result/disasterTweets.mm')
# loading is2word dictionary 
id2word = gensim.corpora.Dictionary.load('Result/disasterTweets.dict')
# id2word.filter_tokens(bad_ids=[id2word.token2id['eofeofeof']])

# making sure eofeofeof is not in the vocabulary 
print('eofeofeof' in id2word.token2id)

# vocab = id2word.token2id
# data_lemmatized = list(id2word.token2id.keys())

# loading the documents for coherence measure c_v, these are documents (i.e. tweets) fed to LDA model 
texts = [line.split() for line in open("Tweet_cleaned/8-18-2017.txt").read().splitlines() if line != "eofeofeof"]

# give appropriate parameters to LDA model 
# another LDA is gensim.models.ldamodel.LdaModel: https://radimrehurek.com/gensim/models/ldamodel.html
lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=id2word,
                                       chunksize=100000,
                                       num_topics=80)


# printing the topics 
pprint.pprint(lda_model.print_topics())
try:
    # saving the topic to view later 
    pp = pprint.PrettyPrinter(stream=open("topics.txt", "w"))
    pp.pprint(lda_model.print_topics())
except:
    pass

# do not need this if streaming corpus is already saved 
# with open(result_dir+'corpus.txt', 'w') as f:
#     for item in corpus:
#         f.write("%s\n" % item)

# sabving LDA model for later use 
model_file = datapath(result_dir+"lda_model")
print(model_file)
lda_model.save(model_file)

# computing perplexity 
perplexity = lda_model.log_perplexity(corpus)
print('\nPerplexity: ', perplexity)

# Computing Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, dictionary=id2word, corpus=corpus, texts=texts, coherence='c_v')
coherence_model_lda_1 = CoherenceModel(model=lda_model, dictionary=id2word, corpus=corpus,coherence='u_mass')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)
coherence_lda_1 = coherence_model_lda_1.get_coherence()
print('\nCoherence Score: ', coherence_lda_1)

# writing down the score for later use 
with open("/home/ec2-user/Data/Result/Corpus/DateCorpus/9-10-2017/lda_scores.csv", 'a') as f:
    writer = csv.writer(f)
    writer.writerow([perplexity, coherence_lda_1, coherence_lda, lda_model.print_topics()])
