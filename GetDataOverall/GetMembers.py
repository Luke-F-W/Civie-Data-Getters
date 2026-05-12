import requests
import json
import os
import time

#get the path to save to
file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
out = os.path.join(filepathabove, "Database", "json-all", "members.json")
data = []
skip = 0

#goes through all records for members
while skip < 384:
    url = "https://api.oireachtas.ie/v1/members?date_start=2015-01-01&skip=" + str(skip) + "&limit=100"
    
    response = requests.get(url)
    response = response.json()["results"]
    
    for record in response:
        memberCode = record.get("member", {}).get("memberCode")
        record["member"]["image"] = "https://data.oireachtas.ie/ie/oireachtas/member/id/" + memberCode + "/image/large"
    
    data += response
    skip += 100
    print("got 100 records, we are now at:" + str(skip))
    time.sleep(0.3)
        
with open(out, "w", encoding="utf-8") as d:
    json.dump(data, d, indent=2, ensure_ascii=False)

print("members is done <-o->")