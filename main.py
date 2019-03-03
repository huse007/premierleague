from fantasy import *

'''
# EXAMPLES
export_to_CSV(getCurrentFixtures(),"fixtures/current_fixtures.csv")
export_to_CSV(getAllFixtures(),"fixtures/all_fixtures.csv")
export_to_CSV(getSortedStrength("strength_overall_home"),"stats/strength_overall_home.csv")
export_to_CSV(getSortedStrength("strength_overall_away"),"stats/strength_overall_away.csv")
export_to_CSV(getSortedStrength("strength_attack_home"),"stats/strength_attack_home.csv")
export_to_CSV(getSortedStrength("strength_attack_away"),"stats/strength_attack_away.csv")
export_to_CSV(getSortedStrength("strength_defence_home"),"stats/strength_defence_home.csv")
export_to_CSV(getSortedStrength("strength_defence_away"),"stats/strength_defence_away.csv")
export_to_CSV(getSortedStrength("strength"),"stats/strength.csv")
#export_to_CSV(getNextInfo(getTeamObj(getID("Arsenal")),"next_info.csv")

for i in datasets["teams"]:
    export_to_CSV(getNextInfo(i),"teams/next_game_"+i["name"]+".csv")

#pprint(datasets)
#pprint(getPlayers(1))

#showPlayers(1)
for i in datasets["elements"]:
    export_to_CSV(getPlayerDetails(i["id"]),"players/"+getPlayerName(i["id"])+".csv")
'''
