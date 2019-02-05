#!/usr/bin/env python

################################################################
#
# eu.py - evidence uploader
#
# Usage: eu.py [-h] --bucket my-evidence-bucket --file screenshot.png
#
# Required argument:
#   -b, --bucket  my-evidence-bucket  name of destination bucket
#   -f, --file  screenshot.png  path to an evidence file to upload
#
# Optional argument:
#   -h, --help   show this help message and exit
#
################################################################

# for control-C handling
import sys
import signal

# parse command-line arguments
import argparse

# regular expressions
import re

# AWS/S3 interface
import boto3

# Gracefully exit on control-C
signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

# Set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Uploads evidence to an S3 bucket.')
    parser.add_argument('-b', '--bucket', required=True, help='name of destination bucket')
    parser.add_argument('-f', '--file', required=True, help='path to an evidence file to upload')
    parser.add_argument('-m', '--metadata', action='append', help='metadata in KEY=VALUE form; okay to specify multiple times')
    return parser

# Extracts basename of a given path. Should Work with any OS Path on any OS
# from https://stackoverflow.com/posts/40845585/revisions
def extract_basename(path):
  basename = re.search(r'[^\\/]+(?=[\\/]?$)', path)
  if basename:
    return basename.group(0)

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

    # point to bucket
    s3_bucket = 'govready-evidence-qb9zxvylp8dluv5bcg1exb'

    # make s3 connection
    s3 = boto3.client('s3')

    # get metadata key/value pairs
    metadata = {}
    for m in args.metadata:
        k, v = m.split('=', 2)
        metadata.update({k:v})

    # upload file
    try:
        s3.upload_file(
            args.file, args.bucket, extract_basename(args.file),
            ExtraArgs={"Metadata": metadata}
        )

    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    exit(main())
