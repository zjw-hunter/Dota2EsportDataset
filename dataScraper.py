from DatabaseConnector import DatabaseConnector
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pprint as pp
import re
from datetime import date, datetime


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
            'teams': None
        }
        uClient = uReq(tourneyURL)
        tourneySoup = soup(uClient.read(), "html.parser")
        uClient.close()
        
        # tourneyID = tourneySoup.select('a.external.text i.lp-dotabuff')[0].parent.attrs['href'].split('/')[5]
        # tourneyName = tourneySoup.select('h1 span')[0].contents[0]
        # tourneyPrizePoolString = re.search(r'\$(\d|\,)+', str(tourneySoup.find('div', string="Prize Pool:").fetchNextSiblings()[0])).group(0)
        # tPP = int(tourneyPrizePoolString[1:].replace(',', ''))
        # dateArray = self.processDateStringArray(str(tourneySoup.find('div', string='Dates:').fetchNextSiblings()[0].contents[0]).replace(',', '').split(' '))
        teamList = []
        for team in tourneySoup.select('div.teamcard center b a'):
            playerList = []
            for player in team.findParent().findParent().findNextSibling().select('td a'):
                playerList.append({
                    "tag"
                })
            team = {
                'result': team.findParent().findParent().findNextSibling().select('td a'),
                'players': [],
                'org': team.contents[0]
            }
            teamList.append(team)

        return teamList

    #Returns [StartDate, EndDate] both are datetime.datetime objects
    def processDateStringArray(self, dsa):
        dateAbbrDict = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }
        #Same Year, Same Month
        if(len(dsa) == 5):
            startDate = datetime(int(dsa[4]), dateAbbrDict[dsa[0]], int(dsa[1]))
            endDate = datetime(int(dsa[4]), dateAbbrDict[dsa[0]], int(dsa[3]))
            return [startDate, endDate]
        #Same Year, Diff Month
        elif(len(dsa) == 6):
            startDate = datetime(int(dsa[5]), dateAbbrDict[dsa[0]], int(dsa[1]))
            endDate = datetime(int(dsa[5]), dateAbbrDict[dsa[3]], int(dsa[4]))
            return [startDate, endDate]
        #Diff Year
        elif(len(dsa) == 7):
            startDate = datetime(int(dsa[2]), dateAbbrDict[dsa[0]], int(dsa[1]))
            endDate = datetime(int(dsa[6]), dateAbbrDict[dsa[4]], int(dsa[5]))
            return[startDate, endDate]
        else:
            return False
    
    def getPlayer(self, playerUrl):
        player = {
            'tag': None,
            'name': None,
            'birthday': None,
            'playerID': None,
            'country': None
        }

        uClient = uReq(playerUrl)



        


        



myLink = 'https://liquipedia.net/dota2/ESL_One/Katowice/2018'
myLink2 = 'https://liquipedia.net/dota2/I-league/Season_2'
myLink3 = 'https://liquipedia.net/dota2/Nexon_Sponsorship_League/Season_2'
myDS = dataScraper()
pp.pprint(myDS.getTourneyDetails(myLink))

