import csv
import urllib.request, json 
import json
from pprint import pprint
import matplotlib.pyplot as plt

# FUNCTIONS
''' limit is the lower bound of transfers in - transfers out '''
def plot_transfers(limit):
    myList = {}
    plt.xlabel("Players");
    plt.ylabel("Number of Transfer Out")
    for i in datasets["bootstrap-static"]["elements"]:
        if i["in_dreamteam"] is True:
            print(i["id"], i["second_name"])
        if (i["transfers_in_event"]-i["transfers_out_event"])>limit:
            myList[i["second_name"]] = i["transfers_in_event"]-i["transfers_out_event"]
    plt.bar(myList.keys(), myList.values())
    plt.show()

''' loading dataset from url '''
def load_dataset(name,url_addr):
    with urllib.request.urlopen(url_addr) as url:
        data = json.loads(url.read().decode())
    datasets[name] = data

''' input: id
return value: team name '''
def find_team_from_id(id):
    for i in datasets["teams"]:
        if i["id"] == id:
            return i["name"]

''' Printing next opponent to file 
tw: left ajust width '''
def print_next_games_to_csv():
    tw = 15 
    with open('output.csv', mode='w') as outputfile:
              output_writer = csv.writer(outputfile,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
              ''' Print header '''
              output_writer.writerow(["ID".ljust(tw), "STRENGTH".ljust(tw), "NAME".ljust(tw), "OPPONENT".ljust(tw)])
              for i in datasets["teams"]:
                      '''Print row '''
                      output_writer.writerow([str(i["id"]).ljust(tw), str(i["strength"]).ljust(tw), i["name"].ljust(tw), find_team_from_id(i["next_event_fixture"][0]["opponent"]).ljust(tw)])

''' Generating a CSV file from a list
input: list of strings, name of file '''
def export_to_CSV(list,filename):
    if list is None:
        print("[ERROR: export_to_CSV()]\n => List cannot be empty]")
        return None
    f = open("output/"+filename,"w+")
    for i in list:
        f.write("%s\n"%i)
    f.close()
    
''' input argument: name of team
return: id of team (or None if team doesn't exist)'''
def getID(team_name):
    for i in datasets["teams"]:
        if i["name"] == team_name:
            return i["id"]
    print("[ERROR : getID()]\n => Team name is not valid") 
    return None

''' input argument: team id
return: name of team (or None)'''
def getName(team_id):
    for i in datasets["teams"]:
        if i["id"] == team_id:
            return i["name"]
    print("[ERROR : getName()]\n => ID is not valid") 
    return None

def getTeamObj(team_id):
    for i in datasets["teams"]:
        if i["id"] == team_id:
            return i;
    print("[ERROR : getTeamObj()]\n => ID is not valid") 
    return None

def getCurrentFixtures():
    tmp_data = []
    for i in datasets["bootstrap-static"]["next_event_fixtures"]:
        home = i["team_h"]
        away = i["team_a"]
        tmp_data.append(getName(home)+","+getName(away)+","+str(getTeamObj(home)["strength"]-getTeamObj(away)["strength"]))
    return tmp_data

def getAllFixtures():
    tmp_list = []
    header = "Time,Home,Away"
    tmp_list.append(header)
    for i in datasets["fixtures"]:
        home = getName(i["team_h"])
        away = getName(i["team_a"])
        time = i["kickoff_time_formatted"]
        if time == None:
            time = "Unknown"
        tmp_list.append(time+","+home+","+away)
    return tmp_list

''' returns a defensive ranking list
key_name must be in allowed ''' 
def getSortedStrength(key_name):
    allowed = ["strength_overall_home", "strength_overall_away", "strength_attack_home","strength_attack_away", "strength_defence_home", "strength_defence_away","strength"]
    if key_name not in allowed:
        print("[ERROR : Invalid key_name from getSortedStrength()]\n"," => Allowed key_names are:"+str(allowed))
        return None
    tmp_list = []
    copy_datasets = datasets["teams"].copy()
    tmp_list.append("ID,Team,"+key_name)
    length = len(datasets["teams"])
    for i in range(0,20):
        max_value = 0
        for j in range(0,len(copy_datasets)):
            if copy_datasets[j][key_name] >= copy_datasets[max_value][key_name]:
                max_value = j
        current = copy_datasets.pop(max_value)
        tmp_list.append(str(current["id"])+","+current["name"]+","+str(current[key_name]))
    return tmp_list

''' returns a list of stats for the next game 
input: one of the teams '''
def getNextInfo(home):
    if home is None:
        print("[ERROR : getNextInfo()]\n => ID is None")
    away = getTeamObj(home["next_event_fixture"][0]["opponent"])
    if home["next_event_fixture"][0]["is_home"] == False:
        new_home = away
        away = home
        home = new_home
    tmp_list = []
    tmp_list.append("Property,Home,Away")
    tmp_list.append("id,"+str(home["id"])+","+str(away["id"]))
    tmp_list.append("name,"+home["name"]+","+away["name"])
    tmp_list.append("short_name,"+home["short_name"]+","+away["short_name"])
    tmp_list.append("strength,"+str(home["strength"])+","+str(away["strength"]))
    tmp_list.append("strength_overall_home,"+str(home["strength_overall_home"])+","+str(away["strength_overall_home"]))
    tmp_list.append("strength_overall_away,"+str(home["strength_overall_away"])+","+str(away["strength_overall_home"]))
    tmp_list.append("strength_attack_home,"+str(home["strength_attack_home"])+","+str(away["strength_attack_home"]))
    tmp_list.append("strength_attack_away,"+str(home["strength_attack_away"])+","+str(away["strength_attack_away"]))
    tmp_list.append("strength_defence_home,"+str(home["strength_defence_home"])+","+str(away["strength_defence_home"]))
    tmp_list.append("strength_defence_away,"+str(home["strength_defence_away"])+","+str(away["strength_defence_away"]))
    tmp_list.append("next_event_fixture_is_home,"+str(home["next_event_fixture"][0]["is_home"])+","+str(away["next_event_fixture"][0]["is_home"]))
    return tmp_list    

# VARIABLES                      
''' URL path '''
path =  "https://fantasy.premierleague.com/drf/"        

# DATA STRUCTURES
''' datasets is a dictionary which will keep all 
loaded datasets. datasets ={ 'Fixture': dataset, ...} '''
datasets = {}

# INITIALIZE
''' LOADING DATASETS FROM URL's
pass a name and url to function: load_dataset(name, url) '''
load_dataset("fixtures", path+"fixtures")
load_dataset("teams", path+"teams")
load_dataset("region", path+"region")
load_dataset("bootstrap-static", path+"bootstrap-static")


