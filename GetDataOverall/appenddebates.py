import requests
import json
import os
import time

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
debatesfile = os.path.join(filepathabove, "Database", "json-all", "debates.json")
skip = 0

with open(debatesfile, "r", encoding="utf-8") as d:
    jsonloaded = json.load(d)

while skip < 10000:
    url = "https://api.oireachtas.ie/v1/debates?skip=" + str(skip) + "&limit=100"
    response = requests.get(url)
    response = response.json()["results"]

    for record in response:
        showas = record.get("debateRecord", {}).get("uri")
        if not any(item.get("debateRecord", {}).get("uri") == showas for item in jsonloaded):
            jsonloaded.append(record)
            print(record)
        else:
            pass   
            print("skipped")
    
    skip += 100
    time.sleep(0.1)

with open(debatesfile, "w", encoding="utf-8") as d:
    json.dump(jsonloaded, d, ensure_ascii=False, indent=2)

print("debates is done <-o->")