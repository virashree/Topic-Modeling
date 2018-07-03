import json
import os
import csv

# result directory
result_dir_name = "/transient/viru/IndexFiles/"
if not os.path.exists(result_dir_name):
    os.makedirs(result_dir_name)

# source directory with json file
source_dir = "/transient/viru/harvey_twitter_dataset/02_archive_only/"
files = os.listdir(source_dir)

# for file in files:
filename = 'HurricaneHarvey' # os.path.basename(file)
newPath = result_dir_name + "/" + filename + '.csv'
# newPath = ""
with open(newPath, "w") as f:
    writer = csv.writer(f)

    writer.writerow(
        ["source_file", "created_at", "retweeted_status_created_at", "tweet_id", "tweet_text", "user_id", "user_name", "user_screen_name", "user_location",
         "user_time_zone", "user_lang", "coordinates", "place_bounding_box", "place_country_code", "place_country", "place_full_name",
         "place_name", "hashtags", "media_url_https", "extended_url_type", "type", "lang", "retweeted_status_tweet_id",
         "retweeted_status_user_screen_name", "tweet_link"])

    # for file in files:
    # filename = "hurricane_twitter.json" # os.path.basename(file)
    with open(source_dir+filename+'.json','r') as data_file:
        for line in data_file:
            if line is not "\n":
                data = json.loads(line)

                if "created_at" and "text" in data:

                    #if "retweeted_status" in data and data["retweeted_status"]["id"] is not None:
                        #print(data["retweeted_status"]["id"])

                    urls = []
                    types = []
                    video_types = []
                    if "extended_entities" in data and data["extended_entities"] is not None \
                            and "media" in data["extended_entities"] and data["extended_entities"]["media"] is not None:
                        for media in data["extended_entities"]["media"]:
                            if "video_info" in media:
                                for v in media["video_info"]["variants"]:
                                    urls.append(v["url"])
                                    types.append(media["type"])
                                    video_types.append((v["content_type"]))
                            else:
                                urls.append(media["media_url_https"])
                                types.append(media["type"])

                    writer.writerow(["HurricaneHarvey.json",
                                     data["created_at"] if "created_at" in data else " ",
                                     data["retweeted_status"]["created_at"] if "retweeted_status" in data and
                                                    "retweeted_status" is not None and
                                                    data["retweeted_status"]["created_at"] is not None
                                                    else " ",
                                     # data["created_at"],
                                     data["id"] if "id" in data else " ",
                                     # data["retweeted_status"]["text"] if "retweeted_status" in data and
                                     #                 "retweeted_status" is not None and
                                     #                 data["retweeted_status"]["text"] is not None
                                     #                 else data["text"],
                                     data["text"],
                                     data["user"]["id"] if "user" in data and "id" in data["user"] else " ",
                                     data["user"]["name"] if "user" in data and "name" in data["user"] else " ",
                                     data["user"]["screen_name"] if "user" in data and "screen_name" in data["user"] else " ",
                                     data["user"]["location"] if "user" in data and "location" in data["user"] else " ",
                                     data["user"]["time_zone"] if "user" in data and "time_zone" in data["user"] else " ",
                                     data["user"]["lang"] if "user" in data and "lang" in data["user"] else " ",

                                     data["coordinates"]["coordinates"] if "coordinates" in data
                                                                           and data["coordinates"] is not None
                                                                           and "coordinates" in data["coordinates"] else " ",

                                     data["place"]["bounding_box"]["coordinates"] if "place" in data and
                                                                                     data["place"] is not None and
                                                                                     data["place"]["bounding_box"] is not None and
                                                                                     data["place"]["bounding_box"]["coordinates"] is not None
                                                                                     else " ",

                                     data["place"]["country_code"] if "place" in data and data["place"] is not None and
                                                                 data["place"]["country_code"] is not None else " ",

                                     data["place"]["country"] if "place" in data and data["place"] is not None and
                                                                 data["place"]["country"] is not None else " ",

                                     data["place"]["full_name"] if "place" in data and data["place"] is not None and
                                                                data["place"]["full_name"] is not None else " ",

                                     data["place"]["name"] if "place" in data and data["place"] is not None and
                                                                data["place"]["name"] is not None else " ",

                                     data["entities"]["hashtags"] if "entities" in data and data["entities"] is not None and
                                                                     data["entities"]["hashtags"] is not None else " ",

                                     [url for url in urls],

                                     [video_type for video_type in video_types],

                                     [type for type in types],

                                     data["lang"] if "lang" in data and data["lang"] is not None else " ",


                                     data["retweeted_status"]["id"] if "retweeted_status" in data and
                                                                     data["retweeted_status"] is not None and
                                                                     data["retweeted_status"]["id"] is not None
                                                                     else " ",

                                     data["retweeted_status"]["user"]["screen_name"] if "retweeted_status" in data and
                                                                                    data["retweeted_status"] is not None and
                                                                                    data["retweeted_status"]["user"] is not None and
                                                                                    data["retweeted_status"]["user"]["screen_name"] is not None
                                                                                    else " ",

                                     "https://twitter.com/" + data["retweeted_status"]["user"][
                                         "screen_name"] + "/status/" + str(data["retweeted_status"]["id"])
                                            if "retweeted_status" in data and data["retweeted_status"] is not None
                                            else
                                                "https://twitter.com/" + data["user"]["screen_name"] + "/status/" + str(data["id"])
                                                if "user" in data and data["user"] is not None
                                                else " "
                                     ])
