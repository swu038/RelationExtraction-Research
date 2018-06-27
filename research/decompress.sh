#!/bin/bash
#How to decompress man pages: 

Page=$1
if [ -e /usr/share/man/man2/${Page}.2.gz ]; then
	gzip -d -c /usr/share/man/man2/${Page}.2.gz > ${Page}.txt
	man 2 ${Page} > ${Page}Output.txt
else
	echo file does not exist.
fi
