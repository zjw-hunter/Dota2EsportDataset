from player import player
from datetime import datetime
from enum import Enum

class league():

    def __init__(self, leagueName, leagueID, prizePool, startDate, endDate, teams):
        self._leagueName = leagueName
        self._leagueID = leagueID
        self._prizePool = prizePool
        self._startDate = startDate
        self._endDate = endDate
        self._teams = teams

    def getMongoObject(self):
        return {
            "leagueName": self._leagueName,
            "leagueID": self._leagueID,
            "prizePool": self._prizePool,
            "startDate": self._startDate,
            "endDate": self._endDate,
            "teams": self._teams
        }

class leagueAttributes(Enum):
    LEAGUENAME = 'leagueName'
    LEAGUEID = 'leagueID'
    PRIZEPOOL = 'prizePool'
    STARTDATE = 'startDate'
    ENDDATE = 'endDate'
    TEAMS = 'teams'