# Author: Virashree Patel

import nltk.tokenize
from collections import Counter
import os
import operator
import math
from nltk.stem.porter import *


# this class provides useful function for plain text tokenizing and statistics
class TextProcessor:

    # tokenize the words in inputFile on white space and removes the punctuations
    # output is written in outputFile
    def tokenize(self, inputFile, outputFile):
        if type(inputFile) is str and type(outputFile) is str:
            file_content = open(inputFile).read()
            tokens = nltk.tokenize.word_tokenize(file_content)
            file = open(outputFile, 'w')
            for token in tokens:
                if re.search('[a-zA-Z]', token) is not None:
                    file.write(token.lower())
                    file.write('\n')
            file.close()
        else:
            return None

    # returns words and their occurrences in form of dictionary for the  given file
    def word_count_on_file(self, file):
        if type(file) is str:
            files = {}
            with open(file) as f:
                files[file] = {}
                words = [word for line in f for word in line.split()]
                c = Counter(words)
                for word, count in c.most_common():
                    files[file][word] = count
            f.close()
            return files
        else:
            return None

    # returns unique words with their frequencies in form of dictionary
    def word_count_on_collection(self, dir):
        if type(dir) is str:
            allWords = {}
            files = os.listdir(dir)
            for file in files:
                with open(dir+"/"+file) as f:
                    words = [word for line in f for word in line.split()]
                    c = Counter(words)
                    for word, count in c.most_common():
                        if word in allWords:
                            allWords[word] += count
                        else:
                            allWords[word] = count
                f.close()
            return allWords
        return None

    # gives number of unique words in a file or collection
    def sum_dict(self, dictionary):
        if type(dictionary) is dict:
            return sum(dictionary.values())

    # gives total number of words in a collection or file
    def dict_size(self, dictionary):
        if type(dictionary) is dict:
            return len(dictionary)

    # sorts the dictionary based on the values
    # if reverse if True sorts it in descending order otherwise in ascending order
    def dict_sort(self, dictionary, reverse):
        sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=reverse)
        return sorted_dict

    # returns number of top occurrences in the dictionary with their frequency
    def top_occurrences(self, dictionary, index):
        return dictionary[:index]

    # returns top words in form of list
    def top_words(self, dictionary, index):
        words = dictionary[:index]
        topWords = [t[0] for t in words]
        return topWords

    # lists all the stop words
    def stop_words(self):
        file = open("stopwords.txt")
        stopwords = [stopword for line in file for stopword in line.split()]
        file.close()
        return stopwords

    # checks if the given word is a stop word or not
    def is_stop_word(self, word):
        stopwords = self.stop_words()
        if any(word in stopwords for w in stopwords):
            return True
        else:
            return False

    # calculates frequency of the word in in terms of percentage
    # total is total number of words
    # words is the dictionary with words as keys and their frequency as value
    def word_occurrence_by_percentage(self, words, total):
        word_freq_data = {}
        if type(words) is dict:
            for key, value in words.items():
                percentage = (value/total) * 100
                word_freq_data[key] = percentage
        return word_freq_data

    # returns words that are responsible for coverage_percentage% in total collection
    def top_words_by_percentage_freq(self, words, coverage_percentage):
        perc = 0
        topWords = {}
        coverage_percentage = float(coverage_percentage)
        words = self.dict_sort(words, True)
        if type(words) is list:
            for w in words:
                word = w[0]
                percentage = w[1]
                if math.ceil(percentage+perc) <= coverage_percentage:
                    perc = percentage + perc
                    topWords[word] = percentage
                else:
                    break
            print(perc)
            return topWords

    # removes stop words from the given inputfile and prints result to outputfile
    def remove_stopwords(self, inputFile, outputFile):
        if type(inputFile) is str and type(outputFile) is str:
            stopwords = self.stop_words()
            with open(inputFile) as f:
                words = [word for line in f for word in line.split()]
                c = Counter(words)
                file = open(outputFile, 'w')
                for word in c.elements():
                    if word not in stopwords:
                        file.write(word)
                        file.write('\n')
                file.close()
            f.close()

    # performs stemming on the words in inputfile and write it to outputfile
    def stem(self, inputFile, outputFile):
        if type(inputFile) is str and type(outputFile) is str:
            stemmer = PorterStemmer()
            with open(inputFile) as f:
                words = [word for line in f for word in line.split()]
                c = Counter(words)
                file = open(outputFile, 'w')
                for word in c.elements():
                    file.write(stemmer.stem(word))
                    file.write('\n')
                file.close()
            f.close()























