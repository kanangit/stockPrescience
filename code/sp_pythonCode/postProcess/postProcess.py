# import modules

import sys,io
from os import listdir
from os.path import isfile, join
import pandas as pd
import codecs
import re
import json
import string
import csv
import argparse
import numpy as np
import math
import time
import matplotlib
#import matplotlib.pyplot as plt

# function sort a 2D array by the column col
def sort_by_column(inList,col,desc = False):
    if desc == True:
        inList.sort(key = lambda inList: inList[col], reverse = desc)
    elif desc == False:
        inList.sort(key = lambda inList: inList[col])
    return inList

def readRecordList(lFilename):
	recordList = []	
	with open(lFilename, 'r',newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		iniList = list(reader)
	for radok in iniList:
		if len(radok) != 0:
			recordList.append(radok)
	return recordList

def get_dateMean(date_list, data_df, dateName, colName):
    out_list = []
    for date in date_list:
        sub_df = data_df[data_df[dateName] == date]
        sub_df.reset_index(drop = True)
        curMean = sub_df[colName].mean()
        out_list.append([date, curMean])
    return out_list


parser = argparse.ArgumentParser()
parser.add_argument("iniFilePath")
parser.add_argument("tmFilePath")
parser.add_argument("snp500path")
args = parser.parse_args()	

ipath = args.iniFilePath
tmFilePath = args.tmFilePath
snp500FilePath = args.snp500path 

inilist_header = ['atype','date','article text','word_count']

full_df = pd.read_csv(ipath, names = inilist_header, index_col=False)
full_df.head()

tm_df = pd.read_csv(tmFilePath)
tm_df.head()
result_df = pd.concat([full_df, tm_df], axis=1, sort=False)
result_df.head()
print(len(result_df))

set_dates = set(list(result_df['date']))
print(len(set_dates))

l_dates = [str(x) for x in set_dates]
l_dates.sort()
l_dates.pop(len(l_dates)-1)
print(l_dates)


time_list = [[time.mktime(time.strptime(date,'%m/%d/%y')), date] for date in l_dates]
time_list = sort_by_column(time_list,0,desc = False)


d_list = [row[1] for row in time_list]

check_list = get_dateMean(d_list,result_df,'date','V5')
#preparing to plot:
allDates = [matplotlib.dates.epoch2num(time[0]) for time in time_list ]
ytemp = [row[1] for row in check_list]

matplotlib.pyplot.plot_date(allDates, ytemp, '-')
