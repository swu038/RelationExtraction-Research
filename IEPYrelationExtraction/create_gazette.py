#!/usr/bin/python

import sys
import csv

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
			if (line == '.TP'):
				line1 = next(icontents)
				line1 = line1.strip() 
				#sys.stdout.write(line1)	
				splitLine1 = line1.split(" ")
				if (splitLine1[0] == '.B' or '.BR'):
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

with open(splitName[0]+'.csv','wb') as new_file:   #note the append
	fieldnames = ['literal', 'class']
	csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
	
	csv_writer.writeheader()
	for i in range(len(TPList)):
		csv_writer.writerow({'literal': TPList[i], 'class': '.TP.B.BR'})
	#end TPList for loop
	for i in range(len(IList)):
		csv_writer.writerow({'literal': IList[i], 'class': '.I'})
	#end IList for loop


