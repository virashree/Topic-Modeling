import os
import csv
import matplotlib.pyplot as plt
import pysftp
import numpy as np


# list_dir = ["MergedFiles_Final"]
result = {}
result['english'] = {}
result['spanish'] = {}
result['all'] = {}
dir_name = "Tweets_byDate_byLanguage"
root = "/transient/viru/"
try:
    with pysftp.Connection('cislinux.cis.ksu.edu', username='viru', password='Cisiscool@2017') as sftp:
        with sftp.cd(root+dir_name):
            directories = sftp.listdir(root+dir_name)
            for dir in directories:
                files = sftp.listdir(root+dir_name+"/"+dir)
            # for root1, dirs1, files1 in sftp.os.walk("/transient/viru/"+dir_name+"/"):
            #     for root, dirs, files in sftp.os.walk("/transient/viru/"+dir_name + "/" + dirs1[0] + "/"):
                for file in files:
                    filename = str(file.split('.')[0])
                    path = root+dir_name + "/" + dir + "/" + file
                    with sftp.open(path, 'rx') as csvfile:
                        reader = csv.reader(x.replace('\0', '') for x in csvfile)
                        next(reader)
                        try:
                            temp = sum(1 for row in reader)
                            if 'english' in filename:
                                result['english'][dir] = temp
                            elif 'spanish' in filename:
                                result['spanish'][dir] = temp
                            print(filename, temp)
                        except Exception as e:
                            print(e)

        dir_name = "IndexFilesByDate"
        # with pysftp.Connection('cislinux.cis.ksu.edu', username='viru', password='Cisiscool@2017') as sftp:
        with sftp.cd(root+dir_name):
            _files = sftp.listdir(root + dir_name)
        # for _root, _dirs, _files in os.walk("../"+dir_name+"/"):
            for file in _files:
                filename = str(file.split('.')[0])
                path = root+dir_name + "/" + file
                with sftp.open(path, 'r') as csvfile:
                    reader = csv.reader(x.replace('\0', '') for x in csvfile)
                    next(reader)
                    try:
                        temp = sum(1 for row in reader)
                        result['all'][filename] = temp
                        print(filename, temp)
                    except Exception as e:
                        print(e)
except Exception as ex:
    print(ex)


if len(result['all']) == len(result['english']) == len(result['spanish']):

    X = np.arange(len(result['all']))
    plt.bar(X, result['all'].values(), width=0.2, color='b', align='center')
    plt.bar(X-0.2, result['english'].values(), width=0.2, color='g', align='center')
    plt.bar(X-0.4, result['spanish'].values(), width=0.2, color='r', align='center')
    plt.legend(('All','English','Spanish'))
    plt.xticks(X, result['english'].keys())
    plt.title("Tweets By Date", fontsize=17)

    plt.show()
    plt.savefig('Tweets_By_Date_histogram.png')
