import json
import os
from shutil import copyfile
import csv
from urllib import request
import urllib


dir_name = "result2.json"
files = os.listdir(dir_name)

irmaKeywords = ["miami","florida","orlando","irma","florida keys island","floridakeysisland","barbuda","cuba","caribbean","keysisland",
                "keys island","haiti","turks","caicos","St. Barts","St. Martin","St Martin","St Barts","stbarts","stmartin","edenrock"]
harveyKeywords = ["harvey","houston","houstonfloods","hurricaneharveyrelief","corpuschristi","corpus christi"]
mariaKeywords = ["maria","puerto rico", "puertorico","San Juan","SanJuan","hurricanemaria","Hurricane Maria"]

paths = ["Harvey", "Maria", "Irma", "Ambiguous"]
for newpath in paths:
    if not os.path.exists(newpath):
        os.makedirs(newpath)

for file in files:
    filename = os.path.basename(file)
    if filename.split('.')[-1] == 'json':
        folderName = str(filename.split('.')[0])  # folder name used for images as well
        imageFolderName = folderName[:10]

        with open(dir_name + "/" + filename) as data_file:
            print(filename)
            for line in data_file:
                tweet = json.loads(line)

                # print(tweet)
                photos = tweet['media_url_https']
                text = tweet['text']
                hashtags = tweet['hashtags']
                tweetId = tweet['id']

                for photo in photos:
                    imgName = photo.split('/')[-1]  # image name used
                    harvey = 0
                    irma = 0
                    maria = 0

                    src = "/home/v/viru/ImagesExtraction/" + imageFolderName + "/" + imgName

                    for hashtag in hashtags:
                        hashtag = hashtag['text'].lower()
                        if hashtag in harveyKeywords:
                            harvey = harvey + 1
                        elif hashtag in irmaKeywords:
                            irma = irma + 1
                        elif hashtag in mariaKeywords:
                            maria = maria + 1

                    if harvey > 0 and maria == 0 and irma == 0:  # single match found
                        dst = "Harvey/" + folderName
                        if not os.path.exists(dst):
                            os.makedirs(dst)
                        writer = csv.writer(open("Harvey/"+folderName+".csv", "a"))
                        writer.writerow([str(tweetId)])

                    elif irma > 0 and maria == 0 and harvey == 0:
                        # src = "/home/v/viru/ImagesExtraction/" + imageFolderName + "/" + imgName
                        dst = "Irma/" + folderName
                        if not os.path.exists(dst):
                            os.makedirs(dst)
                        # copyfile(src, dst + "/" + imgName)
                        writer = csv.writer(open("Irma/"+folderName+".csv", "a"))
                        writer.writerow([str(tweetId)])

                    elif maria > 0 and irma == 0 and harvey == 0:
                        # src = "/home/v/viru/ImagesExtraction/" + imageFolderName + "/" + imgName
                        dst = "Maria/" + folderName
                        if not os.path.exists(dst):
                            os.makedirs(dst)
                        # copyfile(src, dst + "/" + imgName)
                        writer = csv.writer(open("Maria/"+folderName+".csv", "a"))
                        writer.writerow([str(tweetId)])

                    elif harvey == 0 and maria == 0 and irma == 0:  # if no match found
                        text = text.lower()
                        if any(word in text for word in harveyKeywords):
                            # src = "/home/v/viru/ImagesExtraction/" + imageFolderName + "/" + imgName
                            dst = "Harvey/" + folderName
                            if not os.path.exists(dst):
                                os.makedirs(dst)
                            # copyfile(src, dst + "/" + imgName)
                            writer = csv.writer(open("Harvey/"+folderName+".csv", "a"))
                            writer.writerow([str(tweetId)])

                        elif any(word in text for word in irmaKeywords):
                            # src = "/home/v/viru/ImagesExtraction/" + imageFolderName + "/" + imgName
                            dst = "Irma/" + folderName
                            if not os.path.exists(dst):
                                os.makedirs(dst)
                            # copyfile(src, dst + "/" + imgName)
                            writer = csv.writer(open("Irma/"+folderName+".csv", "a"))
                            writer.writerow([str(tweetId)])

                        elif any(word in text for word in mariaKeywords):
                            # src = "/home/v/viru/ImagesExtraction/" + imageFolderName + "/" + imgName
                            dst = "Maria/" + folderName
                            if not os.path.exists(dst):
                                os.makedirs(dst)
                            # copyfile(src, dst + "/" + imgName)
                            writer = csv.writer(open("Maria/"+folderName+".csv", "a"))
                            writer.writerow([str(tweetId)])

                        else:
                            # src = "/home/v/viru/ImagesExtraction/" + imageFolderName + "/" + imgName
                            dst = "Ambiguous/" + folderName
                            if not os.path.exists(dst):
                                os.makedirs(dst)
                            # copyfile(src, dst + "/" + imgName)
                            writer = csv.writer(open("Ambiguous/"+folderName+".csv", "a"))
                            writer.writerow([str(tweetId)])

                    else:  # multiple match found
                        # src = "/home/v/viru/ImagesExtraction/" + imageFolderName + "/" + imgName
                        dst = "Ambiguous/" + folderName
                        if not os.path.exists(dst):
                            os.makedirs(dst)
                        # copyfile(src, dst + "/" + imgName)
                        writer = csv.writer(open("Ambiguous/"+folderName+".csv", "a"))
                        writer.writerow([str(tweetId)])

                    try:
                        copyfile(src, dst + "/" + imgName)
                    except FileNotFoundError:
                        try:
                            request.urlretrieve(photo, dst+"/"+photo.split('/')[-1])
                        except urllib.error.HTTPError as e:
                            pass
                        except:
                            print("Image could not be downloaded")
                    except:
                        raise Exception("something went wrong")

            data_file.close()






















