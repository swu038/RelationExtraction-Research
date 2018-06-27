#!/usr/bin/python

import sys


#no list version!
splitName = sys.argv[1].split(".")   #grabs the man page name

for i in range(1, len(sys.argv)):
	with open(sys.argv[i], 'r') as f:
		contents = f.readlines()
		icontents = iter(contents)
		icontents1 = iter(contents)		

		out = open(splitName[0]+'Flags.txt','a')   #note the append
		out.write('Special Format: .TP and .B or .BR \n')	

		for line in icontents:
			line = line.strip()
			if (line == '.TP'):
				line1 = next(icontents)
				line1 = line1.strip() 
				#sys.stdout.write(line1)	
				splitLine = line1.split(" ")
				if (splitLine[0] == '.B' or '.BR'):
					#sys.stdout.write(splitLine[1]+'\n')
					out = open(splitName[0]+'Flags.txt','a')   #note the append	
					out.write(splitLine[1]+'\n')
					out.close()
		#end for loop

		out = open(splitName[0]+'Flags.txt','a')   #note the append
		out.write('\nSpecial Format: .I \n')	
		
		for line in icontents1:
			line = line.strip()
			splitLine = line.split(' ',1)
			if (splitLine[0] == '.I'):
				#sys.stdout.write(splitLine[1]+'\n')
				out = open(splitName[0]+'Flags.txt','a')
				out.write(splitLine[1]+'\n')
				out.close()
		#end for loop
