import json
import os

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
membersfile = os.path.join(filepath, "Database", "json-all", "members.json")
outfile = os.path.join(filepath, "codes.txt")

with open(membersfile, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(outfile, "w", encoding="utf-8") as f:
    for record in data:
        memberCode = record.get("member", {}).get("memberCode")
        if memberCode:
            f.write(memberCode + "\n")

print("done <-o->")
