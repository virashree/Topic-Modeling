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

stop_words = stopwords.words('english')
stop_words.extend(['rt', "ain’t", "gonna", "wanna"])

file_order = []


def iter_documents(top_directory):
    """
    Generator: iterate over all relevant documents, yielding one
    document (=list of utf8 tokens) at a time.
    """
    # find all .txt documents, no matter how deep under top_directory
    for root, dirs, files in os.walk(top_directory):
        for fname in filter(lambda fname: fname.endswith('.txt'), files):
            # read each document as one big string
            document = open(os.path.join(root, fname)).read()
            # break document into utf8 tokens
            # yield gensim.utils.tokenize(document, lower=True, errors='ignore')
            # yield gensim.utils.simple_preprocess(document, deacc=True)
            file_order.append(fname)
            print("documents tokenized")
            yield [word for word in gensim.utils.simple_preprocess(document, deacc=True) if word not in stop_words]


def lemmatization(texts, allowed_postags):
    """https://spacy.io/api/annotation"""

    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def list_all_docs(docs):
    # docs = iter_documents(top_dir)
    texts = list(docs)
    bigram = gensim.models.Phrases(docs, min_count=100, threshold=100)  # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[docs], min_count=1, threshold=1)
    quadgrams = gensim.models.Phrases(trigram[docs], min_count=1, threshold=1)  # 50 70 100

    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    quadgram_mod = gensim.models.phrases.Phraser(quadgrams)

    data_words_bigrams_trigrams_quadgrams = []
    for doc in texts:
        data_words_bigrams_trigrams_quadgrams.append(quadgram_mod[trigram_mod[bigram_mod[doc]]])
    data_lemmatized = lemmatization(data_words_bigrams_trigrams_quadgrams, allowed_postags=['NOUN', 'ADJ'])
    print("documents lemmatized")
    yield data_lemmatized

# docs = iter_documents(dir)
# data = k_grams(docs)
# cnt = 0
# for d in data:
#     cnt += 1
# print(cnt)


class TweetsCorpus:

    def __init__(self, top_dir):
        self.top_dir = top_dir
        # create dictionary = mapping for documents => sparse vectors
        self.docs = self.list_all_docs(iter_documents(self.top_dir))
        self.list_docs = list(self.docs)[0]
        self.document_order = file_order
        # self.vocab = self.k_grams()
        self.id2word = gensim.corpora.Dictionary(self.list_docs)
        self.corpus = [self.id2word.doc2bow(text) for text in self.list_docs]
        # self.corpus_filename = 'disasterTweets.mm'
        # self.dictionary_filename = 'disasterTweets.dict'
        # self._corpus = corpora.MmCorpus(self.corpus_filename)
        # self._id2word = corpora.Dictionary.load(self.dictionary_filename)
    # def split_line(self, text):
    #     # words = text.split()
    #     words = self.preprocess(text)
    #
    #     out = []
    #     for word in words:
    #         if word not in self.stop_words:
    #             out.append(word)
    #     return out
    #

    def iter_documents(self,top_directory):
        """
        Generator: iterate over all relevant documents, yielding one
        document (=list of utf8 tokens) at a time.
        """
        # find all .txt documents, no matter how deep under top_directory
        for root, dirs, files in os.walk(top_directory):
            for fname in filter(lambda fname: fname.endswith('.txt'), files):
                # read each document as one big string
                document = open(os.path.join(root, fname)).read()
                # break document into utf8 tokens
                # yield gensim.utils.tokenize(document, lower=True, errors='ignore')
                # yield gensim.utils.simple_preprocess(document, deacc=True)
                file_order.append(fname)
                print("documents tokenized")
                yield [word for word in gensim.utils.simple_preprocess(document, deacc=True) if word not in stop_words]

    def lemmatization(self,texts, allowed_postags):
        """https://spacy.io/api/annotation"""
        print("starting lemmatization")
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent))
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    def list_all_docs(self,docs):
        # docs = iter_documents(top_dir)
        texts = list(docs)
        bigram = gensim.models.Phrases(docs, min_count=100, threshold=1000)  # higher threshold fewer phrases.
        trigram = gensim.models.Phrases(bigram[docs], min_count=100, threshold=1000)
        quadgrams = gensim.models.Phrases(trigram[docs], min_count=100, threshold=1000)  # 50 70 100

        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)
        quadgram_mod = gensim.models.phrases.Phraser(quadgrams)

        data_words_bigrams_trigrams_quadgrams = []
        for doc in texts:
            data_words_bigrams_trigrams_quadgrams.append(quadgram_mod[trigram_mod[bigram_mod[doc]]])
        print("bigrams trigramd quadgrams formed")
        data_lemmatized = lemmatization(data_words_bigrams_trigrams_quadgrams, allowed_postags=['NOUN', 'ADJ'])
        print("documents lemmatized")
        yield data_lemmatized

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

    def store_corpus(self, corpus_filename):
        corpora.MmCorpus.serialize(corpus_filename, self.corpus)
        print("corpus saved")

    def store_dictionary(self, dictionary_filename):
        self.id2word.save(dictionary_filename)
        print("dictionary saved")
    # def sent_to_words(self, sentence):
    #     # for sentence in sentences:
    #     yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
    #
    # def remove_stopwords(self, texts):
    #     return np.array([[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts])
    #
    # def preprocess(self, text):
    #     # text = lower_to_unicode(text)
    #     # text = deaccent(text)
    #     # text = strip_multiple_whitespaces(text)
    #     # text = simple_tokenize(text)
    #     text = remove_short(text, 2)
    #     text = remove_stopwords(text)
    #     return text


