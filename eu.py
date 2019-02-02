#!/usr/bin/env python

################################################################
#
# eu.py - evidence uploader
#
# Usage: eu.py [-h] --file screenshot.png
#
# Required argument:
#   --file screenshot.png  path to an evidence file to upload
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

# S3 interface
import tinys3

# Gracefully exit on control-C
signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

# Set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Uploads evidence to an S3 bucket.')
    parser.add_argument('-f', '--file', required=True, help='path to an evidence file to upload')
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

    # set credentials
    s3_access_key = 'AKIAIAHTTVOVCT5ZGIHQ'
    s3_secret_key = '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'
    s3_bucket = 'govready-evidence-qb9zxvylp8dluv5bcg1exb'

    # make s3 connection
    s3 = tinys3.Connection(s3_access_key, s3_secret_key, default_bucket=s3_bucket, tls=True)

    # upload file
    f = open(args.file,'rb')
    s3.upload(extract_basename(args.file),f)
    f.close()

if __name__ == "__main__":
    exit(main())
