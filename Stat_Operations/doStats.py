import Database_Objects.league as league
import Database_Objects.match as dotaMatch
import Database_Objects.player as player
import Database_Objects.team as team
import Database_Objects.regression as regression
from DatabaseConnector import DatabaseConnector, databaseCollections
import os
from dateutil.relativedelta import relativedelta

class doStats():

    def __init__(self):
        self.dbc = DatabaseConnector(os.environ['LOCALMONGOSTR'])
        self.tiList = None

    #gets a list of all the TI events as league objects.
    def getDependents(self):
        self.tiList = []
        for iter in self.dbc.makeQuery({league.leagueAttributes.LEAGUENAME.value: {'$regex': 'The International'}}, databaseCollections.LEAGUES):
            self.tiList.append(league.league.from_dict(iter))
        

    #How does a participant's (methodname) effect their result at TI uses individual, team and roster
    def avgLeagueResult(self, groupType):
        #for each ti
        #dep is the TI result
        dependents = []
        #ind is the avg result of leagues before that TI
        independents = []
        # each TI
        
                
        if(groupType == regression.regressionGroupType.INDIVIDUAL):
            for ti in self.tiList:
            # each Team at that TI
                for t in ti._teams:
                    # each player in that team
                    # generate team object
                    participant = team.team.fromDict(t, ti._leagueName)
                    #each player in the team
                    for p in participant._players:
                        #generate A player object
                        thisPlayer = player.player.fromDict(p['player'])
                        #find all their prior tournaments
                        priors = self.dbc.makeQuery({'$and': [{'teams.players.player.playerID': thisPlayer._playerID}, {'endDate': {'$lt': ti._startDate}} ]}, databaseCollections.LEAGUES)
                        resultList = []
                        # if they have more than 0 priors
                        if priors.count() > 0:
                            #for each prior
                            for prior in priors:
                                #get that team
                                teamItem = list(self.dbc.makeQuery({'$and': [{'leagueName': prior['leagueName']}, {'players.player.playerID': thisPlayer._playerID}]}, databaseCollections.TEAMS))
                                # if they got DQ or DNF don't count results.
                                if( len(teamItem) > 0):
                                    resultList.append(self.placeStringToInt(teamItem[0]['result']))
                            # if they have valid priors
                            if(not resultList == []):
                                independents.append( sum(resultList) / len(resultList) )
                                dependents.append(self.placeStringToInt(participant._result))
            return regression.regression(dependents, [independents], groupType, "Individual_Past_Results", ["Avg_Prior_League_Result"], "TI_Result", "Prior_Individual_Results_Effect_on_TI_Result")
        elif( groupType == regression.regressionGroupType.TEAM):
            for ti in self.tiList:
                # each Team at that TI
                for t in ti._teams:
                    # each player in that team
                    # generate team object
                    participant = team.team.fromDict(t, ti._leagueName)
                    resultList = []
                    for p in participant._players:
                        #generate A player object
                        thisPlayer = player.player.fromDict(p['player'])
                        #find all their prior tournaments
                        priors = self.dbc.makeQuery({'$and': [{'teams.players.player.playerID': thisPlayer._playerID}, {'endDate': {'$lt': ti._startDate}} ]}, databaseCollections.LEAGUES)
                        # if they have more than 0 priors
                        if priors.count() > 0:
                            #for each prior
                            for prior in priors:
                                #get that team
                                teamItem = list(self.dbc.makeQuery({'$and': [{'leagueName': prior['leagueName']}, {'players.player.playerID': thisPlayer._playerID}]}, databaseCollections.TEAMS))
                                # if they got DQ or DNF don't count results.
                                if( len(teamItem) > 0):
                                    resultList.append(self.placeStringToInt(teamItem[0]['result']))
                            # if they have valid priors
                    if(not resultList == []):
                        independents.append( sum(resultList) / len(resultList) )
                        dependents.append(self.placeStringToInt(participant._result))
            return regression.regression(dependents, [independents], groupType, "Team_Past_Results", ["Avg_Prior_League_Result"], "TI_Result", "Prior_Team_Results_Effect_on_TI_Result")
        
        elif( groupType == regression.regressionGroupType.ROSTER):
            for ti in self.tiList:
                # each Team at that TI
                for t in ti._teams:
                    # each player in that team
                    # generate team object
                    participant = team.team.fromDict(t, ti._leagueName)
                    resultList = []
                    playerIDs = []
                    # Get the IDs of their roster
                    for p in participant._players:
                        playerIDs.append(p['player']['playerID'])

                    for prior in self.dbc.makeQuery({"$and": [{"teams": { "$elemMatch": {"players": {"$not": {"$elemMatch": {'player.playerID': {"$nin": playerIDs}}}}}}}, { "teams": {"$not": {"$elemMatch": {"players": []}}}}, {'endDate': {'$lt': ti._startDate}}]}, databaseCollections.LEAGUES):
                        teamItems = list(self.dbc.makeQuery({'$and': [{'leagueName': prior['leagueName']}, {'org': t['org']}]}, databaseCollections.TEAMS))

                        for thisTeam in teamItems:
                            resultList.append(self.placeStringToInt(thisTeam['result']))
                    if(not resultList == []):
                        independents.append( sum(resultList) / len(resultList) )
                        dependents.append(self.placeStringToInt(participant._result))
            return regression.regression(dependents, [independents], groupType, "Roster_Past_Results", ["Avg_Prior_League_Result"], "TI_Result", "Prior_Roster_Results_Effect_on_TI_Result")

    
    
    #Results since last TI 
    def avgRecentLeagueResult(self, groupType):
       #for each ti
        #dep is the TI result
        dependents = []
        #ind is the avg result of leagues before that TI
        independents = []
        # each TI
        
        
        if(groupType == regression.regressionGroupType.INDIVIDUAL):
            for ti in self.tiList:
                lti = self.lastTI(ti)
            # each Team at that TI
                for t in ti._teams:
                    # each player in that team
                    # generate team object
                    participant = team.team.fromDict(t, ti._leagueName)
                    #each player in the team
                    for p in participant._players:
                        #generate A player object
                        thisPlayer = player.player.fromDict(p['player'])
                        #find all their prior tournaments
                        priors = self.dbc.makeQuery({'$and': [{'teams.players.player.playerID': thisPlayer._playerID}, {'endDate': {'$lt': ti._startDate}}, {'startDate': {'$gt': lti._endDate}}]}, databaseCollections.LEAGUES)
                        resultList = []
                        # if they have more than 0 priors
                        if priors.count() > 0:
                            #for each prior
                            for prior in priors:
                                #get that team
                                teamItem = list(self.dbc.makeQuery({'$and': [{'leagueName': prior['leagueName']}, {'players.player.playerID': thisPlayer._playerID}]}, databaseCollections.TEAMS))
                                # if they got DQ or DNF don't count results.
                                if( len(teamItem) > 0):
                                    resultList.append(self.placeStringToInt(teamItem[0]['result']))
                            # if they have valid priors
                            if(not resultList == []):
                                independents.append( sum(resultList) / len(resultList) )
                                dependents.append(self.placeStringToInt(participant._result))
            return regression.regression(dependents, [independents], groupType, "Individual_Recent_Past_Results", ["Avg_Recent_Prior_League_Result"], "TI_Result", "Prior_Recent_Individual_Results_Effect_on_TI_Result")
        elif( groupType == regression.regressionGroupType.TEAM):
            for ti in self.tiList:
                lti = self.lastTI(ti)
                # each Team at that TI
                for t in ti._teams:
                    # each player in that team
                    # generate team object
                    participant = team.team.fromDict(t, ti._leagueName)
                    resultList = []
                    for p in participant._players:
                        #generate A player object
                        thisPlayer = player.player.fromDict(p['player'])
                        #find all their prior tournaments
                        priors = self.dbc.makeQuery({'$and': [{'teams.players.player.playerID': thisPlayer._playerID}, {'endDate': {'$lt': ti._startDate}}, {'startDate': {'$gt': lti._endDate}}]}, databaseCollections.LEAGUES)
                        # if they have more than 0 priors
                        if priors.count() > 0:
                            #for each prior
                            for prior in priors:
                                #get that team
                                teamItem = list(self.dbc.makeQuery({'$and': [{'leagueName': prior['leagueName']}, {'players.player.playerID': thisPlayer._playerID}]}, databaseCollections.TEAMS))
                                # if they got DQ or DNF don't count results.
                                if( len(teamItem) > 0):
                                    resultList.append(self.placeStringToInt(teamItem[0]['result']))
                            # if they have valid priors
                    if(not resultList == []):
                        independents.append( sum(resultList) / len(resultList) )
                        dependents.append(self.placeStringToInt(participant._result))
            return regression.regression(dependents, [independents], groupType, "Team_Recent_Past_Results", ["Avg_Recent_Prior_League_Result"], "TI_Result", "Prior_Recent_Team_Results_Effect_on_TI_Result")
        
        elif( groupType == regression.regressionGroupType.ROSTER):
            for ti in self.tiList:
                lti = self.lastTI(ti)
                # each Team at that TI
                for t in ti._teams:
                    # each player in that team
                    # generate team object
                    participant = team.team.fromDict(t, ti._leagueName)
                    resultList = []
                    playerIDs = []
                    # Get the IDs of their roster
                    for p in participant._players:
                        playerIDs.append(p['player']['playerID'])

                    for prior in self.dbc.makeQuery({"$and": [{"teams": { "$elemMatch": {"players": {"$not": {"$elemMatch": {'player.playerID': {"$nin": playerIDs}}}}}}}, { "teams": {"$not": {"$elemMatch": {"players": []}}}}, {'endDate': {'$lt': ti._startDate}},{'startDate': {'$gt': lti._endDate}} ]}, databaseCollections.LEAGUES):
                        teamItems = list(self.dbc.makeQuery({'$and': [{'leagueName': prior['leagueName']}, {'org': t['org']}]}, databaseCollections.TEAMS))

                        for thisTeam in teamItems:
                            resultList.append(self.placeStringToInt(thisTeam['result']))
                    if(not resultList == []):
                        independents.append( sum(resultList) / len(resultList) )
                        dependents.append(self.placeStringToInt(participant._result))
            return regression.regression(dependents, [independents], groupType, "Roster_Recent_Past_Results", ["Avg_Recent_Prior_League_Result"], "TI_Result", "Recent_Prior_Roster_Results_Effect_on_TI_Result")
    
    
    def avgTIResult(self, groupType):
        #for each ti
        #dep is the TI result
        dependents = []
        #ind is the avg result of leagues before that TI
        independents = []
        # each TI
        
                
        if(groupType == regression.regressionGroupType.INDIVIDUAL):
            for ti in self.tiList:
            # each Team at that TI
                for t in ti._teams:
                    # each player in that team
                    # generate team object
                    participant = team.team.fromDict(t, ti._leagueName)
                    #each player in the team
                    for p in participant._players:
                        #generate A player object
                        thisPlayer = player.player.fromDict(p['player'])
                        #find all their prior tournaments
                        priors = self.dbc.makeQuery({'$and': [{'leagueName': {'$regex': 'The International'}}, {'teams.players.player.playerID': thisPlayer._playerID}, {'endDate': {'$lt': ti._startDate}} ]}, databaseCollections.LEAGUES)
                        resultList = []
                        # if they have more than 0 priors
                        if priors.count() > 0:
                            #for each prior
                            for prior in priors:
                                #get that team
                                teamItem = list(self.dbc.makeQuery({'$and': [{'leagueName': prior['leagueName']}, {'players.player.playerID': thisPlayer._playerID}]}, databaseCollections.TEAMS))
                                # if they got DQ or DNF don't count results.
                                if( len(teamItem) > 0):
                                    resultList.append(self.placeStringToInt(teamItem[0]['result']))
                            # if they have valid priors
                            if(not resultList == []):
                                independents.append( sum(resultList) / len(resultList) )
                                dependents.append(self.placeStringToInt(participant._result))
            return regression.regression(dependents, [independents], groupType, "Individual_Past_TI_Results", ["Avg_Prior_TI_Result"], "TI_Result", "Prior_Individual_TI_Results_Effect_on_TI_Result")
        elif( groupType == regression.regressionGroupType.TEAM):
            for ti in self.tiList:
                # each Team at that TI
                for t in ti._teams:
                    # each player in that team
                    # generate team object
                    participant = team.team.fromDict(t, ti._leagueName)
                    resultList = []
                    for p in participant._players:
                        #generate A player object
                        thisPlayer = player.player.fromDict(p['player'])
                        #find all their prior tournaments
                        priors = self.dbc.makeQuery({'$and': [{'leagueName': {'$regex': 'The International'}}, {'teams.players.player.playerID': thisPlayer._playerID}, {'endDate': {'$lt': ti._startDate}} ]}, databaseCollections.LEAGUES)
                        # if they have more than 0 priors
                        if priors.count() > 0:
                            #for each prior
                            for prior in priors:
                                #get that team
                                teamItem = list(self.dbc.makeQuery({'$and': [{'leagueName': prior['leagueName']}, {'players.player.playerID': thisPlayer._playerID}]}, databaseCollections.TEAMS))
                                # if they got DQ or DNF don't count results.
                                if( len(teamItem) > 0):
                                    resultList.append(self.placeStringToInt(teamItem[0]['result']))
                            # if they have valid priors
                    if(not resultList == []):
                        independents.append( sum(resultList) / len(resultList) )
                        dependents.append(self.placeStringToInt(participant._result))
            return regression.regression(dependents, [independents], groupType, "Team_Past_TI_Results", ["Avg_Prior_TI_Result"], "TI_Result", "Prior_Team_TI_Results_Effect_on_TI_Result")
        elif( groupType == regression.regressionGroupType.ROSTER):
            for ti in self.tiList:
                # each Team at that TI
                for t in ti._teams:
                    # each player in that team
                    # generate team object
                    participant = team.team.fromDict(t, ti._leagueName)
                    resultList = []
                    playerIDs = []
                    # Get the IDs of their roster
                    for p in participant._players:
                        playerIDs.append(p['player']['playerID'])

                    for prior in self.dbc.makeQuery({"$and": [{'leagueName': {'$regex': 'The International'}}, {"teams": { "$elemMatch": {"players": {"$not": {"$elemMatch": {'player.playerID': {"$nin": playerIDs}}}}}}}, { "teams": {"$not": {"$elemMatch": {"players": []}}}}, {'endDate': {'$lt': ti._startDate}}]}, databaseCollections.LEAGUES):
                        teamItems = list(self.dbc.makeQuery({'$and': [{'leagueName': prior['leagueName']}, {'org': t['org']}]}, databaseCollections.TEAMS))

                        for thisTeam in teamItems:
                            resultList.append(self.placeStringToInt(thisTeam['result']))
                    if(not resultList == []):
                        independents.append( sum(resultList) / len(resultList) )
                        dependents.append(self.placeStringToInt(participant._result))
            return regression.regression(dependents, [independents], groupType, "Roster_Past_TI_Results", ["Avg_Prior_TI_Result"], "TI_Result", "Prior_Roster_TI_Results_Effect_on_TI_Result")


    # def gamesPlayed(self, groupType):
    #     #for each ti
    #     #dep is the TI result
    #     dependents = []
    #     #ind is the avg result of leagues before that TI
    #     independents = []
    #     # each TI
        
                
    #     if(groupType == regression.regressionGroupType.INDIVIDUAL):
    #         for ti in self.tiList:
    #         # each Team at that TI
    #             for t in ti._teams:
    #                 # each player in that team
    #                 # generate team object
    #                 participant = team.team.fromDict(t, ti._leagueName)
    #                 #each player in the team
    #                 for p in participant._players:
    #                     #generate A player object
    #                     thisPlayer = player.player.fromDict(p['player'])
    #                     #find all their prior tournaments
    #                     matchCount = self.dbc.makeQuery({"players.account_id": thisPlayer._playerID}, databaseCollections.MATCHES).count()
                        
    #                     independents.append( matchCount )
    #                     dependents.append(self.placeStringToInt(participant._result))
    #         return regression.regression(dependents, [independents], groupType, "Individual_Games_Played", ["Games_Played"], "TI_Result", "Games_Played_Effect_on_TI_Result")
    #     elif( groupType == regression.regressionGroupType.TEAM):
    #         for ti in self.tiList:
    #             # each Team at that TI
    #             for t in ti._teams:
    #                 # each player in that team
    #                 # generate team object
    #                 participant = team.team.fromDict(t, ti._leagueName)
    #                 totalMatchCount = 0
    #                 for p in participant._players:
    #                     #generate A player object
    #                     thisPlayer = player.player.fromDict(p['player'])
    #                     totalMatchCount += self.dbc.makeQuery({"players.account_id": thisPlayer._playerID}, databaseCollections.MATCHES).count()
    #                 independents.append( totalMatchCount )
    #                 dependents.append(self.placeStringToInt(participant._result))
                    
    #         return regression.regression(dependents, [independents], groupType, "Team_Games_Played", ["Games_Played"], "TI_Result", "Games_Played_Effect_on_TI_Result")
        
    #Helpers
    def placeStringToInt(self, placeString):
        return int(placeString.strip()[0:-2])

    def lastTI(self, thisTI):
        lTI = thisTI
        prev = []
        for ti in self.tiList:
            if( ti._startDate < thisTI._startDate):
                prev.append(ti)
        if len(prev) == 0 :
            return thisTI
        lTI = prev[0]
        for ti in prev:
            if( thisTI._startDate - lTI._startDate > thisTI._startDate - ti._startDate):
                lTI = ti
        return lTI


    def doStats(self):
        tiList = self.getDependents()
        self.gamesPlayed(regression.regressionGroupType.TEAM)
        