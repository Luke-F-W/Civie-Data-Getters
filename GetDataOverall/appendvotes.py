import requests
import json
import os
import time

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
votesfile = os.path.join(filepathabove, "Database", "json-all", "votes.json")
skip = 0

with open(votesfile, "r", encoding="utf-8") as d:
    jsonloaded = json.load(d)

while skip < 10000:
    url = "https://api.oireachtas.ie/v1/votes?skip=" + str(skip) + "&limit=100&outcome="
    response = requests.get(url)
    response = response.json()["results"]

    for record in response:
        showas = record.get("division", {}).get("uri")
        if not any(item.get("division", {}).get("uri") == showas for item in jsonloaded):
            jsonloaded.append(record)
            print(record)
        else:
            pass   
            print("skipped")
    
    skip += 100
    time.sleep(0.1)

with open(votesfile, "w", encoding="utf-8") as d:
    json.dump(jsonloaded, d, ensure_ascii=False, indent=2)

print("votes is done <-o->")