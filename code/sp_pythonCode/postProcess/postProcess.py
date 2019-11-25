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

parser = argparse.ArgumentParser()
parser.add_argument("iniFilePath")
parser.add_argument("tmFilePath")
parser.add_argument("snp500path")
args = parser.parse_args()	

ipath = args.userRPath
tmFilePath = args.tmFilePath
snp500FilePath = args.snp500path 

inilist_header = ['atype','date','article text','word_count']

full_df = pd.read_csv(ipath, names = inilist_header, index_col=False)
full_df.head()