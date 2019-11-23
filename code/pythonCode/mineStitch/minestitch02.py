# import modules
import sys,io
from os import listdir
from os.path import isfile, join
import codecs
import re
import json
import string
import csv


filenameOne = r"d:\kananovich\personal\OneDrive\Documents\family\jobsAnton\dataIncubator\stage02\myproject\data\scrapped\aux02\dumpFinancialSoupNoCroco20180101-20181101.csv"
filenameTwo = r"d:\kananovich\personal\OneDrive\Documents\family\jobsAnton\dataIncubator\stage02\myproject\data\scrapped\final\dumpFinancialSoupNoCroco20180101-20181101.csv"
path_csv = 

masterList = [] # initialize the list where we store all data collected


with open(fileNameOne, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    iList = list(reader)
    masterList = masterList + iList

with open(fileNameTwo, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    iList = list(reader)
    masterList = masterList + iList

with open(path_csv,'w',encoding='utf-8', newline='') as my_csv:
    data_writer = csv.writer(my_csv)
    for radok in masterList:
        data_writer.writerow(radok)    

print('Dun. The masterfile is saved in ', path_csv)        