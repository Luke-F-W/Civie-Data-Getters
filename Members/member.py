"""
This gets and makes a JSON of members currently in the dail & seanad, saves their
membercode, name, party code and image.
"""

import requests
import json
import os

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
out = os.path.join(filepathabove, "Database", "json-members")#save to here

#1 url is for the dail and 1 is for the seanad
url1 = "https://api.oireachtas.ie/v1/members?chamber=seanad&house_no=27&skip=0&limit=2000"
url2 = "https://api.oireachtas.ie/v1/members?chamber=dail&house_no=34&skip=0&limit=2000"

def member(json1):
    memberstuff= []
    for entry in json1:
        memberr = entry.get("member")
        memberstuff.append({
            "memberCode": memberr.get("memberCode"),
            "fullName": memberr.get("fullName"),
            "party_code": memberr.get("memberships")[0]
                              .get("membership")
                              .get("parties")[0]
                              
                              .get("party")
                              .get("partyCode"),
            "image": "https://data.oireachtas.ie/ie/oireachtas/member/id/" + memberr.get("memberCode") + "/image/large"
        })
    return memberstuff

dail = requests.get(url2)
seanad = requests.get(url1)

dail = dail.json()
seanad = seanad.json()

dresults = dail["results"]
sresults= seanad["results"]

dail = member(dresults)
seanad = member(sresults)

membersfinal = dail + seanad

with open(os.path.join(out, "Members.json"), "w", encoding="utf-8") as f:
    json.dump(membersfinal, f, indent=2, ensure_ascii=False)
print("done <-o->")
