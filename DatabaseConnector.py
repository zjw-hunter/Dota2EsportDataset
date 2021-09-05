from pymongo import MongoClient
from pprint import pprint

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
        if(cName not in self.DOTA_COLLECTIONS):
            return False
        if(data is None):
            return False
        try:
            if( cName == "Players"):
                self.db.Players.insert_many(data)
            elif( cName == "Matches"):
                self.db.Matches.insert_many(data)
            elif( cName == "Teams"):
                self.db.Teams.insert_many(data)
            elif( cName == "Leagues"):
                self.db.Leagues.insert_many(data)
            else:
                return False
            return True
        except Exception as e:
            print(e)
            return False