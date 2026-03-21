"""
on a small amount of rows sometimes a cell in a column
gets split into multiple cells despite needing
to be in 1 cell, these require manual cleaning.
This short script prints which rows require 
cleaning by going through each row and seeing 
if column T or U have data in them, if so it
prints that row.
"""
import csv
import os

file = os.path.abspath(__file__)
filepath = os.path.dirname(file)
filepathabove = os.path.dirname(filepath)
maincsv = os.path.join(filepathabove, "maincsv.csv") #csv to find the messed up rows in

with open(maincsv, 'r', encoding='utf-8') as csvv:
    x = 0
    for row in csv.reader(csvv):
        if len(row) > 19:
            t = row[19]
        else:
            t = ''
        if len(row) > 20:
            u = row[20]
        else:
            u = ''
        if t or u:
            print(x)
        x += 1