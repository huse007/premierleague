from fantasy import *

'''
export_to_CSV(getCurrentFixtures(),"current_fixtures.csv")
export_to_CSV(getAllFixtures(),"all_fixtures.csv")
export_to_CSV(getSortedStrength("strength_overall_home"),"strength_overall_home.csv")
export_to_CSV(getSortedStrength("strength_overall_away"),"strength_overall_away.csv")
export_to_CSV(getSortedStrength("strength_attack_home"),"strength_attack_home.csv")
export_to_CSV(getSortedStrength("strength_attack_away"),"strength_attack_away.csv")
export_to_CSV(getSortedStrength("strength_defence_home"),"strength_defence_home.csv")
export_to_CSV(getSortedStrength("strength_defence_away"),"strength_defence_away.csv")
export_to_CSV(getSortedStrength("strength"),"strength.csv")
#export_to_CSV(getNextInfo(getTeamObj(getID("Arsenal")),"next_info.csv")

for i in datasets["teams"]:
    export_to_CSV(getNextInfo(i),"teams/next_game_"+i["name"]+".csv")

#pprint(datasets)
#pprint(getPlayers(1))

#showPlayers(1)
for i in datasets["elements"]:
    export_to_CSV(getPlayerDetails(i["id"]),"players/"+getPlayerName(i["id"])+".csv")
'''
