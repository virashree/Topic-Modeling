import time
from enum import Enum
import os
import ast
import csv
from termcolor import colored


irmaKeywords = ["miami", "florida", "orlando", "irma", "florida keys island", "floridakeysisland", "barbuda", "cuba", "caribbean", "keysisland",
                "keys island", "haiti", "turks", "caicos", "st. barts", "st. martin", "saint barts", "saint martin", "stbarts", "stmartin",
                "edenrock", "cape verde", "leeward island", "caicos",  "caicos island", "bahamas", "greater antilles", "anguilla",
                "virgin island", "saint barthelemy"]

harveyKeywords = ["harvey", "houston", "houstonfloods", "hurricaneharveyrelief", "corpuschristi", "corpus christi", "beaumont", "texas", "#tx"
                  "windward island", "windward","suriname", "guyana", "nicaragua", "honduras","belize","cayman island",
                  "yucatán peninsula", "yucatán", "peninsula", "yucatan"]

mariaKeywords = ["maria", "puerto rico", "puertorico","san juan","sanjuan","hurricanemaria","hurricane maria", "puerto","virgin island"
                 "dominica", "guadeloupe", "u.s. virgin islands","u.s. virgin island","dominican", "haiti", "bahamas", "turks", "caicos island",
                 "caicos", "lesser antilles"]

mexicoEarthQuakeKeywords = ["mexico city", "earthquake", "mexicocity", "mexicocityearthquake", "mexico"]

chiapasEarthQuakeKeywords = ["mexico city", "earthquake", "mexicocity", "mexicocityearthquake", "mexico", "chaipas", "guatemala",
                            "chiapas", "mexico city", "tusnami"]


# Hurricane Harvey timeline
# T.S. Forms August 17, Thu Aug 17 2017 4:00 PM AST, Thu Aug 17 2017 04:00 PM UTC
# Final Advisory August 30, Wed Aug 30 2017 10:00 PM CDT, Wed Aug 30 2017 03:00 AM UTC
# Major impact: August 25 - August 29
# Major Areas Affected in usa:	Texas and Louisiana mainly Corpus Christi, Beaumont, Houston
# Other Areas: Windward Islands, Suriname, Guyana, Nicaragua, Honduras, Belize,
# Cayman Islands, Yucatán Peninsula

# Hurricane Irma timeline
# T.S. Forms: August 30, Wed Aug 30 2017 11:00 AM AST, Wed Aug 30 2017 03:00 PM UTC
# Final Advisory September 12, Tue Sep 12 2017 5:00 PM EDT, Tue Sep 12 2017 9:00 PM UTC
# Major impact in usa: September 10 - september 11
# Major impact overall: September 6 - September 11
# Major areas affected in usa: florida
# other areas: Cape Verde, Leeward Islands / Caribbean island chain
# (especially Barbuda, Saint Barthelemy, Anguilla, Saint Martin and the Virgin Islands),
# Greater Antilles (Cuba and Puerto Rico), Turks and Caicos Islands, The Bahamas,
# Eastern United States (especially Florida)

# Hurricane Maria
# T.S. Forms: September 16, Sat Sep 16 2017 2:00 PM AST, Sat Sep 16 2017 6:00 PM UTC
# Final Advisory: September 30, Sat Sep 30 2017 5:00 PM AST, Sat Sep 30 2017 9:00 PM UTC
# Major impact: september 18 - September 23
# Major areas affected in usa: Puerto Rico
# other areas: Lesser Antilles (especially Dominica, Guadeloupe, and the U.S. Virgin Islands),
# Puerto Rico, Dominican Republic, Haiti, Turks and Caicos Islands, The Bahamas,
# Southeastern United States, Mid-Atlantic States, Ireland, United Kingdom, France, Spain

# Mexico Earthquake
# Date: September 19
# place: Mexico city
# time: Tue Sept 19 2017 18:14:39 UTC , 12:14 pm

# chiapas Earthquake
# Date: September 7
# place: Mexico, Guatemala, chiapas, mexico city, tusnami
# time: 23:49:21 CDT, Fri Sep 2017 8 4:49 AM UTC

# print(time.strftime('%Y-%m-%d %H:%M:%S', time.strptime('Wed Oct 04 15:48:30 +0000 2017', '%a %b %d %H:%M:%S +0000 %Y')))
# x = time.strptime('Wed Oct 04 15:48:30 +0000 2017', '%a %b %d %H:%M:%S +0000 %Y')
#  y = time.strptime('Thu Aug 17 2017 8:00 +0000 PM', '%a %b %d %Y %I:%M +0000 %p')


class TweetText(Enum):
    MARIA_RELEVANT = 1
    MARIA_IRRELEVANT = 2
    IRMA_RELEVANT = 3
    IRMA_IRRELEVANT = 4
    HARVEY_RELEVANT = 5
    HARVEY_IRRELEVANT = 6
    MEXICO_RELEVANT = 7
    MEXICO_IRRELEVANT = 8
    CHIAPAS_RELEVANT = 9
    CHIAPAS_IRRELEVANT = 10


class Classifier:

    def __init__(self, tweet_time, tweet_text, tweet_hashtags):
        self.mariaStartTime = time.strptime('Sat Sep 16 2017 06:00 +0000 PM', '%a %b %d %Y %I:%M +0000 %p')
        self.mariaEndTime = time.strptime('Sat Sep 30 2017 09:00 +0000 PM', '%a %b %d %Y %I:%M +0000 %p')
        self.irmaStartTime = time.strptime('Wed Aug 30 2017 03:00 +0000 PM', '%a %b %d %Y %I:%M +0000 %p')
        self.irmaEndTime = time.strptime('Tue Sep 12 2017 09:00 +0000 PM', '%a %b %d %Y %I:%M +0000 %p')
        self.harveyStartTime = time.strptime('Thu Aug 17 2017 04:00 +0000 PM', '%a %b %d %Y %I:%M +0000 %p')
        self.harveyEndTime = time.strptime('Wed Aug 30 2017 03:00 +0000 AM', '%a %b %d %Y %I:%M +0000 %p')
        # self.mexicoEarthquake = time.strptime('Tue Sep 19 18:14:39 +0000 2017', '%a %b %d %H:%M:%S +0000 %Y')
        self.mexicoEarthquake = time.strptime('Tue Sep 19 00:00:00 +0000 2017', '%a %b %d %H:%M:%S +0000 %Y')
        self.chiapasEarthquake = time.strptime('Fri Sep 8 4:49:21 +0000 2017 AM', '%a %b %d %H:%M:%S +0000 %Y %p')
        self.tweet_time = time.strptime(tweet_time, '%a %b %d %H:%M:%S +0000 %Y')
        self.tweet_text = tweet_text.rstrip().lower()
        self.tweet_hashtags = self.getHashtags(tweet_hashtags)

    def isMaria(self):
        if self.tweet_time >= self.mariaStartTime:
            # tweeted during or after maria hurricane
            try:
                if self.tweet_hashtags and self.tweet_hashtags is not None:
                    for hashtag in self.tweet_hashtags:
                        if 'maria' in hashtag:
                            return TweetText.MARIA_RELEVANT
                if 'maria' in self.tweet_text:
                    return TweetText.MARIA_RELEVANT
                if self.tweet_hashtags and self.tweet_hashtags is not None:
                    # check if any keyword is in hashtag
                    for s in mariaKeywords:
                        if any(s in hashtag for hashtag in self.tweet_hashtags):
                            return TweetText.MARIA_RELEVANT
                if any(word in self.tweet_text for word in mariaKeywords):
                    return TweetText.MARIA_RELEVANT
                return TweetText.MARIA_IRRELEVANT
            except Exception as e:
                print(e)
        else:
            return TweetText.MARIA_IRRELEVANT

    def isHarvey(self):
        if self.tweet_time >= self.harveyStartTime:
            # tweeted during or after harvey hurricane
            try:
                if self.tweet_hashtags and self.tweet_hashtags is not None:
                    for hashtag in self.tweet_hashtags:
                        if 'harvey' in hashtag:
                            return TweetText.HARVEY_RELEVANT
                if 'harvey' in self.tweet_text:
                    return TweetText.HARVEY_RELEVANT
                if self.tweet_hashtags and self.tweet_hashtags is not None:
                    for s in harveyKeywords:
                        if any(s in hashtag for hashtag in self.tweet_hashtags):
                            return TweetText.HARVEY_RELEVANT
                if any(word in self.tweet_text for word in harveyKeywords):
                    return TweetText.HARVEY_RELEVANT
                return TweetText.HARVEY_IRRELEVANT
            except Exception as e:
                print(e)
        else:
            return TweetText.HARVEY_IRRELEVANT

    def isIrma(self):
        if self.tweet_time >= self.irmaStartTime:
            # tweeted during or after irma hurricane
            try:
                if self.tweet_hashtags and self.tweet_hashtags is not None:
                    for hashtag in self.tweet_hashtags:
                        if 'irma' in hashtag:
                            return TweetText.IRMA_RELEVANT
                if 'irma' in self.tweet_text:
                    return TweetText.IRMA_RELEVANT
                if self.tweet_hashtags and self.tweet_hashtags is not None:
                    for s in irmaKeywords:
                        if any(s in hashtag for hashtag in self.tweet_hashtags):
                            return TweetText.IRMA_RELEVANT
                if any(word in self.tweet_text for word in irmaKeywords):
                    return TweetText.IRMA_RELEVANT
                return TweetText.IRMA_IRRELEVANT
            except Exception as e:
                print(e)
        else:
            return TweetText.IRMA_IRRELEVANT

    def getHashtags(self, tweet_hashtags):
        if tweet_hashtags != '[]':
            tweet_hashtags = ast.literal_eval(tweet_hashtags)
            if tweet_hashtags:
                hashtags = []
                for item in tweet_hashtags:
                    hashtags.append(item['text'].lower())
                return hashtags
        else:
            return None

    def isMexicoEarthquake(self):
       if self.tweet_time >= self.mexicoEarthquake:
           try:
               if self.tweet_hashtags and self.tweet_hashtags is not None:
                   for hashtag in self.tweet_hashtags:
                       if 'mexicoearthquake' in hashtag or 'mexicocityearthquake' in hashtag \
                               or 'mexico' in hashtag or 'earthquake' in hashtag:
                           return TweetText.MEXICO_RELEVANT
               if 'mexico' in self.tweet_text and 'earthquake' in self.tweet_text:
                   return TweetText.MEXICO_RELEVANT
               if self.tweet_hashtags and self.tweet_hashtags is not None:
                   for s in mexicoEarthQuakeKeywords:
                       if any(s in hashtag for hashtag in self.tweet_hashtags):
                           return TweetText.MEXICO_RELEVANT
               if any(word in self.tweet_text for word in mexicoEarthQuakeKeywords):
                   return TweetText.MEXICO_RELEVANT
               return TweetText.MEXICO_IRRELEVANT
           except Exception as e:
               print(e)
       else:
           return TweetText.MEXICO_IRRELEVANT

    def isChiapasEarthquake(self):
        if self.tweet_time >= self.chiapasEarthquake: #and self.tweet_time < time.strptime('Tue Sep 19 00:00:00 +0000 2017', '%a %b %d %H:%M:%S +0000 %Y'):
            try:
                if self.tweet_hashtags and self.tweet_hashtags is not None:
                    for hashtag in self.tweet_hashtags:
                        if 'earthquake' in hashtag or 'mexico' in hashtag or 'tsunami' in hashtag or \
                                        'mexicoearthquake' in hashtag or 'chiapas' in hashtag:
                            return TweetText.CHIAPAS_RELEVANT
                if 'earthquake' in self.tweet_text or 'mexico' in self.tweet_text or 'tsunami' in self.tweet_text or \
                                'mexicoearthquake' in self.tweet_text or 'chiapas' in self.tweet_text:
                    return TweetText.CHIAPAS_RELEVANT
                if self.tweet_hashtags and self.tweet_hashtags is not None:
                    for s in chiapasEarthQuakeKeywords:
                        if any(s in hashtag for hashtag in self.tweet_hashtags):
                            return TweetText.CHIAPAS_RELEVANT
                if any(word in self.tweet_text for word in chiapasEarthQuakeKeywords):
                    return TweetText.CHIAPAS_RELEVANT
                return TweetText.CHIAPAS_IRRELEVANT
            except Exception as e:
                print(e)
        else:
            return TweetText.CHIAPAS_IRRELEVANT

    def mostRelevent(self):
        if self.tweet_time < self.mariaStartTime:
            # does not belong to maria, belongs to irma
            return TweetText.IRMA_RELEVANT
        elif self.tweet_time >= self.mariaStartTime:
            # belongs to maria
            return TweetText.MARIA_RELEVANT

if __name__ == '__main__':

    paths = ["Harvey.csv", "Irma.csv","Maria.csv","MexicoEarthquake.csv","Chiapas.csv",
             "HarveyIrma.csv", "MexicoIrma.csv","MexicoHarvey.csv","MexicoMaria.csv", "HarveyMaria.csv", "IrmaMaria.csv",

             "MariaIrmaHarvey.csv", "MariaIrmaHarveyMexico.csv"]

# "ChiapasHarvey.csv", "ChiapasIrma.csv", "ChiapasIrmaHarvey.csv",
    # df = pd.read_csv('hurricane_maria_twitter_1.csv',  encoding="ISO-8859-1")

    tweet_ids = {}

    Dir = "Classified"
    if not os.path.exists(Dir):
        os.makedirs(Dir)

    newDir = "Classified/Irma_duplicate"
    if not os.path.exists(newDir):
        os.makedirs(newDir)

    #for path in paths:
        #if not os.path.exists("Classified/"+path):
         #   open("Classified/"+path)

    w1 = csv.writer(open('Classified/Irma_duplicate/Harvey.csv', 'a'))
    w2 = csv.writer(open('Classified/Irma_duplicate/Maria.csv','a'))
    w3 = csv.writer(open('Classified/Irma_duplicate/Irma.csv', 'a'))
    w4 = csv.writer(open('Classified/Irma_duplicate/MexicoEarthquake.csv','a'))

    w5 = csv.writer(open('Classified/Irma_duplicate/HarveyIrma.csv', 'a'))
    w6 = csv.writer(open('Classified/Irma_duplicate/HarveyMaria.csv','a'))
    w7 = csv.writer(open('Classified/Irma_duplicate/IrmaMaria.csv','a'))

    w8 = csv.writer(open('Classified/Irma_duplicate/MariaIrmaHarvey.csv','a'))

    w9 = csv.writer(open('Classified/Irma_duplicate/MexicoIrma.csv','a'))
    w10 = csv.writer(open('Classified/Irma_duplicate/MexicoHarvey.csv','a'))
    w11 = csv.writer(open('Classified/Irma_duplicate/MexicoMaria.csv','a'))

    w12 = csv.writer(open('Classified/Irma_duplicate/MariaIrmaHarveyMexico.csv','a'))
    
    w13 = csv.writer(open('Classified/Irma_duplicate/Chiapas.csv','a'))

    w14 = csv.writer(open('Classified/Irma_duplicate/ChiapasHarvey.csv','a'))
    w15 = csv.writer(open('Classified/Irma_duplicate/ChiapasIrma.csv','a'))

    w16 = csv.writer(open('Classified/Irma_duplicate/ChiapasIrmaHarvey.csv','a'))


    # cnt = 0
    # for index, row in df.iterrows():
    try:
        with open('Duplicates/Irma_duplicate.csv', 'r') as csvfile:
            reader = csv.reader(x.replace('\0', '') for x in csvfile)
            next(reader)
            for row in reader:

                # if retweet status id

                id = int(row[22]) if row[22] != ' ' or '' or None else int(row[3])

                try:
                    if id in tweet_ids:
                        print("already in")
                    else:
                        tweet_ids[id] = ''
                        tweet_time = row[2] if row[2] != '' or ' ' else row[1]
                        classifier = Classifier(row[1], row[4], row[17])
                        isHarvey = classifier.isHarvey()
                        isIrma = classifier.isIrma()
                        isMaria = classifier.isMaria()
                        isMexico = classifier.isMexicoEarthquake()
                        isChiapas = classifier.isChiapasEarthquake()

                        print(row)
                        if isHarvey == TweetText.HARVEY_RELEVANT and isIrma == TweetText.IRMA_RELEVANT and isMaria == TweetText.MARIA_RELEVANT and isMexico == TweetText.MEXICO_IRRELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # MariaIrmaHarvey.csv
                            w8.writerow(row)
                        elif isHarvey == TweetText.HARVEY_RELEVANT and isIrma == TweetText.IRMA_RELEVANT and isMaria == TweetText.MARIA_RELEVANT and isMexico == TweetText.MEXICO_RELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # MariaIrmaHarveyMexico.csv
                            w12.writerow(row)
                        elif isHarvey == TweetText.HARVEY_RELEVANT and isIrma == TweetText.IRMA_RELEVANT and isMaria == TweetText.MARIA_IRRELEVANT and isMexico == TweetText.MEXICO_IRRELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # HarveyIrma.csv
                            w5.writerow(row)
                        elif isIrma == TweetText.IRMA_RELEVANT and isMaria == TweetText.MARIA_RELEVANT and isHarvey == TweetText.HARVEY_IRRELEVANT and isMexico == TweetText.MEXICO_IRRELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # IrmaMaria.csv
                            w7.writerow(row)
                        elif isHarvey == TweetText.HARVEY_RELEVANT and isMaria == TweetText.MARIA_RELEVANT and isIrma == TweetText.IRMA_IRRELEVANT and isMexico == TweetText.MEXICO_IRRELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # HarveyMaria.csv
                            w6.writerow(row)
                        elif isHarvey == TweetText.HARVEY_RELEVANT and isMaria == TweetText.MARIA_IRRELEVANT and isIrma == TweetText.IRMA_IRRELEVANT and isMexico == TweetText.MEXICO_RELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # MexicoHarvey.csv
                            w10.writerow(row)
                        elif isHarvey == TweetText.HARVEY_IRRELEVANT and isMaria == TweetText.MARIA_RELEVANT and isIrma == TweetText.IRMA_IRRELEVANT and isMexico == TweetText.MEXICO_RELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # MexicoMaria.csv
                            w11.writerow(row)
                        elif isHarvey == TweetText.HARVEY_IRRELEVANT and isMaria == TweetText.MARIA_IRRELEVANT and isIrma == TweetText.IRMA_RELEVANT and isMexico == TweetText.MEXICO_RELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # IrmaMexico.csv
                            w9.writerow(row)
                        elif isHarvey == TweetText.HARVEY_RELEVANT and isIrma == TweetText.IRMA_IRRELEVANT and isMaria == TweetText.MARIA_IRRELEVANT and isMexico == TweetText.MEXICO_IRRELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT :
                            # Harvey.csv
                            w1.writerow(row)
                        elif isHarvey == TweetText.HARVEY_IRRELEVANT and isIrma == TweetText.IRMA_RELEVANT  and isMaria == TweetText.MARIA_IRRELEVANT and isMexico == TweetText.MEXICO_IRRELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # Irma.csv
                            w3.writerow(row)
                        elif isHarvey == TweetText.HARVEY_IRRELEVANT and isIrma == TweetText.IRMA_IRRELEVANT and isMaria == TweetText.MARIA_RELEVANT and isMexico == TweetText.MEXICO_IRRELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # Maria.csv
                            w2.writerow(row)
                        elif isMexico == TweetText.MEXICO_RELEVANT and isHarvey == TweetText.HARVEY_IRRELEVANT and isIrma == TweetText.IRMA_IRRELEVANT and isMaria == TweetText.MARIA_IRRELEVANT and isChiapas == TweetText.CHIAPAS_IRRELEVANT:
                            # MexicoEarthquake.csv
                            w4.writerow(row)
                        # elif classifier.mostRelevent() == TweetText.MARIA_RELEVANT:
                        #     # Maria.csv
                        #     w2.writerow(row)
                        elif isHarvey == TweetText.HARVEY_RELEVANT and isIrma == TweetText.IRMA_RELEVANT and isChiapas == TweetText.CHIAPAS_RELEVANT:
                            # HarveyIrmaChiapas.csv
                            w16.writerow(row)
                        elif isHarvey == TweetText.HARVEY_IRRELEVANT and isIrma == TweetText.IRMA_IRRELEVANT and isChiapas == TweetText.CHIAPAS_RELEVANT:
                            # Chiapas.csv
                            w13.writerow(row)
                        elif isHarvey == TweetText.HARVEY_RELEVANT and isChiapas == TweetText.CHIAPAS_RELEVANT and isIrma == TweetText.IRMA_IRRELEVANT:
                            # HarveyChiapas.csv
                            w14.writerow(row)
                        elif isHarvey == TweetText.HARVEY_IRRELEVANT and isChiapas == TweetText.CHIAPAS_RELEVANT and isIrma == TweetText.IRMA_RELEVANT:
                            # IrmaChiapas.csv
                            w15.writerow(row)
                        else:
                            # Chiapas.csv
                            w3.writerow(row)
                except Exception as ex:
                    print(colored(ex,'red'))
    except Exception as e:
        # print(row)
        print(colored(e, 'green'))

















