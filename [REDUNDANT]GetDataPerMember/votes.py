"""
This script loops through each line in a txt file with membercodes,
(the file can be found in the repository) and gets a JSON of all
votes of theirs and saves it as vote+membercode.json. I reuse this code 
in the other sections (excluding lobbying).
"""
import requests
import time
import json
import os

#get path for codes
file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
codes = os.path.join(filepathabove, "codes.txt")

with open(codes, encoding='utf-8') as f:
    for membercode in f:
        membercode = membercode.strip()
        url = "https://api.oireachtas.ie/v1/votes?skip=0&limit=10000&member_id=%2Fie%2Foireachtas%2Fmember%2Fid%2F" + membercode
        
        response = requests.get(url)
        data = response.json()
        out = os.path.join(filepathabove, "Database", "json-votes", "vote" + membercode + ".json")
        with open(out, "w", encoding="utf-8") as d:
            json.dump(data, d, indent=2, ensure_ascii=False)
        
        print(membercode + "is done <-o->")
        time.sleep(0.3)