from player import player
from datetime import datetime

class league():

    def __init__(self, name, leagueID, prizePool, startDate, endDate, teams):
        self._name = name
        self._leagueID = leagueID
        self._prizePool = prizePool
        self._startDate = startDate
        self._endDate = endDate
        self._teams = teams

    def getMongoObject(self):
        return {
            "name": self._name,
            "leagueID": self._leagueID,
            "prizePool": self._prizePool,
            "startDate": self._startDate,
            "endDate": self._endDate,
            "teams": self._teams
        }