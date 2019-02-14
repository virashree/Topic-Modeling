import os
import csv

# from textblob import TextBlob

dir = "/transient/viru/TopicAnalysisFiles/tweets_all_en/"
result_dir = "/transient/viru/TopicAnalysisFiles/Tweets_all_not_cleaned/"
files = os.listdir(dir)

for file in files:
    if file != ".DS_Store":
        filename = str(os.path.basename(file).split('.')[0])
        with open(dir + file, 'r') as f, open(result_dir+filename+'.txt', 'w') as f_o:
            reader = csv.reader(x.replace('\0', '') for x in f)
            next(reader)  # skips the header
            for row in reader:
                f_o.write(row[5]+"\n")

#
#
# for file in files:
#     if file != ".DS_Store":
#         filename = str(os.path.basename(file).split('.')[0])
#         with open(dir + file, 'r') as f, open(result_dir+filename+'.csv', 'w') as f_o:
#             reader = csv.reader(x.replace('\0', '') for x in f)
#             writer = csv.writer(f_o)
#             next(reader) # skips the header
#             for row in reader:
#                 if row[21] == 'en':
#                     writer.writerow(row)

# text="the quick brown fox jumped over the lazy sleeping dog le rapide goupil brun sauta par dessus le chien paresseux " \
#      "sommeil el zorro marrón rápido saltó sobre el perro que duerme perezoso BLM FEMA MAGA "

# english_vocab = set(w.lower() for w in nltk.corpus.words.words())
# text_vocab = set(w.lower() for w in text.split(" ") if w.lower().isalpha())
# unusual = text_vocab.difference(english_vocab)

# print(detect("bronco"))

# b = TextBlob("hola")
# print(b.detect_language())


