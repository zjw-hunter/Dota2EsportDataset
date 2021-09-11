from enum import Enum

class team():

    def __init__(self, leagueID, result, org, players):
        self._leagueID = leagueID
        self._result = result
        self._org = org
        self._players = players

    @classmethod
    def fromDict(cls, teamDict):
        return cls(teamDict['leagueID'], teamDict['result'], teamDict['org'], teamDict['players'])
    
    def getMongoObj(self):
        return {
            "leagueID": self._leagueID,
            "result": self._result,
            "org": self._org,
            "players": self._players
        }
        
class teamAttributes(Enum):
    LEAGUEID = 'leagueID'
    RESULT = 'result'
    ORG = 'org'
    PLAYERS = 'players'