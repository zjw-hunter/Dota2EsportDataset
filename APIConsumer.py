import requests




class APIConsumer():

    LiquipediaBaseURL = "https://liquipedia.net/dota2/api.php?action=askargs&format=json&conditions=Category%3ATier%201%20Tournaments&utf8=1"


    def __init__(self):
        pass

    def getTournaments(self):
        try:
            response = requests.get(self.LiquipediaBaseURL)

        except Exception as e: print(e)