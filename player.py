from datetime import datetime
from dateutil.relativedelta import relativedelta

class player():

    def __init__(self, tag, name, birthday, playerID, country, roles):
        self._tag = tag
        self._name = name
        self._birthday = birthday
        self._playerID = playerID
        self._country = country
        self._roles = roles

    def howOld(self, date):
        return relativedelta(date, self._birthday).years

    def getMongoObj(self):
        return {
            "tag": self._tag,
            "name": self._name,
            "birthday": self._birthday,
            "playerID": self._playerID,
            "country": self._country,
            "roles": self._roles
        }
    