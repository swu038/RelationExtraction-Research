#!/usr/bin/python

import sys
import nltk
import re
import pprint

splitName = sys.argv[1].split(".")   #grabs the man page name
TPList = []
IList = []
EntityList = []
Training_set = []

def extractEntities(document):
	contents = iter(document)			
		
	for line in contents:
		line = line.strip()
		#splits first string sentence
		splitLine = line.split(' ',1)
		if (splitLine[0] == '.TP'):
			line1 = next(contents)
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
	#end contents for loop
#end extractEntities

def ie_preprocess(document):
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	return sentences
#end ie_preprocess

def tag_entities(List):
	sent_entities = [[(entity) for entity in List]]		#double brackets for format??
	tagged_entities = [nltk.pos_tag(sent) for sent in sent_entities]
	outer = re.compile("\[\[(.+)\]\]")
	m = outer.search(str(tagged_entities))
	inner_str = m.group(1)
	innerre = re.compile("\('([^']+)', '([^']+)'\)")
	results = innerre.findall(inner_str)
	return results
#end document_features

#main()
for i in range(1, len(sys.argv)):
	with open(sys.argv[i], 'r') as f:
		raw = f.read()
		f.seek(0)	#starts the file anew
		contents = f.readlines()
		extractEntities(contents)

		#labeled_entities = ([(entity, 'TP') for entity in TPList] + [(entity, 'I') for entity in IList])	
	
		TP_tagged = tag_entities(TPList)
		I_tagged = tag_entities(IList)

		out = open(splitName[0]+'Trained.txt','a')	#note the append			
		conlltags = [(w,t,'I-TP') for (w,t) in TP_tagged]
		test = nltk.chunk.conlltags2tree(conlltags)
		tagged = [[((w,t),c) for (w,t,c) in nltk.chunk.tree2conlltags(sent)] for sent in test]
		print test
		#for x,y in TP_tagged:
			#out.write("%s %s I-TP\n" % (x,y))
		#for x,y in I_tagged:
			#out.write("%s %s B-I\n" % (x,y))	
#end sys.argv for loop
