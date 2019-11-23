# import modules
import sys,io
from os import listdir
from os.path import isfile, join
import codecs
import re
import json
import string
import csv

wd = r'd:\kananovich\personal\OneDrive\Documents\family\jobsAnton\dataIncubator\stage02\myproject\data\scrapped\aux02'
path_csv = r'd:\kananovich\personal\OneDrive\Documents\family\jobsAnton\dataIncubator\stage02\myproject\data\scrapped\final\dumpFinancial2018.csv'

allfilenames = [f for f in listdir(wd) if isfile(join(wd, f))] # get filenames of all files in the wd

masterList = [] # initialize the list where we store all data collected
for lfilename in allfilenames:
	print('doing the file ',lfilename)
	with open(wd + lfilename, 'r', newline='') as f:
		reader = csv.reader(f)
		iList = list(reader)
		masterList = masterList + iList

with open(path_csv,'w',encoding='utf-8', newline='') as my_csv:
    data_writer = csv.writer(my_csv)
    for radok in masterList:
        data_writer.writerow(radok)    

print('Dun. The masterfile is saved in ', path_csv)        