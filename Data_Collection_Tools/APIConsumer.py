from DatabaseConnector import DatabaseConnector, databaseCollections
import datetime
import requests
import os
import time

from Database_Objects.match import dotaMatch
from Database_Objects.league import league

class APIConsumer():

    #We are using the valve api to get matches, to avoid issues I'm setting a 250ms rate limit
    valveRateLimit = 0.25
    valveMatchesAPI = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1'
    valveMatchAPI = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1'

    def __init__(self):
        self.dbc = DatabaseConnector(os.environ['LOCALMONGOSTR'])

    # does a getRequest using the url provided and waiting the rateLimit (time in seconds)
    def getRequest(self, url, rateLimit,):
        try:
            time.sleep(rateLimit)
            response = requests.get(url).json()
            return(response)
        except Exception as e:
            print(e)
            return False
    #gets all the matches from a given league that start after a given date leagueID is a string, startDate is a datetime.datetime object. Returns a list of match IDs
    def getMatchList(self, leagueID, startDate, endDate):
        matchList = [] #we will return this
        try:
            #the parameters for this api 
            myParams = {
                'key': os.environ.get('STEAM_API_KEY'),
                'LEAGUE_ID': leagueID,
                }
            #rate Limit + request
            time.sleep(self.valveRateLimit)
            resp = requests.get(self.valveMatchesAPI, params=myParams).json()
            #iterate through original results
            for matchObj in resp['result']['matches']:
                if(matchObj['start_time'] < (endDate + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)).timestamp() and matchObj['start_time'] > startDate.timestamp()):
                    matchList.append(matchObj['match_id'])
                # if we hit qualifier matches we can safely return the 
                elif(matchObj['start_time'] < startDate.timestamp()):
                    return matchList
            #another try block in case there is no 'results_remaining' attribute (then we just continue)
            try:
                moreResponses = resp['results_remaining']
                while(moreResponses > 0):
                    myParams['start_at_match_id'] = matchList[-1] - 1 
                    time.sleep(self.valveRateLimit)
                    nextPage = requests.get(self.valveMatchesAPI, params=myParams).json()
                    for matchObj in nextPage['result']['matches']:
                        if(matchObj['start_time'] < (endDate + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)).timestamp() and matchObj['start_time'] > startDate.timestamp()):
                            matchList.append(matchObj['match_id'])
                        elif(matchObj['start_time'] < startDate.timestamp()):
                            return matchList 
                    moreResponses = nextPage['results_remaining']
                    pass
            except:
                pass
            return matchList
        except Exception as e:
            print(e)
        
    def getMatch(self, matchID):
        try:
            #parameters for the request
            myParams = {
                'key': os.environ['STEAM_API_KEY'],
                'match_id': matchID
            }
            #rate
            time.sleep(self.valveRateLimit)
            resp = requests.get(self.valveMatchAPI, params=myParams).json()['result']
            return dotaMatch.fromDict(resp)
        except Exception as e:
            print(e)

    #do the full consume and database insertion, leagues is a list of league objects
    def fullConsume(self, leagues):
        toBeInserted = []
        for league in leagues:
            for matchID in self.getMatchList(league._leagueID, league._startDate, league._endDate):
                toBeInserted.append(self.getMatch(matchID).getMongoObj())
                print('Inserted match: ' + str(matchID))
        self.dbc.insertMany(toBeInserted, databaseCollections.MATCHES)


myAPIC = APIConsumer()

# matches = myAPIC.getMatchList("9633", datetime.datetime.fromtimestamp(1519102800), datetime.datetime.fromtimestamp(1519534800))
# pprint.pprint(matches)
# pprint.pprint(len(matches))

# myMatch = myAPIC.getMatch(3752505318)
# pprint.pprint(myMatch.players)
myDBC = DatabaseConnector(os.environ['LOCALMONGOSTR'])
leagueList = []
for item in myDBC.makeQuery({}, databaseCollections.LEAGUES):
    leagueList.append(league.league.from_dict(item))

myAPIC.fullConsume(leagueList)