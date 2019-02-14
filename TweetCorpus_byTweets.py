from gensim.corpora.textcorpus import TextCorpus
from gensim.test.utils import datapath
from gensim import utils
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.textcorpus import remove_short,lower_to_unicode,deaccent,strip_multiple_whitespaces,simple_tokenize,remove_stopwords
import os
import numpy as np
import gensim
import spacy
# spacy for lemmatization
import spacy

# Enable logging for gensim - optional
import logging

from spacy.tests.pipeline.test_pipe_methods import nlp
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords


nlp = spacy.load('en', disable=['parser', 'ner'])

# stop words 
stop_words = stopwords.words('english')
stop_words.extend(['rt', "ain’t", "gonna", "wanna","http","htt","https"])

file_order = []


# def iter_documents(top_directory):
#     """
#     Generator: iterate over all relevant documents, yielding one
#     document (=list of utf8 tokens) at a time.
#     """
#     # find all .txt documents, no matter how deep under top_directory
#     for root, dirs, files in os.walk(top_directory):
#         for fname in filter(lambda fname: fname.endswith('.txt'), files):
#             # read each document as one big string
#             document = open(os.path.join(root, fname)).read()
#             # break document into utf8 tokens
#             # yield gensim.utils.tokenize(document, lower=True, errors='ignore')
#             # yield gensim.utils.simple_preprocess(document, deacc=True)
#             file_order.append(fname)
#             print("documents tokenized")
#             yield [word for word in gensim.utils.simple_preprocess(document, deacc=True) if word not in stop_words]


# this should be changed according to the directory or file structure
def iter_documents(top_file):
    """
    Generator: iterate over all relevant documents, yielding one
    document (=list of utf8 tokens) at a time.
    """
    documents = np.genfromtxt(top_file, dtype=str, delimiter='\n')

    for document in documents:
        yield [word for word in gensim.utils.simple_preprocess(document, deacc=True) if word not in stop_words]


def lemmatization(texts, allowed_postags):
    """https://spacy.io/api/annotation"""

    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


# creating k-grams and lemmatization 
def list_all_docs(docs):
    # docs = iter_documents(top_dir)
    texts = list(docs)
    # constructiong bi-grams, tri-grams and quad-grams 
    bigram = gensim.models.Phrases(texts, min_count=200, threshold=500)  # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[texts], min_count=200, threshold=500)
    quadgrams = gensim.models.Phrases(trigram[texts], min_count=200, threshold=500)  # 50 70 100

    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    quadgram_mod = gensim.models.phrases.Phraser(quadgrams)

    data_words_bigrams_trigrams_quadgrams = []
    for doc in texts:
        data_words_bigrams_trigrams_quadgrams.append(quadgram_mod[trigram_mod[bigram_mod[doc]]])

    # lemmatization, keeping only Nouns and adjectives 
    data_lemmatized = lemmatization(data_words_bigrams_trigrams_quadgrams, allowed_postags=['NOUN', 'ADJ'])
    print("documents lemmatized")
    yield data_lemmatized


# class Tweetcorpus_byTweets
class TweetCorpus_byTweets:

    def __init__(self, top_dir):
        self.top_dir = top_dir # directory containing all the data 
        # create dictionary = mapping for documents => sparse vectors
        self.docs = list_all_docs(iter_documents(self.top_dir)) 
        self.list_docs = list(self.docs)[0] # cleaned documents 
        self.document_order = file_order # storing document order, in my case it was storing the file order in the order they were processed, remove it if not needed 
        self.id2word = gensim.corpora.Dictionary(self.list_docs) # id2word dictionary 
        self.id2word.filter_tokens(bad_ids=[self.id2word.token2id['eofeofeof']]) # remove this if not applicable for your usecase, In my case I am removing eofeofeof term that seperates documents by date from the vocabulary 
        self.corpus = [self.id2word.doc2bow(text) for text in self.list_docs if 'eofeofeof' not in text] # building corpus , eofeofeof lines are not included , remove that logic if not applicable 

    def get_texts(self):
        for doc in iter(self.docs):
            yield doc
        # for filename in self.top_dir:
        #     temp = self.split_line(open(filename).read())
        #     yield temp
        # for filename in self.input:
        #     for doc in filename.getstream():
        #         print(doc)
        #         yield [word for word in utils.to_unicode(doc).lower().split() if word not in self.stop_words]

    def __len__(self):
        return len(self.list_docs)
        # self.length = sum(1 for _ in self.get_texts())
        # return self.length

    def iterDictionary(self):
        for doc in self.list_docs:
            doc = [doc]
            yield gensim.corpora.Dictionary(doc)

    def __iter__(self):
        """
        Again, __iter__ is a generator => TxtSubdirsCorpus is a streamed iterable.
        """
        for doc in iter(self.get_texts()):
            # transform tokens (strings) into a sparse vector, one at a time
            yield self.id2word.doc2bow(doc)

    # stores the documents order in the order they were processed
    def store_doc_order(self, doc_order_filename):
        with open(doc_order_filename, 'w') as f:
            for item in self.document_order:
                f.write(item + "\n")

    # store the documents if needed for later use
    def store_docs(self, docs_filename):
        with open(docs_filename,'w') as f:
            for doc in self.list_docs:
                for item in doc:
                    f.write(item+" ")
                f.write("\n")

    # storing the corpus
    def store_corpus(self, corpus_filename):
        corpora.MmCorpus.serialize(corpus_filename, self.corpus)
        print("corpus saved")

    # storing the dictionary
    def store_dictionary(self, dictionary_filename):
        self.id2word.save(dictionary_filename)
        print("dictionary saved")
