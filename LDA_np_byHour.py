from pprint import pprint

# Gensim
import gensim


from TweetsCorpus import TweetsCorpus
import os
# Enable logging for gensim - optional
import logging
from gensim.test.utils import datapath
from gensim.models import CoherenceModel
import csv
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
import gensim.corpora as corpora

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# dir = "/transient/viru/TopicAnalysisFiles/All_Text_Tweets_Preprocessed/"
# result_dir = "/transient/viru/TopicAnalysisFiles/All_Text_Tweets_Preprocessed/"

dir = "/Users/vira/PycharmProjects/TopicModeling/Tweet_cleaned/"
result_dir = "Result/"

# docs = []
#
# for file in files:
#     print(file)
#     # filename = str(os.path.basename(file).split('.')[0])
#     filepath = dir+dir_name+"/"+file
#     f = open(filepath, "r")
#     f_data = np.genfromtxt(filepath, dtype=str, delimiter='\n')
#     # data_words = list(sent_to_words(f_data))
#     # data_words_nostops = remove_stopwords(list(sent_to_words(f_data)))
#     docs.append(remove_stopwords(list(sent_to_words(f_data))))
#
# data = np.array(docs)

# files = os.listdir(dir+dir_name+"/")
# for i, file in enumerate(files):
#     files[i] = dir+dir_name+"/"+file

# sentences = sentences.get_texts()

# sentences = Text8Corpus(datapath('testcorpus.txt'))
# id2word = corpora.Dictionary(sentences)
#
# corpus = [id2word.doc2bow(text) for text in sentences]

# id2word = gensim.corpora.Dictionary(sentences.docs)

# sentences.initializer()
# sentences.store_corpus(result_dir+"disasterTweets.mm")
# sentences.store_dictionary(result_dir+"disasterTweets.dict")

# docs = sentences.list_docs
# test = iter(sentences.docs)
# print(len(sentences))
# id2word = sentences.id2word
# corpus = sentences
# document_order = sentences.document_order
# dicts = sentences.iterDictionary()

# for i, id2word in enumerate(dicts):
#     lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
#                                                 id2word=id2word,
#                                                 num_topics=24,
#                                                 update_every=1,
#                                                 chunksize=1,
#                                                 passes=1)
#
#     pprint(lda_model.print_topics())
#     filename = document_order[i]
#
#     with open(result_dir+filename+'_corpus.txt', 'w') as f:
#         for item in corpus:
#             f.write("%s\n" % item)
#
#     id2word.save(result_dir+filename+'_dict')
#
#     model_file = datapath(result_dir+filename+"_lda_model")
#     # print(model_file)
#     lda_model.save(model_file)
#
#     #
#     # pyLDAvis.enable_notebook()
#     # vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
#     # vis
#     # Compute Perplexity
#
#     # a measure of how good the model is. lower the better.
#     perplexity = lda_model.log_perplexity(corpus)
#     print('\nPerplexity: ', perplexity)
#
#     # Compute Coherence Score
#     coherence_model_lda = CoherenceModel(model=lda_model, texts=sentences.list_docs, dictionary=id2word, coherence='c_v')
#     coherence_lda = coherence_model_lda.get_coherence()
#     print('\nCoherence Score: ', coherence_lda)
#
#     with open(result_dir+'lda_scores.csv', 'a') as f:
#         writer = csv.writer(f)
#         writer.writerow([filename, perplexity, coherence_lda, lda_model.print_topics()])

sentences = TweetsCorpus(dir+"8-18-2017.txt")

# vocab = sentences.id2word.token2id
# dictionary = sentences.id2word
sentences.store_corpus(result_dir+"disasterTweets.mm")
sentences.store_dictionary(result_dir+"disasterTweets.dict")
sentences.store_docs(result_dir+"documents.txt")
# corpus = sentences.corpus
# sentences.store_doc_order(result_dir+"document_order.txt")
# print(sentences.corpus[:1])


# corpus = gensim.corpora.MmCorpus('Tweet_cleaned/disasterTweets.mm')
# print(corpus[:1])
# id2word = gensim.corpora.Dictionary.load('Tweet_cleaned/disasterTweets.dict')
# vocab = id2word.token2id
#
# lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
#                                             id2word=id2word,
#                                             num_topics=10)
#
# pprint(lda_model.print_topics())
# new_doc = "harvey is coming to barbado and caribbean"
# doc_bow = id2word.doc2bow(new_doc.lower().split())
# print(doc_bow)
#
# doc_lda = lda_model[doc_bow]
# print(doc_lda)
# print(lda_model[doc_bow])
# with open(result_dir+'corpus.txt', 'w') as f:
#     for item in corpus:
#         f.write("%s\n" % item)
#
# model_file = datapath(result_dir+"lda_model")

