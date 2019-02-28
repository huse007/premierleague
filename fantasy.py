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

# PROGRAM FLOW
''' PLOT TRANSFERS arg'''
plot_transfers(10000)

# EXPORT DATA TO FILES
''' PRINT SIMPLE OUTPUT TO CSV FILE '''
print_next_games_to_csv()

