#!/usr/bin/python

import sys

#3 entities version!
splitName = sys.argv[1].split(".")   #grabs the man page name
TPList = []
IList = []
BList = []
relationList = []

for i in range(1, len(sys.argv)):
	with open(sys.argv[i], 'r') as f:
		contents = f.readlines()
		icontents = iter(contents)
		icontents1 = iter(contents)			

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
				seen1 = set(BList)
				if splitLine[1] not in seen:
					seen.add(splitLine[1])
					if splitLine[1] not in seen1:
						seen1.add(splitLine[1])
						BList.append(splitLine[1])
			#end If .B				
		#end icontents for loop

		#extract relations
		for line in icontents1:
			line = line.strip()
			#for i in range(len(IList)):
			if line.find(IList[1]) >= 0:
				relation = line.split(IList[1])
				#removes spaces in list
				relation = [x.strip(' ') for x in relation] 
				if (relation[1] != ''):
					print relation
					if (relation[1] != '.I'):
					   
		
#end sys.argv for loop

out = open(splitName[0]+'Flags.txt','a')   #note the append
out.write('Special Format: .TP and .B or .BR'+'\n')
for i in range(len(TPList)):
	out.write(TPList[i]+'\n')
#end TPList for loop
out.write('\n'+'Special Format: .I'+'\n')
for i in range(len(IList)):
	out.write(IList[i]+'\n')
#end IList for loop
out.write('\n'+'Special Format: .B'+'\n')
for i in range(len(BList)):
	out.write(BList[i]+'\n')
#end BList for loop
out.close()

#for i in range(len(TPList)):
	#sys.stdout.write(TPList[i])
