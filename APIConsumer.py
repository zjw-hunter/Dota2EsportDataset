import requests
import time

class APIConsumer():

    rateLimit = 1250

    LiquipediaGetT1s = "https://liquipedia.net/dota2/api.php?action=askargs&format=json&conditions=Category%3ATier%201%20Tournaments&utf8=1"
    LiquipediaGetQs = "https://liquipedia.net/dota2/api.php?action=askargs&format=json&conditions=Category%3AQualifier%20Tournaments&utf8=1"
    LiquipediaGetArticleByTitle = "https://liquipedia.net/dota2/api.php?action=query&format=json&prop=cirrusdoc&list=&titles="
    LiquipediaSpace = "%20"
    LiquipediaSuffix = "&utf8=1"

    def __init__(self):
        pass

    def getRequest(self, url):
        try:
            time.sleep(self.rateLimit)
            response = requests.get(url)
            return(response)
        except Exception as e:
            print(e)
            return False