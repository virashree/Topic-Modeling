import sys
import os
import csv
# import re
import numpy as np
# import pandas as pd
from pprint import pprint
import json
import nltk
from nltk.stem import PorterStemmer
# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.test.utils import datapath

# spacy for lemmatization
import spacy

# Plotting tools
# import pyLDAvis
# import pyLDAvis.gensim  # don't skip this
# import matplotlib.pyplot as plt

# Enable logging for gensim - optional
import logging

from spacy.tests.pipeline.test_pipe_methods import nlp

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['rt', "ain’t", "gonna", "wanna","amp"])

dir = "/Users/vira/Downloads/"
result_dir = "Result/"
# files = os.listdir(dir)


def sent_to_words(sentences):
    for sentence in sentences:
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def remove_stopwords(texts):
    return {k: [word for word in simple_preprocess(str(doc)) if word not in stop_words] for k, doc in texts.items()}


def make_bigrams(texts):
    return {k: bigram_mod[doc] for k, doc in texts.items()}


def make_trigrams(texts):
    temp = {k: trigram_mod[bigram_mod[doc]] for k,doc in texts.items()}
    return temp


def make_quadgrams(texts):
    temp = {k: quadgram_mod[trigram_mod[bigram_mod[doc]]] for k,doc in texts}
    return temp


def lemmatization(texts, allowed_postags):
    """https://spacy.io/api/annotation"""
    texts_out = {}
    for k, sent in texts.items():
        doc = nlp(" ".join(sent))
        # texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        texts_out[k] = [token.lemma_ for token in doc if token.pos_ in allowed_postags]
    return texts_out


# for file in files:
    # if file != ".DS_Store":
file="8-28-2017.txt"
filename = str(os.path.basename(file).split('.')[0])
print(file)
f = open(dir+file, "r")
# Convert to list

# data = [line for line in f.readlines()]
#
ps = PorterStemmer()
# data = [ps.stem(sent) for sent in data]

data = {}
words = set(nltk.corpus.words.words())


for line in f.readlines():
    line = " ".join(w for w in nltk.wordpunct_tokenize(line) if w.lower() in words or not w.isalpha())
    data[ps.stem(line)] = ""

gen = sent_to_words(data.keys())

k = 0
data_words = {}
for v in gen:
    data_words[k] = v
    k = k+1

# data_words = list(sent_to_words(data))

# print(data_words[:1])

# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words.values(), min_count=5, threshold=100)  # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words.values()], threshold=100)
quadgrams = gensim.models.Phrases(trigram[data_words.values()], threshold=100) # 50 70 100

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)
quadgram_mod = gensim.models.phrases.Phraser(quadgrams)

# See trigram example
# print(trigram_mod[bigra        m_mod[data_words[0]]])

# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

data_words_bigrams_trigrams = make_trigrams(data_words_bigrams)

data_words_bigrams_trigrams_quadgrams = make_trigrams(data_words_bigrams_trigrams)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj
data_lemmatized = lemmatization(data_words_bigrams_trigrams_quadgrams, allowed_postags=['NOUN', 'ADJ'])

# print(data_lemmatized[:1])

# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized.values())
#
# Create Corpus
texts = data_lemmatized.values()
#
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# View
# print(corpus[:1])

# print ([[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]])

# Build LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=25,
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=100,
                                            alpha=0.001,
                                            per_word_topics=True)

pprint(lda_model.print_topics())
# doc_lda = lda_model[corpus]

with open(result_dir+filename+'_corpus.txt', 'w') as f:
    for item in corpus:
        f.write("%s\n" % item)

id2word.save(result_dir+filename+'_dict')

model_file = datapath(result_dir+filename+"_lda_model")
print(model_file)
lda_model.save(model_file)

#
# pyLDAvis.enable_notebook()
# vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
# vis
# Compute Perplexity

# a measure of how good the model is. lower the better.
perplexity = lda_model.log_perplexity(corpus)
print('\nPerplexity: ', perplexity)

# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)

with open(result_dir+'lda_scores.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow([filename, perplexity, coherence_lda, lda_model.print_topics()])

