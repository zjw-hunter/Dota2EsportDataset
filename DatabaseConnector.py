from team import teamAttributes
from pymongo import MongoClient
from pprint import pprint

from league import league, leagueAttributes
from player import player, playerAttributes
from team import team, teamAttributes

from enum import Enum

class DatabaseConnector():

    DOTA_COLLECTIONS = ["Players", "Matches", "Teams", "Leagues", "Heroes"]
    client = MongoClient("mongodb://localhost:27017")
    db = client.Dota2ProMatches
    def __init__(self):
        pass

    def getServerStatus(self):
        return(self.db.command("serverStatus"))

    def getCollections(self):
        return(self.DOTA_COLLECTIONS)

    # obj is the data, cName is the collection to add the document to.
    # true if operation worked, otherwise false
    def insertMany(self, data, cName):
        if(cName not in databaseCollections):
            return False
        if(data is None):
            return False
        try:
            if( cName.value == "Players"):
                self.db.Players.insert_many(data)
            elif( cName.value == "Matches"):
                self.db.Matches.insert_many(data)
            elif( cName.value == "Teams"):
                self.db.Teams.insert_many(data)
            elif( cName.value == "Leagues"):
                self.db.Leagues.insert_many(data)
            else:
                return False
            return True
        except Exception as e:
            print(e)
            return False
    
    def getDocumentByAttribute(self, value, attribute):
        if(attribute in leagueAttributes):
            return 1
        elif(attribute in playerAttributes):
            return 2
        elif(attribute in teamAttributes):
            return 3
        return False

class databaseCollections(Enum):
    PLAYERS = 'Players'
    MATCHES = 'Matches'
    TEAMS = 'Teams'
    LEAGUES = 'Leagues'
    HEROES = 'Heroes'