#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse
import time
import datetime
import plantcv.parallel as pcvp


# Parse command-line arguments
###########################################
def options():
    """Parse command line options.

    Args:

    Returns:
        argparse object.
    Raises:
        IOError: if dir does not exist.
        IOError: if workflow does not exist.
        IOError: if the metadata file SnapshotInfo.csv does not exist in dir when flat is False.
        ValueError: if adaptor is not phenofront or dbimportexport.
        ValueError: if a metadata field is not supported.
    """
    # Job start time
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print("Starting run " + start_time + '\n', file=sys.stderr)

    # These are metadata types that PlantCV deals with.
    # Values are default values in the event the metadata is missing
    valid_meta = {
        # Camera settings
        "camera": {
            "label": "camera identifier",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        "imgtype": {
            "label": "image type",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        "zoom": {
            "label": "camera zoom setting",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        "exposure": {
            "label": "camera exposure setting",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        "gain": {
            "label": "camera gain setting",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        "frame": {
            "label": "image series frame identifier",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        "lifter": {
            "label": "imaging platform height setting",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        # Date-Time
        "timestamp": {
            "label": "datetime of image",
            "datatype": "<class 'datetime.datetime'>",
            "value": None
        },
        # Sample attributes
        "id": {
            "label": "image identifier",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        "plantbarcode": {
            "label": "plant barcode identifier",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        "treatment": {
            "label": "treatment identifier",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        "cartag": {
            "label": "plant carrier identifier",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        # Experiment attributes
        "measurementlabel": {
            "label": "experiment identifier",
            "datatype": "<class 'str'>",
            "value": "none"
        },
        # Other
        "other": {
            "label": "other identifier",
            "datatype": "<class 'str'>",
            "value": "none"
        }
    }
    parser = argparse.ArgumentParser(description='Parallel imaging processing with PlantCV.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--dir", help='Input directory containing images or snapshots.', required=True)
    parser.add_argument("-a", "--adaptor",
                        help='Image metadata reader adaptor. PhenoFront metadata is stored in a CSV file and the '
                             'image file name. For the filename option, all metadata is stored in the image file '
                             'name. Current adaptors: phenofront, filename', default="phenofront")
    parser.add_argument("-p", "--workflow", help='Workflow script file.', required=True)
    parser.add_argument("-j", "--json", help='Output database file name.', required=True)
    parser.add_argument("-i", "--outdir", help='Output directory for images. Not required by all workflows.',
                        default=".")
    parser.add_argument("-T", "--cpu", help='Number of CPU to use.', default=1, type=int)
    parser.add_argument("-c", "--create",
                        help='will overwrite an existing database'
                             'Warning: activating this option will delete an existing database!',
                        default=False, action="store_true")
    parser.add_argument("-D", "--dates",
                        help='Date range. Format: YYYY-MM-DD-hh-mm-ss_YYYY-MM-DD-hh-mm-ss. If the second date '
                             'is excluded then the current date is assumed.',
                        required=False)
    parser.add_argument("-t", "--type", help='Image format type (extension).', default="png")
    parser.add_argument("-l", "--delimiter", help='Image file name metadata delimiter character.', default='_')
    parser.add_argument("-f", "--meta",
                        help='Image file name metadata format. List valid metadata fields separated by the '
                             'delimiter (-l/--delimiter). Valid metadata fields are: ' +
                             ', '.join(map(str, list(valid_meta.keys()))), default='imgtype_camera_frame_zoom_id')
    parser.add_argument("-M", "--match",
                        help='Restrict analysis to images with metadata matching input criteria. Input a '
                             'metadata:value comma-separated list. This is an exact match search. '
                             'E.g. imgtype:VIS,camera:SV,zoom:z500',
                        required=False)
    parser.add_argument("-C", "--coprocess",
                        help='Coprocess the specified imgtype with the imgtype specified in --match '
                             '(e.g. coprocess NIR images with VIS).',
                        default=None)
    parser.add_argument("-w", "--writeimg", help='Include analysis images in output.', default=False,
                        action="store_true")
    parser.add_argument("-o", "--other_args", help='Other arguments to pass to the workflow script.', required=False)
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        raise IOError("Directory does not exist: {0}".format(args.dir))
    if not os.path.exists(args.workflow):
        raise IOError("File does not exist: {0}".format(args.workflow))
    if args.adaptor is 'phenofront':
        if not os.path.exists(os.path.join(args.dir, 'SnapshotInfo.csv')):
            raise IOError(
                'The snapshot metadata file SnapshotInfo.csv does not exist in {0}. '
                'Perhaps you meant to use a different adaptor?'.format(
                    args.dir))
    if not os.path.exists(args.outdir):
        raise IOError("Directory does not exist: {0}".format(args.outdir))

    args.jobdir = start_time
    try:
        os.makedirs(args.jobdir)
    except IOError as e:
        raise IOError("{0}: {1}".format(e.strerror, args.jobdir))

    if args.adaptor != 'phenofront' and args.adaptor != 'filename':
        raise ValueError("Adaptor must be either phenofront or filename")

    if args.dates:
        dates = args.dates.split('_')
        if len(dates) == 1:
            # End is current time
            dates.append(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        start = map(int, dates[0].split('-'))
        end = map(int, dates[1].split('-'))
        # Convert start and end dates to Unix time
        start_td = datetime.datetime(*start) - datetime.datetime(1970, 1, 1)
        end_td = datetime.datetime(*end) - datetime.datetime(1970, 1, 1)
        args.start_date = (start_td.days * 24 * 3600) + start_td.seconds
        args.end_date = (end_td.days * 24 * 3600) + end_td.seconds
    else:
        end = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        end_list = map(int, end.split('-'))
        end_td = datetime.datetime(*end_list) - datetime.datetime(1970, 1, 1)
        args.start_date = 1
        args.end_date = (end_td.days * 24 * 3600) + end_td.seconds

    args.valid_meta = valid_meta
    args.start_time = start_time

    # Image filename metadata structure
    fields = args.meta.split(args.delimiter)
    # Keep track of the number of metadata fields matching filenames should have
    args.meta_count = len(fields)
    structure = {}
    for i, field in enumerate(fields):
        structure[field] = i
    args.fields = structure

    # Are the user-defined metadata valid?
    for field in args.fields:
        if field not in args.valid_meta:
            raise ValueError("The field {0} is not a currently supported metadata type.".format(field))

    # Metadata restrictions
    args.imgtype = {}
    if args.match is not None:
        pairs = args.match.split(',')
        for pair in pairs:
            key, value = pair.split(':')
            args.imgtype[key] = value
    else:
        args.imgtype['None'] = 'None'

    if (args.coprocess is not None) and ('imgtype' not in args.imgtype):
        raise ValueError("When the coprocess imgtype is defined, imgtype must be included in match.")

    # Recreate JSON file if flag is on
    if os.path.exists(args.json) and args.create:
        os.remove(args.json)

    return args


###########################################

# Main
###########################################
def main():
    """Main program.

    Args:

    Returns:

    Raises:

    """

    # Get options
    args = options()

    # Variables
    ###########################################
    # Database upload file name prefix
    # Use user inputs to make filenames
    prefix = 'plantcv'
    if args.imgtype is not None:
        kv_list = []
        for key in args.imgtype:
            kv_list.append(key + str(args.imgtype[key]))
        prefix = prefix + '_' + '_'.join(map(str, kv_list))
    if args.dates:
        prefix = prefix + '_' + args.dates
    ###########################################

    # Open log files
    error_log = open(prefix + '_errors_' + args.start_time + '.log', 'w')

    # Run info
    ###########################################

    # Read image file names
    ###########################################
    jobcount, meta = pcvp.metadata_parser(data_dir=args.dir, meta_fields=args.fields, valid_meta=args.valid_meta,
                                          meta_filters=args.imgtype, start_date=args.start_date, end_date=args.end_date,
                                          error_log=error_log, delimiter=args.delimiter, file_type=args.type,
                                          coprocess=args.coprocess)
    ###########################################

    # Process images
    ###########################################
    # Job builder start time
    job_builder_start_time = time.time()
    print("Building job list... ", file=sys.stderr)
    jobs = pcvp.job_builder(meta=meta, valid_meta=args.valid_meta, workflow=args.workflow, job_dir=args.jobdir,
                            out_dir=args.outdir, coprocess=args.coprocess, other_args=args.other_args,
                            writeimg=args.writeimg)
    # Job builder clock time
    job_builder_clock_time = time.time() - job_builder_start_time
    print("took " + str(job_builder_clock_time) + '\n', file=sys.stderr)

    # Parallel image processing time
    multi_start_time = time.time()
    print("Processing images... ", file=sys.stderr)

    pcvp.multiprocess(jobs, args.cpu)

    # Parallel clock time
    multi_clock_time = time.time() - multi_start_time
    print("took " + str(multi_clock_time) + '\n', file=sys.stderr)
    ###########################################

    # Compile image analysis results
    ###########################################
    # Process results start time
    process_results_start_time = time.time()
    print("Processing results... ", file=sys.stderr)
    pcvp.process_results(job_dir=args.jobdir, json_file=args.json)
    # Process results clock time
    process_results_clock_time = time.time() - process_results_start_time
    print("took " + str(process_results_clock_time) + '\n', file=sys.stderr)
    ###########################################

    # Cleanup
    ###########################################
    error_log.close()
    ###########################################


###########################################

if __name__ == '__main__':
    main()
