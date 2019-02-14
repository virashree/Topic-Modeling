import os
import csv

dir = "/transient/viru/TopicAnalysisFiles/K-gram_files/"
result_dir = "/transient/viru/TopicAnalysisFiles/K-grams_ranked/"
input_dir = "/transient/viru/TopicAnalysisFiles/TfIdf/"
# dir = "K_grams_files/"
# result_dir = "K_grams_ranked/"
# input_dir = "TfIdf/"
files = os.listdir(dir)
# in_files = os.listdir(input_dir)

for file in files:
    if file != "":
        print(file)
        k_grams_tfIdf = {}
        tfIdf = {}
        filename = str(os.path.basename(file).split('.')[0])

        with open(dir+file, "r") as f, open(result_dir+filename+".csv", "w") as f_o, \
                open(input_dir+filename+"_tfIdf.csv", "r") as f_in:
            reader = csv.reader(f_in)
            # looping through file to read tf-ifd for each word and storing in a Dict
            for row in reader:
                tfIdf[row[0]] = float(row[1])

            for row in f:
                row = row.strip('\n')
                if row != "":
                    try:
                        k_grams = row.split(",")
                        for k_gram in k_grams:
                            score = 0
                            tokens = k_gram.split(" ")  # getting all words from the k-gram separated by a white space
                            words = []
                            for token in tokens:
                                word = token.split("_")[0]  # removing the pos tag to get the term
                                words.append(word)
                                score += tfIdf[word]    # summing the tf-idf score for each uni-gram
                            k_grams_tfIdf[" ".join(words)] = score
                    except Exception as e:
                        print(e)
            # sorted(k_grams_tfIdf, key=k_grams_tfIdf.get, reverse=True)
            for key, value in k_grams_tfIdf.items():
                writer = csv.writer(f_o)
                writer.writerow([key, value])
