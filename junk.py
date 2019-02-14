# import os
# from pprint import pprint

#
# dir = "/transient/viru/TopicAnalysisFiles/All_Text_Tweets_by_time_EOF/"
# files = os.listdir(dir)
#
# for file in files:
#     with open(dir+file, 'a') as f:
#         if file != ".DS_Store":
#             f.writelines("\n")
#             f.writelines("eofeofeof")
#             f.writelines("\n")
#
# result_dir = "/transient/viru/TopicAnalysisFiles/All_Text_Tweets_Tokenized_Processed/"
#
# # result_dir = "Result/"
# dateFileList = ['8-18-2017.txt','8-19-2017.txt','8-20-2017.txt','8-21-2017.txt','8-22-2017.txt'
# ,'8-23-2017.txt','8-24-2017.txt','8-25-2017.txt','8-26-2017.txt','8-27-2017.txt','8-28-2017.txt'
# ,'8-29-2017.txt','8-30-2017.txt','8-31-2017.txt','9-1-2017.txt','9-2-2017.txt','9-3-2017.txt'
# ,'9-4-2017.txt','9-5-2017.txt','9-6-2017.txt','9-7-2017.txt','9-8-2017.txt','9-9-2017.txt'
# ,'9-10-2017.txt','9-11-2017.txt','9-12-2017.txt','9-13-2017.txt','9-14-2017.txt'
# ,'9-15-2017.txt','9-16-2017.txt','9-17-2017.txt','9-18-2017.txt','9-19-2017.txt'
# ,'9-20-2017.txt','9-21-2017.txt','9-22-2017.txt','9-23-2017.txt','9-24-2017.txt','9-25-2017.txt'
# ,'9-26-2017.txt','9-27-2017.txt','9-28-2017.txt','10-4-2017.txt']
# cnt = 0
# with open("/transient/viru/TopicAnalysisFiles/_byTweets_min300_threshold_500/documents.txt", 'r') as f:
#     for line in f:
#         if "eofeofeof" in line:
#             cnt = cnt + 1
#         else:
#             with open(result_dir+dateFileList[cnt], "a") as f_o:
#                 f_o.writelines(line)
#
#
#
#

import gensim
import csv
dateFileList = ['8-18-2017.txt','8-19-2017.txt','8-20-2017.txt','8-21-2017.txt','8-22-2017.txt'
,'8-23-2017.txt','8-24-2017.txt','8-25-2017.txt','8-26-2017.txt','8-27-2017.txt','8-28-2017.txt'
,'8-29-2017.txt','8-30-2017.txt','8-31-2017.txt','9-1-2017.txt','9-2-2017.txt','9-3-2017.txt'
,'9-4-2017.txt','9-5-2017.txt','9-6-2017.txt','9-7-2017.txt','9-8-2017.txt','9-9-2017.txt'
,'9-10-2017.txt','9-11-2017.txt','9-12-2017.txt','9-13-2017.txt','9-14-2017.txt'
,'9-15-2017.txt','9-16-2017.txt','9-17-2017.txt','9-18-2017.txt','9-19-2017.txt'
,'9-20-2017.txt','9-21-2017.txt','9-22-2017.txt','9-23-2017.txt','9-24-2017.txt','9-25-2017.txt'
,'9-26-2017.txt','9-27-2017.txt','9-28-2017.txt','10-4-2017.txt']

corpus = gensim.corpora.MmCorpus('disasterTweets.mm')
id2word = gensim.corpora.Dictionary.load('disasterTweets.dict')
lda_model = gensim.models.ldamodel.LdaModel.load("lda_model")

for file in dateFileList:
    print(file)
    with open('topics_by_date_35.csv', 'a') as f, \
            open('topics_nos_by_date_35.csv', 'a') as f1:
        writer = csv.writer(f)
        writer1 = csv.writer(f1)
        document = open('documents/'+file).read()
        doc_bow = id2word.doc2bow(document.lower().split())
        topics = lda_model.get_document_topics(doc_bow,minimum_probability=0.035)
        t = []
        for topic in topics:
            t.append(topic[0])
        writer1.writerow([file, t])
        writer.writerow([file,topics])


# import csv
#
# with open("/Users/vira/Downloads/Topic_codes_by_topic.csv",'r',encoding='utf-8-sig') as f, \
#         open("/Users/vira/Downloads/Topics_num_by_date.csv",'r', encoding='utf-8-sig') as f1, \
#         open("/Users/vira/Downloads/Topic_codes_by_Date.csv",'w') as f2, \
#         open("/Users/vira/Downloads/Topic_codes.csv",'r',encoding='utf-8-sig') as f3, \
#         open("/Users/vira/Downloads/Topic_codes_names_by_Date.csv",'w') as f4, \
#         open("/Users/vira/Downloads/Topic_info.csv",'r',encoding='utf-8-sig') as f5:
#     reader = csv.reader(f)
#     reader1 = csv.reader(f1)
#     reader2 = csv.reader(f3)
#     reader3 = csv.reader(f5)
#     writer = csv.writer(f2)
#     writer1 = csv.writer(f4)
#     codes = {}  # topic codes
#     for line in reader:
#         topic_no = line[0].strip()
#         topic_codes = line[1].split(',')
#         codes[topic_no] = topic_codes
#
#     topic_info = {}  # topic - all info
#     for line in reader3:
#         topic_no = line[0].strip()
#         topic_codes = line[1].split(',')
#         topic_pda = line[2].strip().split(',')
#         disaster = line[3].strip().split(',')
#         place = line[4].strip().split(',')
#         special = line[5].strip().split(',')
#         organization = line[6].strip().split(',')
#         topic_info[topic_no] = {'topic_codes':topic_codes,'pda':topic_pda,'disaster':disaster,'place':place,'special':special,'organization':organization}
#
#     topics_date = {}  # date - topic no
#     for line in reader1:
#         date = line[0].strip()
#         topics = [item.strip() for item in line[1].split(',')]
#         topics_date[date] = topics
#
#     topic_date_pda={}  # date - pda
#     topics_date_code = {}
#     topic_date_disaster = {}
#     topic_date_place = {}
#     topic_date_special = {}
#     topic_date_org = {}
#     for date,topic_nums in topics_date.items():
#         topic_pda = []
#         topics_codes = set()
#         topic_place = set()
#         topic_disaster = set()
#         topic_special = set()
#         topic_org = set()
#         for topic in topic_nums:
#             topics_codes.update(topic_info[topic]['topic_codes'])
#             topic_pda = topic_pda + topic_info[topic]['pda']
#             topic_disaster.update(topic_info[topic]['disaster'])
#             topic_place.update(topic_info[topic]['place'])
#             topic_special.update(topic_info[topic]['special'])
#             topic_org.update(topic_info[topic]['organization'])
#         topic_date_pda[date] = topic_pda
#         topics_date_code[date] = list(topics_codes)
#         topic_date_disaster[date] = list(topic_disaster)
#         topic_date_place[date] = list(topic_place)
#         topic_date_org[date] = list(topic_org)
#         topic_date_special[date] = list(topic_special)


    # topic_codes = {}  # code no - code name
    # for line in reader2:
    #     code_no = line[0]
    #     code_name = line[1]
    #     topic_codes[code_no] = code_name
    # print(topic_codes)
    #
    # for file, codes in topics_date_code.items():
    #     codes = [int(x) for x in codes]
    #     codes = sorted(codes)
    #     code_names = []
    #     for code in codes:
    #         code_names.append(topic_codes[str(code)])
    #     print(code_names)
    #     writer.writerow([file, ",".join(str(x) for x in codes), ",".join(str(x) for x in topic_date_pda[file])])
    #     writer1.writerow([file, ",".join(str(x) for x in code_names), ",".join(str(x) for x in topics_date[file]),
    #                       ",".join(str(x) for x in topic_date_pda[file]),",".join(str(x) for x in topic_date_disaster[file]),
    #                       ",".join(str(x) for x in topic_date_place[file]), ",".join(str(x) for x in topic_date_special[file]),
    #                       ",".join(str(x) for x in topic_date_org[file])])


# import csv
#
# with open("//home/ec2-user/Data/Result/Corpus/_byTweets_min200_th500_bytime/filelist.csv",'r') as f:
#     reader = csv.reader(f)
#     filelist = []
#     for line in reader:
#         filelist = filelist + line
#     cnt = 0
#     l = len(filelist)
#     with open("/home/ec2-user/Data/Result/Corpus/_byTweets_min200_th500_bytime/documents.txt", 'r') as f:
#         for line in f:
#             if "eofeofeof" in line:
#                 cnt = cnt + 1
#                 if cnt < l:
#                     print(filelist[cnt])
#                 else:
#                     break
#             else:
#                 with open("/home/ec2-user/Data/Result/Corpus/_byTweets_min200_th500_bytime/documents/"+filelist[cnt], "a") as f_o:
#                     f_o.writelines(line)

# import gensim
# import csv
#
# corpus = gensim.corpora.MmCorpus('disasterTweets.mm')
# id2word = gensim.corpora.Dictionary.load('disasterTweets.dict')
# lda_model = gensim.models.ldamodel.LdaModel.load("lda_model")
# with open("_byTweets_min200_th500_bytime/filelist.csv",'r') as f:
#     reader = csv.reader(f)
#     dateFileList = []
#     for line in reader:
#         dateFileList = dateFileList + line
# for file in dateFileList:
#     print(file)
#     with open('_byTweets_min200_th500_bytime/topics_by_hour_all.csv', 'a') as f, open('_byTweets_min200_th500_bytime/topics_num_by_hour_all.csv', 'a') as f1:
#         writer = csv.writer(f)
#         writer1 = csv.writer(f1)
#         document = open('_byTweets_min200_th500_bytime/documents/'+file).read()
#         doc_bow = id2word.doc2bow(document.lower().split())
#         topics = lda_model.get_document_topics(doc_bow)
#         t = []
#         for topic in topics:
#             t.append(topic[0])
#         writer1.writerow([file, ",".join(str(x) for x in t)])
#         writer.writerow([file,topics])

import csv

with open("/Users/vira/Downloads/Hours_9-11_02.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    all_topics = {}
    for line in reader:
        hour = line[0]
        topics = line[1].split(',')
        all_topics[hour]= topics
        print(hour ,":",all_topics[hour])
    list_topics = list(all_topics.values())
    flat_list = [item for sublist in list_topics for item in sublist]
    print("all topics", set(flat_list), len(set(flat_list)))
    common_topics = list(set(list_topics[0]).intersection(*list_topics))
    print(common_topics)
    all_topics_list = list(all_topics.values())
    for i, topics in enumerate(all_topics_list):
        if i != 0:
            changed_topics = [t for t in topics if t not in all_topics_list[i-1]]
            print(i, ":", changed_topics)


    # print(common_topics)
    # uncommon_topics = {}
    # for hour, topics in all_topics.items():
    #     uncommon_topics[hour] = [t for t in all_topics[hour] if t not in common_topics]
    #     print(hour, ":", uncommon_topics[hour])
    # super_list = []
    # for k, t in uncommon_topics.items():
    #     super_list = super_list + t
    # print(Counter(super_list))


# 4 , 29, 9
#
# import os
# from gensim import corpora
# from gensim.corpora.mmcorpus import MmCorpus
# from gensim.test.utils import datapath
# import ast
# rootdir="/Users/vira/Downloads/DateCorpus/"
#
# for subdir, dirs, files in os.walk(rootdir):
#     for dir in dirs:
#         dirpath = os.path.join(rootdir, dir)
#         print(dirpath)
#         # corpus = corpora.MmCorpus(dirpath+'/disasterTweets.mm')
#         corpus = MmCorpus(datapath(dirpath+'/disasterTweets.mm'))
#         # corpus = corpora.MmCorpus.serialize(dirpath+'/disasterTweets.txt', corpus)
#         MmCorpus.save_corpus(dirpath+'/disasterTweets.txt', corpus)
#         print(corpus)
#         corpus=[]
#         with open(dirpath+'/disasterTweets.txt', 'r') as f:
#             for line in f:
#                 line = ast.literal_eval(line.rstrip())
#                 corpus.append(line)
#
#


