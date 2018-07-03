import csv
import os
# from termcolor import colored

dir_name = "../IndexFilesByDate/"

result_dir_name = "../Tweets_byDate_byLanguage/"
if not os.path.exists(result_dir_name):
    os.makedirs(result_dir_name)

files = os.listdir(dir_name)

for file in files:
    filename = str(os.path.basename(file).split('.')[0])
    path = dir_name + filename + ".csv"
    if not os.path.exists(result_dir_name+filename):
        os.makedirs(result_dir_name+filename)
    with open(path, 'r') as csvfile:
        reader = csv.reader(x.replace('\0', '') for x in csvfile)
        next(reader)
        try:
            for row in reader:
                language = row[21]
                if 'en' in language:
                    with open(result_dir_name + filename + "/" + filename + "_english.csv", "a") as resultEnglishFile:
                        writer = csv.writer(resultEnglishFile)
                        if os.stat(result_dir_name + filename + "/" + filename + "_english.csv").st_size == 0:
                            writer.writerow(
                                ["source_file", "created_at", "retweeted_status_created_at", "tweet_id", "tweet_text",
                                 "user_id", "user_name", "user_screen_name", "user_location",
                                 "user_time_zone", "user_lang", "coordinates", "place_bounding_box",
                                 "place_country_code", "place_country", "place_full_name",
                                 "place_name", "hashtags", "media_url_https", "extended_url_type", "type", "lang",
                                 "retweeted_status_tweet_id",
                                 "retweeted_status_user_screen_name", "tweet_link"])
                        writer.writerow(row)
                        # print(colored(row[21], 'green'))
                elif language == 'es':
                    with open(result_dir_name + filename + "/" + filename + "_spanish.csv", "a") as resultSpanishFile:
                        writer = csv.writer(resultSpanishFile)
                        if os.stat(result_dir_name + filename + "/" + filename + "_spanish.csv").st_size == 0:
                            writer.writerow(
                                ["source_file", "created_at", "retweeted_status_created_at", "tweet_id", "tweet_text",
                                 "user_id", "user_name", "user_screen_name", "user_location",
                                 "user_time_zone", "user_lang", "coordinates", "place_bounding_box",
                                 "place_country_code", "place_country", "place_full_name",
                                 "place_name", "hashtags", "media_url_https", "extended_url_type", "type", "lang",
                                 "retweeted_status_tweet_id",
                                 "retweeted_status_user_screen_name", "tweet_link"])
                        writer.writerow(row)
                        # print(colored(row[21], 'red'))
        except Exception as e:
            print(e)