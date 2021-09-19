from enum import Enum

class dotaMatch():
    def __init__(self, players, radiantWin, duration, matchID, leagueID):
        self.players = players
        self.radiantWin = radiantWin
        self.duration = duration
        self.matchID = matchID,
        self.leagueID = leagueID
    
    @classmethod
    def fromDict(cls, matchDict):
        return cls(matchDict['players'], matchDict['radiant_win'], matchDict['duration'], matchDict['match_id'], matchDict['leagueid'])
    
    def getMongoObj(self):
        return {
            "players": self.players,
            "radiantWin": self.radiantWin,
            "duration": self.duration,
            "matchID": self.matchID,
            "leagueID": self.leagueID
        }

class matchAttributes(Enum):
    PLAYERS = 'players'
    RADIANTWIN = 'radiantWin'
    DURATION = 'duration'
    MATCHID = 'matchID'
    LEAGUEID = 'leagueID'
