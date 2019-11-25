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
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument("iniFilePath")
parser.add_argument("tmFilePath")
parser.add_argument("userWPath")
args = parser.parse_args()	

print('reading the file ',args.userRPath)
rList = readRecordList(args.userRPath)

with open(args.userWPath,'w',encoding='utf-8', newline='') as my_csv:
    data_writer = csv.writer(my_csv)
    for radok in rList:
    	if len(radok) != 0:    		
    		data_writer.writerow(radok)    

print('Dun. The masterfile is saved in ', args.userWPath)