import requests
import time
import json
import os

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
codes = os.path.join(filepathabove, "codes.txt")

with open(codes, encoding="utf-8") as f:
    for membercode in f:
        membercode = membercode.strip()
        out = os.path.join(filepathabove, "Database", "json-questions", "question" + membercode + ".json")

        if os.path.exists(out):
            with open(out, "r", encoding="utf-8") as d:
                alldata = json.load(d)
        else:
            alldata = []

        url = "https://api.oireachtas.ie/v1/questions?skip=0&limit=10000&qtype=oral,written&member_id=%20%2Fie%2Foireachtas%2Fmember%2Fid%2F" + membercode + "&show_answers=true"
        response = requests.get(url)
        data = response.json().get("results", [])

        for record in data:
            uri = record.get("question", {}).get("uri")
            if not any(item.get("question", {}).get("uri") == uri for item in alldata):
                alldata.append(record)
                print(record)
            else:
                pass
                print("skipped")
        
        with open(out, "w", encoding="utf-8") as d:
            json.dump(alldata, d, indent=2, ensure_ascii=False)

        print(membercode + " is done <-o->")
        time.sleep(0.3)

print("all done <-o->")