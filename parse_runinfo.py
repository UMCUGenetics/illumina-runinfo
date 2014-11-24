import argparse
import datetime
from xml.dom.minidom import parse


from app import db
from app.models import RunInfo, Platform

### Use zip?


#get_firstChild_value
def get_firstChild_value(run_params, tag):
    return run_params.getElementsByTagName(tag)[0].firstChild.nodeValue

#Parse HiSeq
def parse_hiseq(run_params):
    run_start_date = get_firstChild_value(run_params, 'RunStartDate')
    run_start_date = datetime.datetime.strptime(run_start_date, "%y%m%d").date()

    platform = Platform.query.filter(Platform.name == 'HiSeq').first()

    run_info = RunInfo(

        run_id = get_firstChild_value(run_params, 'RunID'),
        experiment_name = get_firstChild_value(run_params, 'ExperimentName'),

        run_mode = get_firstChild_value(run_params, 'RunMode'),
        barcode = get_firstChild_value(run_params, 'Barcode'),
        run_start_date = run_start_date,
        pair_end_fc = bool(get_firstChild_value(run_params, 'PairEndFC')),
        read_1 = int(get_firstChild_value(run_params, 'Read1')),
        read_2 = int(get_firstChild_value(run_params, 'Read2')),
        index_read_1 = int(get_firstChild_value(run_params, 'IndexRead1')),
        index_read_2 = int(get_firstChild_value(run_params, 'IndexRead2')),
        pe = get_firstChild_value(run_params, 'Pe'),

        platform = platform
    )

    return run_info


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

    db.session.add(run_info)
    db.session.commit()
