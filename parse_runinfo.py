#!/usr/bin/python

import os
import argparse
import sys
from xml.dom.minidom import parse


parser = argparse.ArgumentParser()
parser.add_argument("-r","--run", help="Illumina run root directory", required=False)
parser.add_argument("-p","--paramfile", help="Illumina runParameters.xml file", required=False)
args = parser.parse_args()
NSfields = ['ApplicationName','RunID','ExperimentName', 'Chemistry', 'FlowCellSerial','RunStartDate','IsPairedEnd','PlannedRead1Cycles','PlannedRead2Cycles', 'PlannedIndex1ReadCycles', 'PlannedIndex2ReadCycles']
#HSfields = ['RunID','ExperimentName', 'Chemistry', 'LibraryID', 'RunNumber', 'FlowCellSerial','RunStartDate','IsPairedEnd','PlannedRead1Cycles','PlannedRead2Cycles', 'PlannedIndex1ReadCycles', 'PlannedIndex2ReadCycles', 'ApplicationName']
HSfields = ['ApplicationName','RunID','ExperimentName','RunMode', 'Barcode','RunStartDate','PairEndFC','Read1','Read2', 'IndexRead1','IndexRead2','Pe' ]
MSfields = ['ApplicationName','RunID','ExperimentName', 'Barcode','RunStartDate']

result = ''


runName = args.run
fileName = args.paramfile


if fileName:
    runParameters = parse(fileName)
else:
    if not os.path.isdir(args.run):
	print args.run+" is not a valid directory"
	sys.exit(1)
    if runName.endswith('/'):
	runName = runName[:-1]
	runName = os.path.split(runName)[1]
    if os.path.isfile(args.run+"/RunParameters.xml"):
	runParameters = parse(args.run+"/RunParameters.xml")
    elif os.path.isfile(args.run+"/runParameters.xml"):
	runParameters = parse(args.run+"/runParameters.xml")
    else:
	print args.run+"/(r|R)unParameters.xml does not exist "
	sys.exit(1)


if runParameters.getElementsByTagName('ApplicationName')[0].firstChild.nodeValue == 'MiSeq Control Software':
    #typically miSeq format
    for f in MSfields:
	if runParameters.getElementsByTagName(f):
	    result += runParameters.getElementsByTagName(f)[0].firstChild.nodeValue + "\t"
	else:
	    result += "NA" + "\t"

    #get readlengths for reads
    	
    read1 = runParameters.getElementsByTagName('RunInfoRead')[0].getAttribute('NumCycles') + "\t"
    if runParameters.getElementsByTagName('RunInfoRead')[1].getAttribute('IsIndexedRead') == 'N':
        read2 = runParameters.getElementsByTagName('RunInfoRead')[1].getAttribute('NumCycles') + "\t"
        PE = "true" + "\t"
        index1 = "NA" + "\t"
        index2 = "NA" + "\t"
    elif runParameters.getElementsByTagName('RunInfoRead')[1].getAttribute('IsIndexedRead') == 'Y':
        index1 = runParameters.getElementsByTagName('RunInfoRead')[1].getAttribute('NumCycles') + "\t"
        if runParameters.getElementsByTagName('RunInfoRead')[2].getAttribute('IsIndexedRead') == 'Y':
    	    index2 = runParameters.getElementsByTagName('RunInfoRead')[2].getAttribute('NumCycles') + "\t"
	    read2 = runParameters.getElementsByTagName('RunInfoRead')[3].getAttribute('NumCycles') + "\t"
	    PE = "true"+ "\t"
	else:
	    index2 = "NA" + "\t"
	    read2 = runParameters.getElementsByTagName('RunInfoRead')[2].getAttribute('NumCycles') + "\t"
	    PE = "true" + "\t"
	
	result += PE
	result += read1
	result += read2
	result += index1
	result += index2
	
	result += runParameters.getElementsByTagName('Chemistry')[0].firstChild.nodeValue + "\t"
	print result
	
elif runParameters.getElementsByTagName('ApplicationName')[0].firstChild.nodeValue == 'HiSeq Control Software':
    #typically HiSeq format
    result = ''
    for f in HSfields:
	if runParameters.getElementsByTagName(f):
    	    result += runParameters.getElementsByTagName(f)[0].firstChild.nodeValue + "\t"
    	else:
	    result += "NA" + "\t"
    print result
elif runParameters.getElementsByTagName('ApplicationName')[0].firstChild.nodeValue == 'NextSeq Control Software':
    #typically NextSeq format
    for f in NSfields:
	if runParameters.getElementsByTagName(f):
	    result += runParameters.getElementsByTagName(f)[0].firstChild.nodeValue + "\t"
        else:
	    result += "NA" + "\t"
    print result + "\tNA"


