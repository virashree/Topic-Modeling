import csv
import os
import matplotlib.pyplot as plt
import numpy as np


dir_name = "/transient/viru/IRMA-extra-tweets-index-withoutduplicates/"

# with pysftp.Connection('cislinux.cis.ksu.edu', username='viru', password='Cisiscool@2017') as sftp:
#     with sftp.cd(root + dir_name):
#         _files = sftp.listdir(root + dir_name)

# for _root, _dirs, _files in os.walk("../"+dir_name+"/"):
#     for file in _files:
#         filename = str(file.split('.')[0])
        # path = root + dir_name + "/" + file
retweet_count = 0
        # tweet_count = 0
with open(dir_name+'IRMA_2017-09-05_withoutDuplicates.csv', 'r') as csvfile:
    reader = csv.reader(x.replace('\0', '') for x in csvfile)
    next(reader)
    for row in reader:
        if row[22] != ' ':
            retweet_count += 1
        # tweet_count += 1
    print(retweet_count)
    # data[file] = [retweet_count, tweet_count]
    # print(file,retweet_count,tweet_count)
#
# with open('Retweet_count_filtered_english_tweets.csv', 'w') as file:
#     writer = csv.writer(file)
#     for key, value in data.items():
#         writer.writerow([key, value[0], value[1]])

#
# X = np.arange(len(data))
#
# for key, value in data.items():
#     plt.bar(X, value[0], width=0.2, color='b', align='center')
#     plt.bar(X-0.2, value[1], width=0.2, color='g', align='center')
# plt.xticks(X, data.keys())
# plt.title("Retweet Count", fontsize=17)
#
# plt.show()
# plt.savefig('Retweet_count.png')
#
#
#
