"""
This removes records without a membercode, significantly
reducing the size of the csv.
"""
import pandas as pd
import os
file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
maincsv = os.path.join(filepathabove, "maincsv.csv") #csv to remove rows lacking membercode in

csvv = pd.read_csv(maincsv)
rows = csvv.values
rows = rows.tolist()

filtered = []
for row in rows:
    #ignore the record if membercode is empty, else add to filtered 
    if pd.isna(row[19]):
        continue
    else:
        filtered.append(row)

#make csv
csvv = pd.DataFrame(filtered)
csvv.to_csv(maincsv, index=False, header=False)
print("finished!! <-o->")
