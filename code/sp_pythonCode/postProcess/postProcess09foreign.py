# import modules

import matplotlib.dates 
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
#import matplotlib
import matplotlib.pyplot
"""

Purpose: compare the results of Structural topic modelling (STM) of a newspaper articles to
the Stock index price change.
Algorithm:
1. Import the data of STM and calculate STM daily average.
2. Import the SNP price vs time
3. Plot both quantities vs time in the same graph 

"""
#column name of the STM output data we wish to plot:
stm_colname = 'V6'
stm_label = 'Normalized average daily salience of the topic'
snp500_label = 'Normalized SNP 500 close price'
# Title and labels of the output graph
strTitle = 'SNP 500 Price vs. Salience of Foreign Politics in the News in 2018'
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

check_list = get_dateMean(d_list, result_df, 'date', stm_colname)


#preparing to plot:

allDates = [matplotlib.dates.epoch2num(time[0]) for time in time_list ]
ytemp = [row[1] for row in check_list]
print(min(ytemp))
ytempNorm = [(float(perc) - min(ytemp) ) / max(ytemp) for perc in ytemp]
matplotlib.pyplot.plot_date(allDates, ytempNorm, 'ro', label = stm_label)
matplotlib.pyplot.title(strTitle)
matplotlib.pyplot.xlabel('Date')
##matplotlib.pyplot.show()

snp500_df = pd.read_csv(snp500FilePath)
snp500_df.head()

epochStart = time.mktime(time.strptime('2018-01-01','%Y-%m-%d'))
epochEnd =time.mktime(time.strptime('2018-12-31','%Y-%m-%d')) 

l_snp_dates = list(snp500_df['Date'])

epoch_list = [time.mktime(time.strptime(date,'%Y-%m-%d')) for date in l_snp_dates]

epoch_df = pd.DataFrame(epoch_list, columns = ['Epoch'])
snp500_df = pd.concat([snp500_df, epoch_df], axis=1, sort=False)
snp500_2018_df = snp500_df[snp500_df['Epoch'] >= epochStart]
snp500_2018_df.reset_index(drop = True)
snp500_2018_df = snp500_df[snp500_df['Epoch'] <= epochEnd]
snp500_2018_df.reset_index(drop = True)

#Preparing to plot

l_dates = list(snp500_2018_df['Epoch'])
l_snp = list(snp500_2018_df['Close'])
#normalize against maximum:
l_snpNorm = [(float(price)-float(min(l_snp))) / float(max(l_snp) - min(l_snp)) for price in l_snp]
allDatesSnp = [matplotlib.dates.epoch2num(time) for time in l_dates ]

matplotlib.pyplot.plot_date(allDatesSnp, l_snpNorm, '-', label = snp500_label)
matplotlib.pyplot.legend(loc= 'upper left')
matplotlib.pyplot.show()

for huj in l_dates:
	print(time.gmtime(huj))