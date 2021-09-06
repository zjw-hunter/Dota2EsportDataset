from DatabaseConnector import DatabaseConnector
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pprint as pp

class dataScraper():

    baseUrl = 'https://liquipedia.net'
    tourneyListUrl = 'https://liquipedia.net/dota2/Tier_1_Tournaments'
    def __init__(self):
        pass

    def getTourneyList(self):
        returnList = []

        uClient = uReq(self.tourneyListUrl)
        tourneyListSoup = soup(uClient.read(), "html.parser")
        uClient.close()
        soupList = tourneyListSoup.select('div.Tournament.Header')
        for item in soupList:
            returnList.append([item.select('b a')[0].contents[0], self.baseUrl + item.select('b a')[0].attrs['href']])
        return returnList
    
    def getTourneyDetails(self, tourneyURL):
        returnObj = {
            'name': None,
            'id': None,
            'prizePool': None,
            'startDate': None,
            'endDate': None,
            'version': None,
            'teams': None
        }
        return None


myDS = dataScraper()
pp.pprint(myDS.getTourneyList())

