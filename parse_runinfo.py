import argparse
from xml.dom.minidom import parse

from app import db
from app.models import RunInfo, Platform

### Use zip?


#get_firstChild_value
def get_firstChild_value(run_param, tag):
    return

#Parse HiSeq
def parse_hiseq(run_params):
    run_id = run_params.getElementsByTagName('RunID')[0].firstChild.nodeValue
    experiment_name = run_params.getElementsByTagName('ExperimentName')[0].firstChild.nodeValue

    run_mode = run_params.getElementsByTagName('')[0].firstChild.nodeValue
    barcode = run_params.getElementsByTagName('')[0].firstChild.nodeValue
    run_start_date = run_params.getElementsByTagName('')[0].firstChild.nodeValue
    pair_end_fc = run_params.getElementsByTagName('')[0].firstChild.nodeValue
    read_1 = run_params.getElementsByTagName('')[0].firstChild.nodeValue
    read_2 = run_params.getElementsByTagName('')[0].firstChild.nodeValue
    index_read_1 = run_params.getElementsByTagName('')[0].firstChild.nodeValue
    index_read_2 = run_params.getElementsByTagName('')[0].firstChild.nodeValue
    pe = run_params.getElementsByTagName('')[0].firstChild.nodeValue

    HSfields = ['RunMode', 'Barcode','RunStartDate','PairEndFC','Read1','Read2', 'IndexRead1','IndexRead2','Pe' ]



    #run_info = RunInfo(run_id, experiment_name)

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
    HSfields = ['ApplicationName','RunID','ExperimentName','RunMode', 'Barcode','RunStartDate','PairEndFC','Read1','Read2', 'IndexRead1','IndexRead2','Pe' ]
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
