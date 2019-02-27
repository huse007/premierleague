import json
from pprint import pprint
import matplotlib.pyplot as plt
with open('bootstrap-static') as f:
    data = json.load(f)

myList={}
#pprint(data)
for i in data["elements"]:
    if i["in_dreamteam"] is True:
        print(i["id"], i["second_name"])
    if (i["transfers_in_event"]-i["transfers_out_event"])>20000:
        myList[i["second_name"]] = i["transfers_in_event"]-i["transfers_out_event"]

#print(myList)
plt.bar(myList.keys(), myList.values())
          
#plt.hist(a)
plt.xlabel("Players");
plt.ylabel("Number of Transfer Out")
plt.show()

