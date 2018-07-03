from collections import Counter
import csv
import os

dir = "/transient/viru/TopicAnalysisFiles/K_grams"
files = os.listdir(dir)
documents = []

for file in files:
    with open(dir+"/"+file, 'r') as f:
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

with open("/transient/viru/TopicAnalysisFiles/DF_matrix.csv", 'w') as f:
    w = csv.writer(f)
    for item in document_frequencies:
        w.writerow(item)