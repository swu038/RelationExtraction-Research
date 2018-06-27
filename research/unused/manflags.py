#!/usr/bin/python

import sys
import nltk
import re
from nltk.sem import extract_rels,rtuple

splitName = sys.argv[1].split(".")   #grabs the man page name
TPList = []
IList = []

for i in range(1, len(sys.argv)):
	with open(sys.argv[i], 'r') as f:
		contents = f.readlines()
		icontents = iter(contents)			
		
		for line in icontents:
			line = line.strip()
			#splits first string sentence
			splitLine = line.split(' ',1)
			if (splitLine[0] == '.TP'):
				line1 = next(icontents)
				line1 = line1.strip() 
				#sys.stdout.write(line1)	
				splitLine1 = line1.split(" ")
				if (splitLine1[0] == '.B' or splitLine1[0] == '.BR'):
					seen = set(TPList)
					#ck for duplicates
					if splitLine1[1] not in seen:
						seen.add(splitLine1[1])	
						TPList.append(splitLine1[1])
			#end if .TP
			if (splitLine[0] == '.I'):
				#sys.stdout.write(splitLine[1]+'\n')
				seen = set(IList)
				#ck for duplicates
				if splitLine[1] not in seen:
					seen.add(splitLine[1])
					IList.append(splitLine[1])
			#end if .I
			if (splitLine[0] == '.B'):
				seen = set(TPList)
				if splitLine[1] not in seen:
					seen.add(splitLine[1])
					TPList.append(splitLine[1])
			#end If .B			
		#end icontents for loop
#end sys.argv for loop

out = open(splitName[0]+'TPEntities.txt','a')   #note the append
#out.write('Special Format: .TP and .B or .BR'+'\n')
for i in range(len(TPList)):
	out.write(TPList[i]+'\n')
#end TPList for loop
out.close()

out1 = open(splitName[0]+'IEntities.txt','a')	#note the append
#out1.write('Special Format: .I'+'\n')
for i in range(len(IList)):
	out1.write(IList[i]+'\n')
#end IList for loop

out1.close()

