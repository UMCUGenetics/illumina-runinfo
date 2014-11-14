import argparse
from xml.dom.minidom import parse

from app import db
from app.models import RunInfo, Platform

#Parse HiSeq
def parse_hiseq(run_parameters):
    print "Hiseq\n"

#Parse MiSeq
#Parse NextSeq

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('platform', choices=['hiseq','miseq','nextseq'], help="Sequencing platform")
    parser.add_argument('paramFile', help="Illumina runParameters.xml file")
    args = parser.parse_args()
    
    # Parse runParameters.xml
    run_parameters = parse(args.paramFile)
    platform = args.platform
    
    if platform == 'hiseq':
	run_info = parse_hiseq(run_parameters)
    #elif platform == 'miseq':
	#run_info = parse_miseq(run_parameters)
    #elif platform == 'nextseq':
	#run_info = parse_nextseq(run_parameters)

    #db.session.add(run_info)
    #db.session.commit()
    
"""
    #if run_parameters.getElementsByTagName('ApplicationName')[0].firstChild.nodeValue == 'MiSeq Control Software':
	platform = 'miseq'
    
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
"""