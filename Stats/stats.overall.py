"""
Generates an overallStats.json file used for homepage stats on the Oireachtas
data visualisation dashboard. Pulls from lobbying & members. I chose lobbying as it is was what this
project was originally meant to focus on before i expanded it to include bills, votes etc...
the members list produces party seat breakdowns for the Dail and Seanad, plus
top 5 rankings across lobbying, and lobbyist.
"""
import os
import json
import unicodedata
import re
from collections import Counter

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)

#paths
memberss = os.path.join(filepathabove, "Database", "json-members", "members.json")
outputt = os.path.join(filepathabove, "Database", "json-stats")

lobbyy = os.path.join(filepathabove, "Database", "json-all", "lobbying.json")

def normalisename(name):
    name = unicodedata.normalize('NFKD', name)
    name = name.encode('ASCII', 'ignore')
    name = name.decode('utf-8')
    name = re.sub('[^a-zA-Z]', '', name)
    return name.lower()

members = open(memberss, encoding="utf-8")
members = json.load(members)
memberlookup = {}

dail = Counter()
seanad = Counter()

for id in members:
    memberlookup[id["memberCode"]] = id
    chamber = id["memberCode"].split(".")
    chamber = chamber[1]
    #John-Brady.D.2016-10-03 (this is an example of a membercode), the "D" is the chamber
    if chamber == "D":
        dail[id["party_code"]] += 1
    elif chamber == "S":
        seanad[id["party_code"]] += 1

raw = open(lobbyy, encoding="utf-8")
lobbydata = json.load(raw)

lobbypm = Counter()
alllobbyists = Counter()

#gets lobbyist name, normalises, then adds
for record in lobbydata:
    lobbyistname = record["Lobbyist Name"]
    lobbyistname = normalisename(lobbyistname)
    alllobbyists[lobbyistname] += 1

#splits membercodes by :: and counts
for record in lobbydata:
    codes = record.get("MemberCodes")
    for code in codes.split("::"):
        if code in memberlookup:
            lobbypm[code] += 1

lobbied = []
for item in lobbypm.most_common(5):
    code = item[0] 
    count = item[1]

    m = memberlookup[code]
    lobbied.append({
        "name": m["fullName"],
        "party": m["party_code"],
        "count": count
    })

finaldail =   dict(dail.most_common())
finalseanad = dict(seanad.most_common())
finallobbyist = dict(alllobbyists.most_common(5))
#output
stats = {
    "members": {
        "dail_by_party":   finaldail,
        "seanad_by_party": finalseanad
    },
    "lobbying": {
        "top5_lobbied_members": lobbied,
        "top5_lobbyists": finallobbyist
    }
}

with open(os.path.join(outputt + "/overallStats.json"), "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)
print(outputt)
