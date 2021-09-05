import requests
import time

class APIConsumer():

    # LiquipediaGetT1s = "https://liquipedia.net/dota2/api.php?action=askargs&format=json&conditions=category%3A%20Tier%201%20Tournaments&parameters=offset%3D"
    # LiquipediaGetQs = "https://liquipedia.net/dota2/api.php?action=askargs&format=json&conditions=category%3A%20Qualifier%20Tournaments&parameters=offset%3D"
    # LiquipediaGetArticleByTitle = "https://liquipedia.net/dota2/api.php?action=query&format=json&prop=cirrusdoc&list=&titles="
    # LiquipediaSpace = "%20"
    # LiquipediaSuffix = "&utf8=1"

    def __init__(self):
        pass

    # does a getRequest using the url provided and waiting the rateLimit (time in seconds)
    def getRequest(self, url, rateLimit):
        try:
            time.sleep(rateLimit)
            response = requests.get(url).json()
            return(response)
        except Exception as e:
            print(e)
            return False