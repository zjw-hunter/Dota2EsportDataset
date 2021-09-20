import Database_Objects.league as league
import Database_Objects.match as dotaMatch
import Database_Objects.player as player
import Database_Objects.team as team
import Database_Objects.regression as regression
from DatabaseConnector import DatabaseConnector, databaseCollections
import os

class doStats():

    def __init__(self):
        self.dbc = DatabaseConnector(os.environ['LOCALMONGOSTR'])


    def getDependents(self):
        return list(self.dbc.makeQuery({league.leagueAttributes.LEAGUENAME.value: {'$regex': 'The International'}}, databaseCollections.LEAGUES))

    #How does a participant's 
    def avgLeagueResult(self):
        pass

    def avgRecentLeagueResult(self):
        pass

    def avgTIResult(self):
        pass

    def gamesPlayed(self):
        pass

    def gamesPlayedInCurrentRole(self):
        pass

    def gamesPlayedWithHero(self):
        pass

    def heroesPlayed(self):
        pass

    def tiParticipation(self):
        pass

    def placeStringToInt(self, placeString):
        return int(placeString[0:-2])