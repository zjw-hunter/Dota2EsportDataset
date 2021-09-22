from enum import Enum

class team():

    def __init__(self, leagueID, result, org, players, leagueName):
        self._leagueID = leagueID
        self._result = result
        self._org = org
        self._players = players
        self._leagueName = leagueName

    @classmethod
    def fromDict(cls, teamDict, altLN = ""):
        if( len(altLN) > 0):
            return cls(teamDict['leagueID'], teamDict['result'], teamDict['org'], teamDict['players'], altLN)
        return cls(teamDict['leagueID'], teamDict['result'], teamDict['org'], teamDict['players'], teamDict['leagueName'])
    
    def getMongoObj(self):
        return {
            "leagueID": self._leagueID,
            "result": self._result,
            "org": self._org,
            "players": self._players,
            "leagueName": self._leagueName
        }
        
class teamAttributes(Enum):
    LEAGUEID = 'leagueID'
    RESULT = 'result'
    ORG = 'org'
    PLAYERS = 'players'
    LEAGUENAME = 'leagueName'