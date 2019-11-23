# import modules
import sys,io
from os import listdir
from os.path import isfile, join
import codecs
import re
import json
import string
import csv
import argparse


#the function reads the paragraph records from the given .csv file
#and deletes empty rows if there are any
def readRecordList(lFilename):
	recordList = []	
	with open(lFilename, 'r',newline='', encoding='utf-8') as f:
		reader = csv.reader(f)
		iniList = list(reader)
	for radok in iniList:
		if len(radok) != 0:
			recordList.append(radok)
	return recordList


#the function deletes metionings the origin country of the paragraph
# in the text of the paragraph
def remCroco(record):
	recDeleted = record	
	match = r'([^a-zA-Z|\'|\-])'
	recDeleted[5] = re.sub(match,' ',record[5])			
	recDeleted[5] = re.sub('    ',' ',record[5])
	recDeleted[5] = re.sub('   ',' ',record[5])
	recDeleted[5] = re.sub('  ',' ',record[5])
	return recDeleted	

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,'cp437','backslashreplace')

parser = argparse.ArgumentParser()
parser.add_argument("userRPath")
parser.add_argument("userWPath")
args = parser.parse_args()	

print('doing the file ',args.userRPath)
rList = readRecordList(args.userRPath)
for r in rList:
	r = remCroco(r)

with open(args.userWPath,'w',encoding='utf-8', newline='') as my_csv:
    data_writer = csv.writer(my_csv)
    for radok in rList:
    	if len(radok) != 0:    		
    		data_writer.writerow(radok)    

print('Dun. The masterfile is saved in ', args.userWPath)