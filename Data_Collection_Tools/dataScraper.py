from DatabaseConnector import DatabaseConnector, databaseCollections
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pprint as pp
import re
import os
from datetime import datetime

from Database_Objects.player import player, playerAttributes
from Database_Objects.league import league, leagueAttributes
from Database_Objects.team import team as teamObj
import traceback

class dataScraper():

    dbc = DatabaseConnector(os.environ['LOCALMONGOSTR'])
    baseUrl = 'https://liquipedia.net'
    tourneyListUrl = 'https://liquipedia.net/dota2/Tier_1_Tournaments'
    def __init__(self):
        pass

    #Gathers the list of t1 tournaments from liquipedia
    def getTourneyList(self):
        returnList = []

        uClient = uReq(self.tourneyListUrl)
        tourneyListSoup = soup(uClient.read(), "html.parser")
        uClient.close()
        soupList = tourneyListSoup.select('div.Tournament.Header')
        for item in soupList:
            if(not 'style' in item.findNextSiblings()[0].attrs):
                returnList.append( self.baseUrl + item.select('b a')[0].attrs['href'])
        return returnList

    #Accepts the URL for the tournament returns a league object
    def getTourneyDetails(self, tourneyURL):
        try: 
            return self.dbc.getDocumentsByAttribute(tourneyURL, leagueAttributes.URL)[0]
        except Exception as e:
            print(traceback.format_exc())
        
        #Get the soup
        uClient = uReq(tourneyURL)
        tourneySoup = soup(uClient.read(), "html.parser")
        uClient.close()
        
        #Gather basic items
        try:
            tourneyID = tourneySoup.select('a.external.text i.lp-dotabuff')[0].parent.attrs['href'].split('/')[5]
        except: 
            tourneyID = None
        tourneyName = tourneySoup.select('h1 span')[0].contents[0]
        tourneyPrizePoolString = re.search(r'\$(\d|\,)+', str(tourneySoup.find('div', string="Prize Pool:").fetchNextSiblings()[0])).group(0)
        tPP = int(tourneyPrizePoolString[1:].replace(',', ''))
        dateArray = self.processDateStringArray(str(tourneySoup.find('div', string='Dates:').fetchNextSiblings()[0].contents[0]).replace(',', '').split(' '))
        
        #Gather Results
        placeOrder = []
        placeBuckets = {}
        for line in tourneySoup.select('table.prizepooltable span.team-template-text a'):
            placeOrder.append(line.contents[0].lower())
        i = 0
        for bucket in tourneySoup.select('table.prizepooltable tr td b'):
            try: 
                bucketSize = int(bucket.parent.attrs['rowspan'])
                for team in placeOrder[i:i+bucketSize]:
                    placeBuckets[team] = bucket.contents[-1].split('-')[0]
                i+= bucketSize -1
            except: 
                try:
                    placeBuckets[placeOrder[i]] = bucket.contents[-1].strip()
                except:
                    print(traceback.format_exc())
                    #This covers the 'mvp' section of the prizepool 
                    if( "</" in str(bucket.contents[0])): 
                        print('here')
                        pass
                    else:
                        return False
            i += 1
        if len(placeBuckets) == 0:
            return False
        #gather players into a team
        teamList = []
        for item in tourneySoup.select('div.teamcard center b a'):
            if( "<s>" not in str(item.contents[0])):
                playerList = []
                for lineItem in item.findParent().findParent().findNextSibling().select('tr'):
                    if(lineItem.find(string = re.compile(r'^([12345C])$'))):
                        try:
                            playerList.append(
                                {
                                    'role': lineItem.find(string = re.compile(r'^([12345C])$')),
                                    'player': self.getPlayer( self.baseUrl + str(lineItem.contents[-1].contents[-1].attrs['href'])).getMongoObj()
                                })
                        except:
                            pass
                try:
                    foundTeam = teamObj(tourneyID, placeBuckets[item.contents[0].lower()], item.contents[0], playerList).getMongoObj()
                    teamList.append(foundTeam)

                except Exception as e:
                    pass
                    # print(item.contents[0])
                    # print(placeBuckets)
                    # print(traceback.format_exc())
        #Gather the returnable
        returnable = league(tourneyName, tourneyID, tPP, dateArray[0], dateArray[1], teamList, tourneyURL)
        #Insert into database
        try:
            self.dbc.insertMany(teamList, databaseCollections.TEAMS)
            pp.pprint("Inserted " + str(len(teamList)) + " teams")
            self.dbc.insertMany([returnable.getMongoObj()], databaseCollections.LEAGUES)
            pp.pprint("Inserted " + returnable._leagueName)
        except Exception as e:
            print(traceback.format_exc())
        #Done    
        return returnable
        

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
        try: 
            return self.dbc.getDocumentsByAttribute(playerUrl, playerAttributes.URL)[0]
        except:
            pass
        if( 'php' in playerUrl):
            return None
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
            # pp.pprint("Inserted player: " + returnable._tag)
        except Exception as e:
            pass
        return returnable
    #Do the whole thing
    def fullScrape(self):
            for tourneyURL in self.getTourneyList():
                    self.getTourneyDetails(tourneyURL)
    
    def whatsIn(self):
        inDB = list(self.dbc.makeQuery({}, databaseCollections.LEAGUES))
        fullList = self.getTourneyList()
        for item in inDB:
            fullList.remove(item['url'])
        return fullList    

myScraper = dataScraper()
# to Run the script uncomment the following line and run dataScraper.py in the command line.
# myScraper.fullScrape()