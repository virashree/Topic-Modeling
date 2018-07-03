import csv
import ast
import shutil
import os

dir_name = "../ClassificationFiles/DisasterFiles_Classified_filtered/"
imag_dir_name = "../Twitter-Images/"
dir_des = "../ClassificationFiles/DisasterImages_filtered/"

if not os.path.exists(dir_des):
    os.makedirs(dir_des)

files_org = os.listdir(dir_name)
files_img = os.listdir(imag_dir_name)


def getList(string_list):
    if string_list != '[]':
        _list = ast.literal_eval(string_list)
        return _list
    else:
        return None


def getImages(media_url_https, media_type):
    imageLinks = getList(media_url_https)
    imageType = getList(media_type)
    images = []
    videos = []
    for link, type in zip(imageLinks, imageType):
        if type == 'photo':
            images.append(link)
        else:
            videos.append(link)
    return images, videos

for file in files_org:
    filename = str(os.path.basename(file).split('.')[0])
    path = dir_name + filename + ".csv"
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile) # x.replace('\0', '') for x in
        next(reader)
        for row in reader:
            if row[19] != '[]':
                mediaFiles = row[19]
                mediaFilesType = row[21]
                images, videos = getImages(mediaFiles, mediaFilesType)
                if not os.path.exists(dir_des + filename):
                    os.makedirs(dir_des + filename)
                for image in images:
                    imageName = image.split('/')[-1]
                    if imageName in files_img:
                        src = imag_dir_name + imageName
                        dst = dir_des + filename + "/" + imageName
                        shutil.copyfile(src, dst)
                        with open(dir_des + filename + "/" + filename + "_includedImages.csv", "a") as imageRecord:
                            writer = csv.writer(imageRecord)
                            writer.writerow([row[0], image, row[24]])
                    else:
                        with open(dir_des + filename + "/" + filename + "_excludedImages.csv", "a") as imageRecord:
                            writer = csv.writer(imageRecord)
                            writer.writerow([row[0], image, row[24]])

                for video in videos:
                    with open(dir_des + filename + "/" + filename + "_videos.csv", "a") as videoRecord:
                        writer = csv.writer(videoRecord)
                        writer.writerow([row[0], video, row[24]])









