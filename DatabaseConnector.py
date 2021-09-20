from Database_Objects import regression
from Database_Objects.match import dotaMatch, matchAttributes
from Database_Objects.team import teamAttributes
from Database_Objects.league import league, leagueAttributes
from Database_Objects.player import player, playerAttributes
from Database_Objects.team import team, teamAttributes

from pymongo import MongoClient
import os
from enum import Enum

class DatabaseConnector():

    
    def __init__(self, mongoString):
        self.client = MongoClient(mongoString)
        self.db = self.client.Dota2ProMatches

    def getServerStatus(self):
        return(self.db.command("serverStatus"))

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
            elif( cName.value == "Regressions"):
                self.db.Regressions.insert_many(data)
            else:
                return False
            return True
        except Exception as e:
            print(e)
            return False

    # takes a query which is a dictionary using mongo syntax and a database Collection to look in
    def makeQuery(self, query, dbc):
        if(dbc == databaseCollections.LEAGUES):
            return self.db.Leagues.find(query)
        elif(dbc == databaseCollections.TEAMS):
            return self.db.Teams.find(query)
        elif(dbc == databaseCollections.PLAYERS):
            return self.db.Players.find(query)
        elif(dbc == databaseCollections.HEROES):
            return self.db.Heroes.find(query)
        elif(dbc == databaseCollections.MATCHES):
            return self.db.Matches.find(query)
        elif(dbc == databaseCollections.REGRESSIONS):
            return self.db.Regressions.find(query)


    def getDocumentsByAttribute(self, value, attribute):
        returnable = []
        if(attribute in leagueAttributes):
            results = self.db.Leagues.find({attribute.value: value})
            for iterable in results:
                returnable.append(league.from_dict(iterable))
        elif(attribute in playerAttributes):
            results = self.db.Players.find({attribute.value: value})
            for iterable in results:
                returnable.append(player.fromDict(iterable))
        elif(attribute in teamAttributes):
            results = self.db.Teams.find({attribute.value: value})
            for iterable in results:
                returnable.append(team.fromDict(iterable))
        elif(attribute in matchAttributes):
            results = self.db.Matches.find({attribute.value: value})
            for iterable in results:
                returnable.append(dotaMatch.fromDict(iterable))
        elif(attribute in regression.regressionAttributes):
            results = self.db.Regressions.find({attribute.value: value})
            for iterable in results:
                returnable.append(dotaMatch.fromDict(iterable))
        return returnable

class databaseCollections(Enum):
    PLAYERS = 'Players'
    MATCHES = 'Matches'
    TEAMS = 'Teams'
    LEAGUES = 'Leagues'
    HEROES = 'Heroes'
    REGRESSIONS = 'Regressions'


# client = MongoClient(os.environ['LOCALMONGOSTR'])
# db = client.Dota2ProMatches
# tbu = db.Matches.find({})
# for iter in tbu:
#     if(not iter['matchID'] > 0 ):
#         print(type(iter['matchID']))
#     # db.Matches.update_one(
#     #     {'_id': iter['_id']},
#     #     {"$set": {'matchID': iter['matchID'][0]}})
# client.close()