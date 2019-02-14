import pyLDAvis
import os
import csv
from nltk.stem import PorterStemmer
from gensim import corpora, models

ps = PorterStemmer()

# dir = "/transient/viru/TopicAnalysisFiles/K_grams/"
dir = "K_grams/"
files = os.listdir(dir)

# result_dir = "/transient/viru/TopicAnalysisFiles/K_grams_relevant/"
result_dir = "K_grams_relevant/"
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# result_dir_1 = "/transient/viru/TopicAnalysisFiles/Doc_term_matrix/"
result_dir_1 = "Doc_term_matrix/"
if not os.path.exists(result_dir_1):
    os.makedirs(result_dir_1)
vocab = {}

with open("output_stemmed.csv", 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        if int(line[1]) > 100:
            vocab[line[0]] = line[1]

# open(result_dir+file, 'w') as f_out
# , open(result_dir_1+"DM.csv", 'w')
docs = []
for file in files:
    terms = []
    with open(dir+file,'r') as f_in:
        for line in f_in:
            k_grams = line.split(',')
            temp = []
            for k_gram in k_grams:
                # k_gram = ps.stem(k_gram)
                if k_gram in vocab:
                    temp.append(k_gram)
                    terms.append(k_gram)
            # f_out.writelines(",".join(temp))
            # f_out.writelines("\n")
    docs.append(terms)

dictionary = corpora.Dictionary(docs)

# document - term matrix
corpus = [dictionary.doc2bow(doc) for doc in docs]

# Lda = models.ldamodel.LdaModel

# running lda model
lda_model = models.ldamodel.LdaModel(corpus, num_topics=8, id2word=dictionary, passes=50)

tweets_data = pyLDAvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(tweets_data)

# deriving the topics
lda_topics = lda_model.print_topics(num_topics=8, num_words=4)
print(lda_topics)
# print the topics

for lda_topic in lda_topics:
    topic_terms_with_prob = str(lda_topic[1]).split(' + ')
    topic = " ".join([term.split('*')[1].strip('\"') for term in topic_terms_with_prob])
    print(topic)

# # LDA using single core
# dictionary = corpora.Dictionary(filtered_tweets)
# corpus = [dictionary.doc2bow(text) for text in filtered_tweets]

# # model the topics
# ldamodel = models.ldamodel.LdaModel(corpus, num_topics=8, id2word = dictionary, passes=50)