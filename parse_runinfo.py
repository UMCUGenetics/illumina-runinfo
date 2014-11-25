import argparse
import sys
import datetime
from xml.dom.minidom import parse
from sqlalchemy import exc

from app import db
from app.models import RunInfo, Platform

#get_firstChild_value
def get_firstChild_value(run_params, tag):
    return run_params.getElementsByTagName(tag)[0].firstChild.nodeValue

#Parse HiSeq
def parse_hiseq(run_params):
    #run_start_date str to python date format
    run_start_date = get_firstChild_value(run_params, 'RunStartDate')
    run_start_date = datetime.datetime.strptime(run_start_date, "%y%m%d").date()

    #Get Platform -> Hiseq
    platform = Platform.query.filter(Platform.name == 'HiSeq').first()

    #Make run_info object
    run_info = RunInfo(
        run_id = get_firstChild_value(run_params, 'RunID'),
        experiment_name = get_firstChild_value(run_params, 'ExperimentName'),
        run_mode = get_firstChild_value(run_params, 'RunMode'),
        barcode = get_firstChild_value(run_params, 'Barcode'),
        run_start_date = run_start_date,
        paired_end = bool(get_firstChild_value(run_params, 'PairEndFC')),
        read_1 = int(get_firstChild_value(run_params, 'Read1')),
        read_2 = int(get_firstChild_value(run_params, 'Read2')),
        index_read_1 = int(get_firstChild_value(run_params, 'IndexRead1')),
        index_read_2 = int(get_firstChild_value(run_params, 'IndexRead2')),
        pe = get_firstChild_value(run_params, 'Pe'),
        platform = platform
    )

    return run_info

#Parse MiSeq
def parse_miseq(run_params):
    #run_start_date str to python date format
    run_start_date = get_firstChild_value(run_params, 'RunStartDate')
    run_start_date = datetime.datetime.strptime(run_start_date, "%y%m%d").date()

    #Get Platform -> Hiseq
    platform = Platform.query.filter(Platform.name == 'MiSeq').first()

    #Get read, index and pe info
    read_1 = run_params.getElementsByTagName('RunInfoRead')[0].getAttribute('NumCycles')

    if run_params.getElementsByTagName('RunInfoRead')[1].getAttribute('IsIndexedRead') == 'N':
        read_2 = run_params.getElementsByTagName('RunInfoRead')[1].getAttribute('NumCycles')
        paired_end = True
        index_read_1 = None
        index_read_2 = None

    elif run_params.getElementsByTagName('RunInfoRead')[1].getAttribute('IsIndexedRead') == 'Y':
        index_read_1 = run_params.getElementsByTagName('RunInfoRead')[1].getAttribute('NumCycles')
        if run_params.getElementsByTagName('RunInfoRead')[2].getAttribute('IsIndexedRead') == 'Y':
            index_read_2 = run_params.getElementsByTagName('RunInfoRead')[2].getAttribute('NumCycles')
        read_2 = run_params.getElementsByTagName('RunInfoRead')[3].getAttribute('NumCycles')
        paired_end = True

    else:
        index_read_2 = None
        read_2 = run_params.getElementsByTagName('RunInfoRead')[2].getAttribute('NumCycles')
        paired_end = True

    run_info = RunInfo(
        run_id = get_firstChild_value(run_params, 'RunID'),
        experiment_name = get_firstChild_value(run_params, 'ExperimentName'),
        run_mode = get_firstChild_value(run_params, 'Chemistry'),
        barcode = get_firstChild_value(run_params, 'Barcode'),
        run_start_date = run_start_date,
        paired_end = paired_end,
        read_1 = read_1,
        read_2 = read_2,
        index_read_1 = index_read_1,
        index_read_2 = index_read_2,
        platform = platform
    )

    return run_info

#Parse NextSeq
def parse_nextseq(run_params):
    #run_start_date str to python date format
    run_start_date = get_firstChild_value(run_params, 'RunStartDate')
    run_start_date = datetime.datetime.strptime(run_start_date, "%y%m%d").date()

    #Get Platform -> Hiseq
    platform = Platform.query.filter(Platform.name == 'NextSeq').first()

    run_info = RunInfo(
        run_id = get_firstChild_value(run_params, 'RunID'),
        experiment_name = get_firstChild_value(run_params, 'ExperimentName'),
        run_mode = get_firstChild_value(run_params, 'Chemistry'),
        barcode = get_firstChild_value(run_params, 'FlowCellSerial'),
        run_start_date = run_start_date,
        paired_end = bool(get_firstChild_value(run_params, 'IsPairedEnd')),
        read_1 = int(get_firstChild_value(run_params, 'PlannedRead1Cycles')),
        read_2 = int(get_firstChild_value(run_params, 'PlannedRead2Cycles')),
        index_read_1 = int(get_firstChild_value(run_params, 'PlannedIndex1ReadCycles')),
        index_read_2 = int(get_firstChild_value(run_params, 'PlannedIndex2ReadCycles')),
        platform = platform
    )

    return run_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('runParametersFile', help="Illumina runParameters.xml file")
    args = parser.parse_args()

    # Parse runParameters.xml
    run_parameters = parse(args.runParametersFile)

    application_name = get_firstChild_value(run_parameters, 'ApplicationName')
    if application_name == 'HiSeq Control Software':
        run_info = parse_hiseq(run_parameters)
    elif application_name == 'MiSeq Control Software':
        run_info = parse_miseq(run_parameters)
    elif application_name == 'NextSeq Control Software':
        run_info = parse_nextseq(run_parameters)
    else:
        sys.exit("Unknown ApplicationName")

    # Save run_info object to database
    try:
        db.session.add(run_info)
        db.session.commit()
        print "Added to database:\t" + str(run_info)
    except exc.IntegrityError:
        db.session.rollback()
        sys.exit("This run is already in the database:\t" + str(run_info))
