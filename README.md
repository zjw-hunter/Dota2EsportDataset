# Dota 2 Esport Dataset

This Project was making a public dataset for professional dota leagues and matches.
I included events from this [list](https://liquipedia.net/dota2/Tier_1_Tournaments)

## Database Specification

### Leagues

| Field | Type | Description |
| ---------- | ------- | ------------------------ |
| leagueName | String | The name of the league. |
| leagueID | String | The league's dotaTV id. |
| prizePool | Int | The league's prizepool in USD. |
| startDate | Date | The league's first main event day. |
| endDate | Date | The league's last main event day. |
| teams | Array | This contains json team objects. |
| url | String | This string is the url source for this data. |

### Teams

| Field | Type | Description |
| ---------- | ------- | ------------------------ |
| leagueName | String | The name of the league. |
| result | String | The place the team got. Ties are rounded up.|
| org | String | The team's organization |
| players | Array | An array of {role: \<the role that player had\>), player: \<playerObject\>} |

### Players

| Field | Type | Description |
| ---------- | ------- | ------------------------ |
| tag | String | The players tag. |
| playerName | String | The player's name (romanized in some cases). |
| birthday | Date | The player's birthday. |
| playerID | Int | The player's ID |
| country | Array | An array of strings with player's nation's names. |
| roles | String | The roles this player has played. |
| url | String | The url source of this data. |

### Matches

| Field | Type | Description |
| ---------- | ------- | ------------------------ |
| players | Array | Array of players that contains their stats for this match. |
| radiantWin | Boolean | True if radiant won. |
| duration | Int | Duration of the match in seconds. |
| matchID | Int | The ID of the match. |
| leagueID | Int | The ID of the league. |

## Dataset Notes

- Some teams have a name mismatch between the actual name and the name on the results notably: VG.r (Vici Gaming Reborn), 4 Anchors + Sea Captain, RoX, Relax, they have not been processed.
- Summit 5, 6 and 7 have a duplicate eventID 
- Players with no page on Liquipedia have not been processed.
- Some events do not an eventID they are: 
  - The International 2011
  - ASUS Open 2012 Finals
  - World Cyber Games 2012
  - Electronic Sports World Cup 2012
  - The Premier League: Season 2
  - DreamHack Summer 2012
  - StarLadder StarSeries Season 1
  - The Premier League: Season 1
  - The Premier League: Season 1
  - Dota2 Star Championship

## Additional Resources

In addition to the Dataset I also made some python classes for data collection and statistical operations. They are located in the source folder:

     /Dota2EsportDataset/Database_Objects/
I have also made the data collection tools available, feel free to use them to update the dataset or scan a different list of tournaments. 

In order to use them you will need to set a few environmental variables:

- To use the steam api you must generate a key and set the environmental variable 'STEAM_API_KEY' to its value. 
- I was using mongoDB locally so I set the environmental variable LOCALMONGOSTR to my mongoString.

For more details on the steam API see [here](https://wiki.teamfortress.com/wiki/WebAPI)

Thanks to the volunteers / editors of [Liquipedia](https://liquipedia.net/dota2/Main_Page) without whom this project would not have been possible.

Shoutout to [DatDota](http://www.datdota.com/) and Noxville for helping me out.
