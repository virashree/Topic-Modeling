from urllib import request
import urllib
import json
# import pysftp
import csv
import os
import shutil

dir_name = "_rawData/"
files = os.listdir(dir_name)

resultDir = "Images/"
if not os.path.exists(resultDir):
    os.makedirs(resultDir)

try:
    # with pysftp.Connection('cislinux.cis.ksu.ed-u', username='viru', password='Cisiscool@2017') as sftp:
    for file in files:
        filename = os.path.basename(file)
        print(filename)
        with open(dir_name + filename) as data_file:
            for line in data_file:
                if line != '\n':
                    data = json.loads(line)
                    images = []
                    videos = []

                    if "extended_entities" in data and data["extended_entities"] is not None \
                            and "media" in data["extended_entities"] and data["extended_entities"]["media"] is not None:
                        for media in data["extended_entities"]["media"]:
                            if media["type"] == 'photo':
                                images.append(media['media_url_https'])
                            else:
                                if "video_info" in media:
                                    if media["video_info"]["variants"]:
                                        videos.append(media["video_info"]["variants"][0]["url"])

                    folderName = str(filename.split('.')[0])
                    if not os.path.exists(resultDir+folderName):
                        os.makedirs(resultDir+folderName)

                    for i in images:
                        try:
                            imageName = i.split('/')[-1]
                            # file = open(resultDir+folderName+"/"+imageName, "wb")
                            request.urlretrieve(i, resultDir+folderName+"/"+imageName)
                            print(i, imageName)
                        except urllib.error.HTTPError as e:
                            print(e.code, i)
                            pass
                        except:
                            raise Exception("An error occurred in downloading the images")
                    for v in videos:
                        with open(resultDir+folderName+"videos.csv","a") as resultFile:
                            writer = csv.writer(resultFile)
                            writer.writerow(v)

            # print("images downloaded")
            #
            # sftp.makedirs("/home/v/viru/ImageExtraction/" + foldername)
            # with sftp.cd("/home/v/viru/ImageExtraction/" + foldername):
            #     imgs = os.listdir("Images/" + foldername)
            #     for img in imgs:
            #         imgName = os.path.basename(img)
            #         sftp.put("Images/" + foldername + "/" + imgName)
            #
            # # shutil.rmtree("Images/" + str(foldername), ignore_errors=True)
except:
    raise Exception("An error occurred!")

# sftp.close()
