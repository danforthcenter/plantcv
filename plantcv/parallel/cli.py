#!/usr/bin/env python
import os
import sys
import argparse
import plantcv.parallel


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
    parser = argparse.ArgumentParser(description='Parallel imaging processing with PlantCV.')
    config_grp = parser.add_argument_group("CONFIG")
    config_grp.add_argument("--template", required=False, help="Create a template configuration file.")
    run_grp = parser.add_argument_group("RUN")
    run_grp.add_argument("--config", required=False,
                         help="Input configuration file (created using the --template option).")
    inspect_grp = parser.add_argument_group("DRYRUN")
    inspect_grp.add_argument("--dryrun", required=False,
                             help="Input configuration file (created using the --template option).")
    args = parser.parse_args()

    # Create a config
    config = plantcv.parallel.WorkflowConfig()

    # Create a template configuration file if requested
    if args.template:
        config.save_config(config_file=args.template)
        sys.exit()

    # run or dry-run
    configfile = args.config
    dryrun = False
    if args.dryrun:
        dryrun = args.dryrun
        configfile = args.dryrun
    # Import a configuration if provided
    if configfile:
        config.import_config(config_file=configfile)
        if configfile == config.results:
            print("Configuration file would be overwritten by results, change the results field of config.",
                  file=sys.stderr)
            sys.exit(1)

    if not config.validate_config():
        print("Error: Invalid configuration file. Check errors above.", file=sys.stderr)
        sys.exit(1)
    return config, dryrun
###########################################


# Run the main program
###########################################
def main():
    """Main program.

    Args:

    Returns:

    Raises:

    """
    # Get options
    config, dryrun = options()
    if dryrun:
        summary_df, meta = plantcv.parallel.inspect_dataset(config)
        print(f"Saving {dryrun}_summary_df.csv")
        summary_df.to_csv(os.path.splitext(dryrun)[0] + "_summary_df.csv")
        print(f"Saving {os.path.splitext(dryrun)[0]}_metadata_df.csv")
        meta.to_csv(dryrun + "_metadata_df.csv")
    else:
        # run parallel using config
        plantcv.parallel.run_parallel(config)
###########################################
