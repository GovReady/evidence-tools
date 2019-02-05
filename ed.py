#!/usr/bin/env python

################################################################
#
# ed.py - evidence downloader
#
# Usage: ed.py [-h] --bucket my-evidence-bucket [--file screenshot.png]
#
# Required argument:
#   -b, --bucket  my-evidence-bucket  name of source bucket
#
# Optional arguments:
#   -h, --help  show this help message and exit
#   --file screenshot.png  name of an evidence file to download
#
################################################################

# for control-C handling
import sys
import signal

# parse command-line arguments
import argparse

# regular expressions
import re

# OS-specific (paths)
import os

# AWS/S3 interface
import boto3

# Gracefully exit on control-C
signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

# Set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Downloads evidence from an S3 bucket. If no file is specified with "-f", prints the names of all files in the bucket.')
    parser.add_argument('-b', '--bucket', required=True, help='name of source bucket')
    parser.add_argument('-f', '--file', help='path to an evidence file to upload')
    return parser

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

    # make s3 connection
    s3 = boto3.client('s3')

    # if no file specified, list bucket contents
    if (args.file is None):
        try:
            response = s3.list_objects(Bucket=args.bucket)
            for object in response['Contents']:
                print(object['Key'])
            # TODO: replace IsTruncated warning with a NextMarker continuation loop
            if response['IsTruncated']:
                sys.stderr.write("WARNING: List truncated at {} objects.\n".format(response['MaxKeys']))
        except Exception as e:
            print(e)
    else:
        # download file
        # TODO: allow user to specify destination directory, and "overwrite" option
        try:
            if os.path.exists(args.file):
                raise Exception("Download cancelled: file '{}' exists.".format(args.file))
            s3.download_file(
                args.bucket, args.file, args.file
            )
        except Exception as e:
            print(e)
        
if __name__ == "__main__":
    exit(main())
