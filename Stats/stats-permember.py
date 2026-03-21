"""
This creates stats per member based on their political activities, it gets the
vote count (how many ta, nil and staon votes) question category count and lobbyists along with
how many times they have lobbied the member in question, it also gets the tally for each
of the 5 sections (lobbying, questions, votes, debates and bills). Unlike most other scripts
in the data getters section, membercodes are obtained VIA a json instead of a txt file.
This is because members.json was a last minute change, and members info were originally
stored on a CSV file.
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
billss = os.path.join(filepathabove, "Database", "json-bills")
lobbyy = os.path.join(filepathabove, "Database", "json-lobbying")
questionss = os.path.join(filepathabove, "Database", "json-questions")
votess = os.path.join(filepathabove, "Database", "json-votes")
debatess = os.path.join(filepathabove, "Database", "json-debates")
memberss = os.path.join(filepathabove, "Database", "json-members", "members.json")
outputt = os.path.join(filepathabove, "Database", "json-stats")

#normalise names
def normalisename(name):
    name = unicodedata.normalize('NFKD', name)
    name = name.encode('ASCII', 'ignore')
    name = name.decode('utf-8')
    name = re.sub('[^a-zA-Z]', '', name)
    return name.lower()

def findfile(directory, membercode):
    for filename in os.listdir(directory):
        if membercode in filename:
            return os.path.join(directory, filename)
    return None

membercodes = []

#load membercodes 
with open(memberss, "r", encoding="utf-8") as f:
    memberdata = json.load(f)
    for member in memberdata:
        toappend = member["memberCode"]

        membercodes.append(toappend)

for membercode in membercodes:
    combined = {
        "stats": {
            "member_code": membercode,
            "votes": {},
            "questions": {},
            "lobbying": {},
            "record_counts": {
                "lobbying_records": 0,
                "question_records": 0,
                "vote_records": 0,
                "debate_records": 0,
                "bill_records": 0
            }
        }
    }
    
    #prepare lobbying data
    lobby = findfile(lobbyy, membercode)
    if lobby:
        with open(lobby, "r", encoding="utf-8") as f:
            data = json.load(f)
            combined["stats"]["record_counts"]["lobbying_records"] = len(data)

            lobbylist = []
            for lobbyist in data:
                name = lobbyist["Lobbyist Name"]
                name = normalisename(name)
                lobbylist.append(name)
            count = Counter(lobbylist)
            combined["stats"]["lobbying"] = dict(count)
    
    #prepare question data 
    questions = findfile(questionss, membercode)
    if questions:
        with open(questions, "r", encoding="utf-8") as f:
            data = json.load(f)
            questioncount =data["head"]["counts"]["resultCount"]
            combined["stats"]["record_counts"]["question_records"] = questioncount


            categories = []
            records = data["results"]
            for record in records:
                name = record["question"]["to"]["showAs"]
                toappend = normalisename(name)
                categories.append(toappend)
            count = Counter(categories)
            combined["stats"]["questions"] = dict(count)
    
    #prepare vote data
    votes = findfile(votess, membercode)
    if votes:
        with open(votes, "r", encoding="utf-8") as f:
            data = json.load(f)
            votecount = data["head"]["counts"]["resultCount"]
            combined["stats"]["record_counts"]["vote_records"] = votecount
            categories = []
            records = data["results"]
            for record in records:
                name = record["division"]["memberTally"]["showAs"]
                toappend = normalisename(name)

                categories.append(toappend)

            count = Counter(categories)
            combined["stats"]["votes"] = dict(count)

    #get debate count
    debates = findfile(debatess, membercode)
    if debates:
        with open(debates, "r", encoding="utf-8") as f:
            data = json.load(f)
            debatecount = data["head"]["counts"]["resultCount"]
            combined["stats"]["record_counts"]["debate_records"] = debatecount
    
    #get bill count
    bills = findfile(billss, membercode)
    if bills:
        with open(bills, "r", encoding="utf-8") as f:
            data = json.load(f)
            billcount = data["head"]["counts"]["resultCount"]
            combined["stats"]["record_counts"]["bill_records"] = billcount

    #save stats
    finaloutput = os.path.join(outputt, membercode + ".json")
    with open(finaloutput, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)
    
    print(membercode)
