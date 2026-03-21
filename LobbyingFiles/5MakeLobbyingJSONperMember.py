'''
This pulls all data from the oireachtas api per member, and saves it
As a JSON file per membercode, allowing me to keep easier to query records.
'''
import time
import pandas as pd
import os 

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
maincsv = os.path.join(filepathabove, "maincsv.csv") #csv to make json from
save = os.path.join(filepathabove, "Database", "json-lobbying") #save to here
codes = os.path.join(filepathabove, "codes.txt") #membercodes

csvv = pd.read_csv(maincsv, sep=',')

with open(codes, encoding='utf-8') as f:
    for id in f:
        id = id.strip()
        filtered = csvv["MemberCodes"]
        filtered = filtered.str.contains(id, na=False)
        filtered = csvv[filtered]

        if filtered.empty:
            continue

        filtered.to_json(
            os.path.join(save, "lobby" + id + ".json"),
            orient="records",
            indent=2,
            force_ascii=False
        )
        print(id + "is done <-o->")
        time.sleep(0.1)