from collections import Counter
import csv
import os

in_dir = "TA_Collection/K-grams/"
result_dir = "TA_Collection/DF_matrix/"

if not os.path.exists(result_dir):
    os.makedirs(result_dir)
# dir = "/transient/viru/TopicAnalysisFiles/K_grams/"
dirs = os.listdir(in_dir)
for dir in dirs:
    documents = []
    files = os.listdir(in_dir + dir)
    for file in files:
        with open(in_dir + dir+"/"+file, 'r') as f:
            words = [word for line in f for word in line.split(',') if word != "\n" and "1hashtags" not in word
                     and "2url" not in word and "3email" not in word and "4username" not in word
                     and "5emoticon" not in word and "6htmltag" not in word and "7ascii" not in word]
            documents.append(words)

    word_frequencies = [Counter(document) for document in documents]
    terms = []
    for word_frequency in word_frequencies:
        terms = terms + list(word_frequency.keys())
    document_frequencies = Counter(terms)
    document_frequencies = sorted(document_frequencies.items(), key=lambda x: (-x[1], x[0]))
    # print(document_frequencies)

    if not os.path.exists(result_dir+dir):
        os.makedirs(result_dir+dir)

    with open(result_dir+dir+"/"+"DF_matrix.csv", 'w') as f:
        w = csv.writer(f)
        for item in document_frequencies:
            w.writerow(item)