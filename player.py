from datetime import datetime
from enum import Enum
from dateutil.relativedelta import relativedelta

class player():

    def __init__(self, tag, playerName, birthday, playerID, country, roles):
        self._tag = tag
        self._playerName = playerName
        self._birthday = birthday
        self._playerID = playerID
        self._country = country
        self._roles = roles

    def howOld(self, date):
        return relativedelta(date, self._birthday).years

    def getMongoObj(self):
        return {
            "tag": self._tag,
            "playerName": self._playerName,
            "birthday": self._birthday,
            "playerID": self._playerID,
            "country": self._country,
            "roles": self._roles
        }

class playerAttributes(Enum):
    TAG = 'tag'
    PLAYERNAME = 'playerName'
    BIRTHDAY = 'birthday'
    PLAYERID = 'playerID'
    COUNTRY = 'country'
    ROLES = 'roles'