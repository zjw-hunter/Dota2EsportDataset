from DatabaseConnector import DatabaseConnector, databaseCollections
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pprint as pp
import re
from datetime import datetime
from player import player, playerAttributes
from league import league
from team import team as teamObj

class dataScraper():

    dbc = DatabaseConnector()
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
            if(not 'style' in item.findNextSiblings()[0].attrs):
                returnList.append([item.select('b a')[0].contents[0], self.baseUrl + item.select('b a')[0].attrs['href']])
        return returnList
    
    def getTourneyDetails(self, tourneyURL):
        
        uClient = uReq(tourneyURL)
        tourneySoup = soup(uClient.read(), "html.parser")
        uClient.close()
        
        tourneyID = tourneySoup.select('a.external.text i.lp-dotabuff')[0].parent.attrs['href'].split('/')[5]
        tourneyName = tourneySoup.select('h1 span')[0].contents[0]
        tourneyPrizePoolString = re.search(r'\$(\d|\,)+', str(tourneySoup.find('div', string="Prize Pool:").fetchNextSiblings()[0])).group(0)
        tPP = int(tourneyPrizePoolString[1:].replace(',', ''))
        dateArray = self.processDateStringArray(str(tourneySoup.find('div', string='Dates:').fetchNextSiblings()[0].contents[0]).replace(',', '').split(' '))
        teamList = []
        placeOrder = []
        placeBuckets = {}


        for line in tourneySoup.select('table.prizepooltable span.team-template-text a'):
            placeOrder.append(line.contents[0])
        
        i = 0
        for bucket in tourneySoup.select('table.prizepooltable tr td b'):
            try: 
                bucketSize = int(bucket.parent.attrs['rowspan'])
                for team in placeOrder[i:i+bucketSize]:
                    placeBuckets[team] = bucket.contents[-1].split('-')[0]
                i+= bucketSize -1
            except: 
                placeBuckets[placeOrder[i]] = bucket.contents[-1].strip()
            i += 1
        
        for item in tourneySoup.select('div.teamcard center b a'):
            if( "<s>" not in str(item.contents[0])):
                playerList = []
                for lineItem in item.findParent().findParent().findNextSibling().select('tr'):
                    if(lineItem.find(string = re.compile(r'^([12345C])$'))):
                        playerList.append(
                            [ lineItem.find(string = re.compile(r'^([12345C])$')),
                               self.getPlayer( self.baseUrl + str(lineItem.contents[-1].contents[-1].attrs['href']))
                            ])
                teamList.append(teamObj(tourneyID, placeBuckets[item.contents[0]], item.contents[0], playerList).getMongoObj())
                

        return league(tourneyName, tourneyID, tPP, dateArray[0], dateArray[1], teamList, tourneyURL)

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
    #returns a player object scraped from the url provided
    def getPlayer(self, playerUrl):
        # try: 
        #     thePlayer = self.dbc.getDocumentByAttribute(playerUrl, playerAttributes.URL)
        # if( ):
        #     return 
        uClient = uReq(playerUrl)
        playerSoup = soup(uClient.read(), "html.parser")
        uClient.close()

        tag = playerSoup.select('h1 span')[0].contents[0]
        name = playerSoup.find_all("div", string=re.compile(r'.*Name:'))[-1].fetchNextSiblings()[0].contents[0]
        try:
            birthDay = datetime.strptime(playerSoup.find("div", string="Birth:").fetchNextSiblings()[0].contents[0], '%B %d, %Y')
        except:
            birthDay = None
        try:
            playerID = int(playerSoup.select('a.external.text i.lp-dotabuff')[0].parent.attrs['href'].split('/')[5])
        except:
            playerID = None
        country = []
        try:
            for flag in playerSoup.select('div.infobox-cell-2 span.flag a'):
                country.append(flag.attrs['title'])
        except:
            pass
        roles = []
        for role in playerSoup.find('div', string="Role(s):").fetchNextSiblings()[0].children:
            if( role.contents):
                roles.append(role.contents[0])

        returnable = player(tag, name, birthDay, playerID, country, roles, playerUrl)
        try:
            self.dbc.insertMany([returnable.getMongoObj()], databaseCollections.PLAYERS)
        except Exception as e:
            print(e)
        return returnable


        


        

myLink5 = 'https://liquipedia.net/dota2/Arteezy'
myLink4 = 'https://liquipedia.net/dota2/March_(Park_Tae-won)'
myLink = 'https://liquipedia.net/dota2/ESL_One/Katowice/2018'
myLink2 = 'https://liquipedia.net/dota2/I-league/Season_2'
myLink3 = 'https://liquipedia.net/dota2/Nexon_Sponsorship_League/Season_1'
myDS = dataScraper()
pp.pprint(myDS.getPlayer(myLink5))

