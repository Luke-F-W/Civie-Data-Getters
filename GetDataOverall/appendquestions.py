import requests
import json
import os
import time

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
questionsfile = os.path.join(filepathabove, "Database", "json-all", "questions.json")
skip = 0

with open(questionsfile, "r", encoding="utf-8") as d:
    jsonloaded = json.load(d)

while skip < 10000:
    url = "https://api.oireachtas.ie/v1/questions?skip=" + str(skip) + "&limit=100&qtype=&show_answers=true"
    response = requests.get(url)
    response = response.json()["results"]

    for record in response:
        showas = record.get("question", {}).get("uri")
        if not any(item.get("question", {}).get("uri") == showas for item in jsonloaded):
            jsonloaded.append(record)
            print(record)
        else:
            pass   
            print("skipped")
    
    skip += 100
    time.sleep(0.1)

with open(questionsfile, "w", encoding="utf-8") as d:
    json.dump(jsonloaded, d, ensure_ascii=False, indent=2)

print("questions is done <-o->")