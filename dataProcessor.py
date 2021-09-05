from APIConsumer import APIConsumer
from DatabaseConnector import DatabaseConnector
import json

class DataProcessor():

    def __init__(self) -> None:
        self.apic = APIConsumer()
        self.dbc = DatabaseConnector()
        self.tourneyList = None
        pass

    def fetchTourneyList(self):
        self.tourneyList = []
        offset = 0
        cont = True
        t1List = []
        Qlist = []
        while(cont):
            requestURL = str(self.apic.LiquipediaGetT1s + str(offset) + self.apic.LiquipediaSuffix)
            response = self.apic.getRequest(requestURL)
            # if I get a response
            if(response):
                print("Got a response")
                #if there needs to be another request
                try:
                    offset = response["query-continue-offset"]
                    print(offset)
                except:
                    cont = False
                for object in response["query"]["results"]:
                    t1List.append(object)
            else: 
                print("ERROR")
                break
        cont = True
        offset = 0
        while(cont):
            requestURL = str(self.apic.LiquipediaGetQs + str(offset) + self.apic.LiquipediaSuffix)
            response = self.apic.getRequest(requestURL)
            if(response):
                #if there needs to be another request
                try:
                    offset = response["query-continue-offset"]
                    print(offset)
                except:
                    cont = False
                for object in response["query"]["results"]:
                    Qlist.append(object)
            else:
                print("ERROR")
                break
        for tourney in t1List:
            if(tourney in Qlist):
                t1List.remove(tourney)
        self.dbc.insertMany(t1List, "Leagues")

datap = DataProcessor()
datap.fetchTourneyList()





        

