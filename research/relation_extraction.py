#!/usr/bin/python

import sys
import nltk
import re
from nltk.tree import Tree
import pprint
from collections import defaultdict

splitName = sys.argv[1].split(".")
TPList = []
IList = []
result = []

def extractEntities(document):
	contents = iter(document)
	#sometimes the man page name doesn't match up with the name in the man page....
	reName = re.sub("\d", "", splitName[0])		
	
	reg = r"""(.*""" + re.escape(reName) + r"""\(.*)"""
	reg2 = r'".*?"|(\w+)'
	pattern = re.compile(reg)
	pattern2 = re.compile(reg2, re.MULTILINE)
	ColonDet = False
	BIDet = False

	for line in contents:
		line = line.strip()
		#splits first string sentence
		splitLine = line.split(' ',1)
		if (line[-1:] == ':'):
			ColonDet = True
		if (BIDet == True):
			BIDet = False
			if (line.startswith('.', 0, 1)):
				None
			else:
				m2 = pattern2.finditer(line)
				for match in m2:
					if match.group(1):
						seen = set(IList)
						if match.group(1) not in seen:
							seen.add(match.group(1))
							IList.append(match.group(1))
						#end if
					#end if
				#end for
			#end if
		if (splitLine[0] == '.BI'):
			m = pattern.search(splitLine[1])
			if m is not None:
				inner = m.group(1)
				m2 = pattern2.finditer(inner)
				for match in m2:
					if match.group(1):
						seen = set(IList)
						#ck for duplicates
						if match.group(1) not in seen:
							seen.add(match.group(1))
							IList.append(match.group(1))	
						#end if
					#end if
				#end for
				BIDet = True
			#end if
		if (splitLine[0] == '.TP'):
			line1 = next(contents)
			line1 = line1.strip() 
			#sys.stdout.write(line1)	
			splitLine1 = line1.split(" ")
			if (splitLine1[0] == '.B' or splitLine1[0] == '.BR'):
				ColonDet = False
				seen = set(TPList)
				#ck for duplicates
				if splitLine1[1] not in seen:
					seen.add(splitLine1[1])	
					TPList.append(splitLine1[1])
					if (len(splitLine1) > 2):
						if (splitLine1[3] == 'or'):
							if splitLine1[5] not in seen:
								seen.add(splitLine1[5])
								TPList.append(splitLine1[5])
		#end if .TP
		#change 'BR' to 'B' for different results
		if (splitLine[0] == '.BR' and ColonDet == True):
			ColonDet = False
			seen = set(TPList)
			if splitLine[1] not in seen:
				seen.add(splitLine[1])
				TPList.append(splitLine[1])
		#end If .B			
	#end contents for loop
#end extractEntities

#makes entity an interable list
def tag_extraction(words):
	outer = re.compile("\[\[(.+)\]\]")
	m = outer.search(str(words))
	if(outer.search(str(words))):
		inner_str = m.group(1)
		innerre = re.compile("\('([^']+)', '([^']+)'\)")
		results = innerre.findall(inner_str)
		return results
	else:
		print "Error!"
		sys.exit() 
#end tag_extraction

def stack_tokenize(popped):
	previous = ''
	innerStack = []
	Radded = False
		
	sentences = nltk.sent_tokenize(popped)	
	words = [nltk.word_tokenize(sent) for sent in sentences]
	for x in words:
		for w in x:
			for (e,c) in entities_chunk:
				if(w == e and (c == 'B-NP' or c == 'I-NP')):	
					innerStack.append((w,c))				
				#end if
			#end for
			if(w == ':'):
				#note the colon is not added
				ICheck = False
				for item in I_tagged:
					if(item == previous):
						ICheck = True
				#end for
				if(ICheck == True): 
					innerStack.append(('are', 'R'))
				#limitation?
				elif (re.match("(follow[a-zA-Z]*)|(Follow[a-zA-Z]*)", previous)):
                                        innerStack.append((previous,'R'))
                                elif (re.match("(include[a-zA-Z]*)|(Include[a-zA-Z]*)", previous)):
                                        innerStack.append((previous,'R'))
                                elif (re.match("(meaning[a-zA-Z]*)|(Meaning[a-zA-Z]*)", previous)):
                                        innerStack.append((previous,'R'))
				#end if	
			previous = w							
		#end for
	#end for

	Beginning = False
	RelationFound = False
	relation = ''
	entity1 = []
	entity2 = [] 
	while(Beginning == False):
		if not innerStack:
			Beginning = True
		else:
			inPop = innerStack.pop()
			if(inPop[1] == 'I-NP'):
				seen = set(entity2)
				if inPop[0] not in seen:
					seen.add(inPop[0])
					entity2.append(inPop[0])
				#end if
			elif(inPop[1] == 'R'):
				if entity2:
					RelationFound = True
					relation = inPop[0]
			elif(inPop[1] == 'B-NP' and RelationFound == True):
				reldict = defaultdict(str)
				reldict['entity1'] = inPop[0]
				reldict['relation'] =  relation
				reldict['entity2'] = ' '.join(word for word in entity2)
				result.append(reldict)
				relation = '' 
				del entity2[:]	
				RelationFound = False
			#end if
		#end check
	#end while
#end stack_tokenize

#main()
if (len(sys.argv) != 3):
	print "Incorrect number of inputs!" 
else:
	with open(sys.argv[1], 'r') as f:
		contents = f.readlines()
		extractEntities(contents)
		
	with open(sys.argv[2],'r') as f2:
		ManDoc = f2.readlines()

		#TPentity labelling
		TPstring = []
		TP_tagged = []
		TPstring.append(' '.join(word for word in TPList))
		TPwords = [nltk.word_tokenize(sent) for sent in TPstring]
		TP_tag = [nltk.pos_tag(word) for word in TPwords]
		TP_List = tag_extraction(TP_tag)
		#sometimes NLTK will tag words differently so be careful. Might have to set "t == 'NPP' or t == 'NN'".
		for (w,t) in TP_List:
			if(t == 'NNP'):
				seen = set(TP_tagged)
				#ck for duplicates
				if w not in seen:
					seen.add(w)
					TP_tagged.append(w)
		#end for
		
		#Ientity labeling
		Istring = []
		I_tagged = []
		#need a nonreference copy otherwise it will end up in infinite loop
		IListCopy = IList[:]
		#we are now adding variations of Ientity to list
		for words in IListCopy:
			if (words.endswith('s')):
				#strips the last letter of words
				IList.append(words[:-1])
			else:
				IList.append(words+'s')
		#end for
		Istring.append(' '.join(word for word in IList))
		Iwords = [nltk.word_tokenize(sent) for sent in Istring]
		I_tag = [nltk.pos_tag(word) for word in Iwords]
		I_List = tag_extraction(I_tag)
		for (w,t) in I_List:
			I_tagged.append(w)
		#end for
		
		TP_chunk = [(w,'I-NP') for w in TP_tagged]
		I_chunk = [(w,'B-NP') for w in I_tagged]
		entities_chunk = TP_chunk + I_chunk	
			
		#relation dictionary
		outerStack = [] 	 
		prevCount = -1
		count = -1
		SavedCount = []	
		for line in ManDoc:
			if (len(line.strip()) != 0):
				count = len(line) - len(line.lstrip(' '))
				line1 = line.decode('utf-8').strip()
				if (prevCount == -1):
					prevCount = count
				if (prevCount == count): 
					if outerStack:
						x = outerStack.pop() 
						joined = x + ' ' + line1
						outerStack.append(joined) 
					else:
						outerStack.append(line1)
				elif (prevCount < count):
					outerStack.append(line1)
					SavedCount.append(prevCount)
				elif (prevCount > count):
					stop = False
					while(stop == False):
						savePopped = SavedCount.pop()
						if(savePopped == count):
							popped = outerStack.pop()
							x = outerStack.pop()
							joined = x + ' ' + line1  
							outerStack.append(joined) 
							stack_tokenize(popped)
							stop = True					
						elif(savePopped > count):
							popped = outerStack.pop()
							stack_tokenize(popped)
						else:
							popped = outerStack.pop()
							stack_tokenize(popped)
							outerStack.append(line1)
							SavedCount.append(savePopped)
							stop = True
						#end if
					#end while		
				#end if
			#end if
			prevCount = count
		#end for		
		
		out = open(splitName[0]+'Relation.txt','a')
		for r in result:
			finalResult = (r['entity1']+' '+r['relation']+' '+r['entity2'])
			#print finalResult
			if(r['entity2']):
				out.write(finalResult+'\n')
		#end for
		out.close()
