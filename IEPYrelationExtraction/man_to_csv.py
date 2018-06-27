#!/usr/bin/python

import csv
import sys

DocName = sys.argv[1]	#grabs the man page name
#splitName = sys.argv[1].split('.')

for i in range(1, len(sys.argv)):
	with open(sys.argv[i], 'r') as f:
		contents = f.readlines()
		
		with open('test.csv', 'wb') as new_file:
			fieldnames = ['document_id', 'document_text']
			csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')	

			csv_writer.writeheader()		
			csv_writer.writerow({'document_id': DocName, 'document_text': contents})
			
