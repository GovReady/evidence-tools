#!/usr/bin/env python

################################################################
#
# ed.py - evidence downloader
#
# Usage: ed.py [-h] --bucket my-evidence-bucket [--file screenshot.png]
#
# With `--file`, downloads the specified file from the bucket.
# Without `--file`, lists all the files in the bucket.  With
# `--metadata`, prints metadata for the file or files to STDOUT.
#
# Required argument:
#   -b, --bucket  my-evidence-bucket  name of source bucket
#
# Optional arguments:
#   -h, --help  show this help message and exit
#   -f, --file  screenshot.png  name of an evidence file to download
#   -m, --metadata  print metadata for the file or files
#   --url  generate a pre-signed URL for the evidence file, expires in 120 seconds
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
from botocore.client import Config

# Gracefully exit on control-C
signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

# Set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Downloads evidence from an S3 bucket. If no file is specified with "-f", prints the names of all files in the bucket.')
    parser.add_argument('-b', '--bucket', required=True, help='name of source bucket')
    parser.add_argument('-f', '--file', help='path to an evidence file to download')
    parser.add_argument('-m', '--metadata', action='store_true', help='print metadata for the file or files')
    parser.add_argument('--url', action='store_true', help='generate a pre-signed URL for the evidence file')
    return parser

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

    # make s3 connection
    s3 = boto3.client('s3', 'us-east-1', config=Config(s3={'addressing_style': 'path'},signature_version='s3v4'))

    # if no file specified, list bucket contents
    if args.file is None:
        try:
            response = s3.list_objects(Bucket=args.bucket)
            for object in response['Contents']:
                print(object['Key'])
                if args.metadata:
                    response2 = s3.head_object(Bucket=args.bucket, Key=object['Key'])
                    print('#', response2['Metadata'])
            # TODO: replace IsTruncated warning with a NextMarker continuation loop
            if response['IsTruncated']:
                sys.stderr.write("WARNING: List truncated at {} objects.\n".format(response['MaxKeys']))
        except Exception as e:
            print(e)
    else:
        if args.url:
            # generate pre-signed URL
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': args.bucket,
                    'Key': args.file
                },
                ExpiresIn=120 # seconds
            )
            print(url)
        else:
            # download file
            # TODO: allow user to specify destination directory, and "overwrite" option
            try:
                if os.path.exists(args.file):
                    raise Exception("Download cancelled: file '{}' exists.".format(args.file))
                s3.download_file(
                    args.bucket, args.file, args.file
                )
                if args.metadata:
                    response = s3.head_object(Bucket=args.bucket, Key=args.file)
                    print('#', response['Metadata'])
            except Exception as e:
                print(e)
        
if __name__ == "__main__":
    exit(main())
