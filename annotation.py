import csv
import os

tweet_ids = {}

dir_name = "../MergedFiles/"

result_dir_name = "../MergedFiles_Revised/"
if not os.path.exists(result_dir_name):
    os.makedirs(result_dir_name)

files = os.listdir(dir_name)

for file in files:

    if os.path.basename(file) != '.DS_Store':
        filename = str(os.path.basename(file).split('.')[0])
        path = dir_name + filename + ".csv"
        with open(path, 'r') as csvfile:
            reader = csv.reader(x.replace('\0', '') for x in csvfile)
            next(reader)
            try:
                for row in reader:
                    if row[22] == '' or ' ' or None:
                        original_id = int(row[3])
                        tweet_id = int(row[3])
                    else:
                        original_id = int(row[22])
                        tweet_id = int(row[3])

                    if original_id not in tweet_ids and tweet_id not in tweet_ids:
                        tweet_ids[original_id] = ''
                        if tweet_id != original_id:
                            tweet_ids[tweet_id] = ''

                        with open(result_dir_name + filename + ".csv", "a") as resultFile:
                            writer = csv.writer(resultFile)
                            writer.writerow(row)
                    else:
                        with open(result_dir_name + filename + "_duplicate" + ".csv", "a") as resultFile_r, \
                                open(result_dir_name + filename + ".csv", "a") as resultFile:
                            writer_r = csv.writer(resultFile_r)
                            writer = csv.writer(resultFile)

                            writer_r.writerow(row)
                            writer.writerow(row)
                            print(row)
            except Exception as e:
                print(e)