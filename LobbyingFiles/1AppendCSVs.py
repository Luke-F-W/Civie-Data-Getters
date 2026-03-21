"""
This script combines multiple 
numbered CSV files into a single CSV.
Once merged, the data is manually 
cleaned to correct minor and rare issues.
Each CSV is numbered (eg, 1.csv, 2.csv), which is what x is
for.
"""
import pandas as pd
import os

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
maincsv = os.path.join(filepathabove, "maincsv.csv") #csv that i append everything to
csvs = os.path.join(filepathabove, "csvlist") #folder with lobbying CSVS
x = 1
#x < 33 as there is 32 CSVs
while x < 33:
    csv = (csvs + "\\" + str(x) + ".csv")
    csvv = pd.read_csv(csv)
    csvv.to_csv(maincsv, mode="a", header=False, index=False)
    print(str(x) + " has been added <-o->")
    x += 1
