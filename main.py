import Database_Objects
from Stat_Operations.doStats import doStats
from DatabaseConnector import databaseCollections, DatabaseConnector
from Database_Objects import league, team
import os
myDS = doStats()
myDS.doStats()

# mydbc = DatabaseConnector(os.environ['LOCALMONGOSTR'])

# gatheredData = []
# for l in mydbc.makeQuery({}, databaseCollections.LEAGUES):
#     myLeague = league.league.from_dict(l)
#     for t in myLeague._teams:
#         gatheredData.append(
#             team.team(t['leagueID'], t['result'], t['org'], t['players'], myLeague._leagueName).getMongoObj()

#           )
# mydbc.insertMany(gatheredData, databaseCollections.TEAMS)
        