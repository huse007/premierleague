import csv
import urllib.request, json 
from pprint import pprint
import matplotlib.pyplot as plt
from teamID import teamID


def plot_transfers(limit: int) -> None:
    """ Plotting histogram of transfers
    
    Parameters:
    limit (int): Lower bound on the difference between transfers_in - transfers_out

    Returns:
    None 
    """
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


def load_dataset(name: str,url_addr: str) -> None:
    """ Loading datasets from URL

    Parameters:
    name (str): Name of the corresponding key
    url_addr (str): Endpoint URL for the data

    Returns:
    None
    """
    with urllib.request.urlopen(url_addr) as url:
        data = json.loads(url.read().decode())
    datasets[name] = data

def find_team_from_id(id: int) -> str:
    """ Get name of team

    Parameters: 
    id (int): ID of team.

    Returns:
    str: Name of team.
    """
    for i in datasets["teams"]:
        if i["id"] == id:
            return i["name"]


def export_to_CSV(csvlist:list,filename:str) -> None:
    """ Generating a CSV file from a list
    
    Parameters: 
    csvlist (list): List of strings
    filename (str): Name of output file 

    Returns:
    None
    """    
    if csvlist is None:
        print("[ERROR: export_to_CSV()]\n => List cannot be empty]")
        return None
    f = open("output/"+filename,"w+")
    for i in list:
        f.write("%s\n"%i)
    f.close()
    

def getID(team_name: str) -> int:
    """ Get ID
    
    Parameters:
    team_name (str): Name of team
    
    Returns:
    int: ID of team
    None: If team doesn't exist
    """
    for i in datasets["teams"]:
        if i["name"] == team_name:
            return i["id"]
    print("[ERROR : getID()]\n => Team name is not valid") 
    return None

def getName(team_id:int) -> str:
    """ Get name

    Parameters:
    team_id (int): ID of team.
    
    Returns:
    str: Name of team.
    None: If team doesn't exist
    """
    for i in datasets["teams"]:
        if i["id"] == team_id:
            return i["name"]
    print("[ERROR : getName()]\n => ID is not valid") 
    return None

def getTeamObj(team_id: int) -> dict:
    """ Get team object

    Parameters:
    team_id (int): ID of team.

    Returns:
    dict: Team object

    """
    for i in datasets["teams"]:
        if i["id"] == team_id:
            return i;
    print("[ERROR : getTeamObj()]\n => ID is not valid") 
    return None

def getCurrentFixtures() -> list:
    """ Get current week fixtures

    Parameters:

    Returns:
    list: List of CSV-formatted strings

    """
    tmp_data = []
    for i in datasets["bootstrap-static"]["next_event_fixtures"]:
        home = i["team_h"]
        away = i["team_a"]
        tmp_data.append(getName(home)+","+getName(away)+","+str(getTeamObj(home)["strength"]-getTeamObj(away)["strength"]))
    return tmp_data

def getAllFixtures() -> list:
    """ Get fixtures 

    Parameters:

    Returns:
    list: List of CSV-formatted strings
    """
    tmp_list = []
    header = "Gameweek,Time,Home,Away"
    tmp_list.append(header)
    for i in datasets["fixtures"]:
        home = getName(i["team_h"])
        away = getName(i["team_a"])
        time = i["kickoff_time_formatted"]
        gameweek = str(i["event"])
        if time == None:
            time = "Unknown"
        tmp_list.append(gameweek+","+time+","+home+","+away)
    return tmp_list

def getSortedStrength(key_name: str) -> list:
    """ Get sorted strength ranking list

    Parameters:
    key_name (str): Type of strength (Must be in allowed list)

    Returns:
    list: List of CSV-formatted strings

    """
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

def getNextInfo(home: int) -> list:
    """ Get match info

    Parameters:
    home (int): ID of home or away team

    Returns:
    list: List of CSV-formatted strings containing stats

    """
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

def getPlayers(team_id: int) -> list:
    """ Get player list of a team

    Parameters:
    team_id (int): ID of team.

    Returns:
    list: List of player objects

    """
    players = []
    for i in datasets["elements"]:
        if i["team"] == team_id:
            players.append(i)
    return players

def getPlayer(player_id: int) -> dict:
    """ Get player object

    Parameters:
    player_id (int): ID of player.

    Returns:
    dict: Player object.
    """
    for i in datasets["elements"]:
        if i["id"] == player_id:
            return i
    return None;

def showPlayers(team_id: int) -> None:
    """ Print players' id, first name and last name to console

    Parameters:
    team_id (int): ID of team.

    Returns:
    None

    """
    players = getPlayers(team_id)
    width=20
    print("ID".ljust(5)+"Second Name".ljust(width)+"First Name".ljust(width))
    for i in players:
        print(str(i["id"]).ljust(5)+i["second_name"].ljust(width)+i["first_name"].ljust(width))

def getPlayerDetails(player_id: int) -> list:
    """ Get details of player

    Parameters:
    player_id (int): ID of player

    Returns:
    list: List of CSV-formatted strings containg player stats.

    """
    player = getPlayer(player_id)
    tmp_list = []
    for i in player.keys():
        tmp_list.append(str(i)+","+str(player[i]))
    return tmp_list

def getPlayerName(player_id: int) -> str:
    """ Get name of player

    Parameters:
    player_id (int): ID of player.
    
    Returns:
    str: String containing second_name + first_name
  
    """
    for i in datasets["elements"]:
        if i["id"] == player_id:
            return i["second_name"]+"_"+i["first_name"]
    return None

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
load_dataset("elements",path+"elements")
#Uncomment the line below to import your personal team (Remember to set your teamID in teamID.py)
#load_dataset("my-team",path+"my-team/"+teamID)
