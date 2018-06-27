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
		#end if .TP
		#change here
		if (splitLine[0] == '.B' and ColonDet == True):
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

#main()
for i in range(1, len(sys.argv)):
	with open(sys.argv[i], 'r') as f:
		doc = f.read()
		f.seek(0)	#starts the file anew
		contents = f.readlines()
		extractEntities(contents)
			
		#TPentity labelling
		TPstring = []
		TP_tagged = []
		TPstring.append(' '.join(word for word in TPList))
		TPwords = [nltk.word_tokenize(sent) for sent in TPstring]
		TP_tag = [nltk.pos_tag(word) for word in TPwords]
		TP_List = tag_extraction(TP_tag)
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
		
		#document labeling
		#look for blank lines and replace with .RE	
		reg3 = re.compile(r'^\s*$', re.MULTILINE)
		docRE = reg3.sub('.RE', doc) 
			
		sentences = nltk.sent_tokenize(docRE)
		words = [nltk.word_tokenize(sent) for sent in sentences]
		tags = [nltk.pos_tag(word) for word in words]	
		List_tags = tag_extraction(tags)
		List_words = [w for (w,t) in List_tags]
	
		Doctags = [] 
		EntityExist = False
		PrevEntityI = False
		previous = ''
		for w in List_words:
			for (e,c) in entities_chunk:
				if(w == e and c == 'B-NP'):
					Doctags.append((w,c))
					EntityExist = True
					PrevEntityI = True
				elif(w == e and c == 'B-NP' and
					PrevEntityI == True):
					Doctags.append((w,c))
					EntityExist = True
				elif(w == e and c == 'I-NP'):
					Doctags.append((w,c))
					EntityExist = True
					PrevEntityI = False
				#end if
			#end for
			if(w == ':' and EntityExist == False):
				#note the colon is not added
				ICheck = False
				for x in I_tagged:
					if(x == previous):
						ICheck = True
				#end for
				if (ICheck == True):
					Doctags.append(('are','R'))
				#limitation? Fix here
				elif(re.match('http|Re|exception|\d|Subject|Haardt|replies|Newsgroups|into|\W', previous)):
					None
				else:
					Doctags.pop()
					Doctags.append((previous, 'R'))
				#end if
				PrevEnttiyI = False
			elif(EntityExist == False):		
				Doctags.append((w,'O'))
				PrevEntityI = False
		 	#end if
			EntityExist = False
			previous = w
		#end for
	 
		#out2 = open('format.txt','a')
		#for (w,c) in Doctags:
			#out2.write(str((w,c))+'\n')
		#out2.close()
	
		#relation dictionary	
		stack = []
		result = []
		Radded = False
		for (w,c) in Doctags:
			if(c == 'B-NP'):
				stack.append((w,c))
			elif(c == 'R'):
				stack.append((w,c))
				Radded = True
			elif(c == 'I-NP'):
				stack.append((w,c))
			elif(w == '.RE' and Radded == True):
				Beginning = False
				RelationFound = False
				reldict = defaultdict(str)
				entity1 = []
				entity2 = []
				while(Beginning == False): 
					if not stack:
						Beginning = True
					else:
						current = stack.pop()
						if(current[1] == 'I-NP'):
							seen = set(entity2)
							if current[0] not in seen:
								seen.add(current[0])
								entity2.append(current[0])
						elif(current[1] == 'R'):
							RelationFound = True
							reldict['relation'] = current[0]
						elif(current[1] == 'B-NP' and RelationFound == True):
							Beginning = True
							reldict['entity1'] = current[0]
							reldict['entity2'] = ' '.join(word for word in entity2)
							result.append(reldict)		
						#end if
					#end check
				#end while		
		#end for
		
		out = open(splitName[0]+'RelationB2.txt','a')
		for r in result:
			finalResult = (r['entity1']+' '+r['relation']+' '+r['entity2'])
			#print finalResult
			if(r['entity2']):
				out.write(finalResult+'\n')
		#end for
		out.close()
