import os
from nltk.stem.porter import *
import csv


dir = "/transient/viru/TopicAnalysisFiles/K_grams/"
# dir = "TfIdf/"
files = os.listdir(dir)
TF_matrix = {}
stemmer = PorterStemmer()
for file in files:
    if file != ".DS_Store":
        print(file)
        in_file = open(dir + file, 'r')
        for line in in_file:
                k_grams = line.split(',')
                for token in k_grams:
                    if "1hashtags" not in token and "2url" not in token and "3email" not in token \
                            and "4username" not in token and "5emoticon" not in token \
                            and "6htmltag" not in token and "7ascii" not in token:
                        token = token.rstrip()
                        if token != "":
                            word = stemmer.stem(token)
                            if word not in TF_matrix:
                                TF_matrix[word] = 1
                            else:
                                TF_matrix[word] = TF_matrix[word] + 1

x = sorted(TF_matrix.items(), key=lambda x: (-x[1], x[0]))


with open("output_stemmed.csv", "w") as f:
    w = csv.writer(f)
    for item in x:
        w.writerow(item)

