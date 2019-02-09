#!/usr/bin/env python

################################################################
#
# es-credentials.py - sets up credentials for evidence server 
#
# Usage: es-credentials.py [-h] --bucket evidence-server-01
#
# Examples:
#   ./es-credentials.py -r -b govready-es-srv-01 -p govready-es-srv-01+read -u govready-es-srv-01+read
#   ./es-credentials.py -w -b govready-es-srv-01 -p govready-es-srv-01+write -u govready-es-srv-01+write
#
# Required arguments:
#   -b, --bucket  evidence-server-01  name of evidence server bucket
#   -p, --policy  evidence-server-01-policy  name of policy
#
# Optional arguments (need at least one of -r or -w):
#   -h, --help   show this help message and exit
#   -r, --read  include read permission in policy
#   -w, --write  include write permission in policy
#   -u, --user USERNAME  create a user
#
################################################################

# for control-C handling
import sys
import signal

# parse command-line arguments
import argparse

# AWS/S3 interface
import boto3
from botocore.exceptions import ClientError

# Gracefully exit on control-C
signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

# IAM policies

iam_policy_bucket_read = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:GetObjectTagging"
            ],
            "Resource": [
            ]
        }
    ]
}

iam_policy_bucket_write = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:PutObjectTagging"
            ],
            "Resource": [
            ]
        }
    ]
}

# Set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Sets up credentials for evidence server.')
    parser.add_argument('-b', '--bucket', required=True, help='name of evidence server bucket')
    parser.add_argument('-p', '--policy', required=True, help='name of policy')
    rw_group = parser.add_mutually_exclusive_group(required=True)
    rw_group.add_argument('-r', '--read', action='store_true', help='include read permission in policy')
    rw_group.add_argument('-w', '--write', action='store_true', help='include write permission in policy')
    parser.add_argument('-u', '--user', help='name of user')
    # TODO: consider specifying descriptions and tags
    return parser

def confirm_or_create_bucket(aws_region, s3, bucket_name):
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            try:
                if aws_region == 'us-east-1':
                    # no LocationConstraint is used if AWS region is 'us-east-1'
                    response = s3.create_bucket(
                        ACL='private',
                        Bucket=bucket_name
                        )
                else:
                    response = s3.create_bucket(
                        ACL='private',
                        Bucket=bucket_name,
                        CreateBucketConfiguration={
                            'LocationConstraint': aws_region
                            }
                        )
                if response["ResponseMetadata"]["HTTPStatusCode"] is not 200:
                    print(response)
                    print("Error: bucket creation failed.")
                response = s3.put_public_access_block(
                    Bucket=bucket_name,
                    PublicAccessBlockConfiguration={
                        'BlockPublicAcls': True,
                        'IgnorePublicAcls': True,
                        'BlockPublicPolicy': True,
                        'RestrictPublicBuckets': True
                        }
                    )
            except Exception as e:
                print(e)
        else:
            print(e)

def confirm_or_create_policy(iam, args):
    try:
        response = iam.list_policies(Scope='Local')
        arn = None
        # TODO: use NextMarker to retrieve more than one page
        for policy in response["Policies"]:
            if policy["PolicyName"] == args.policy:
                arn = policy["Arn"]
        if arn is None:
            # policy was not found; let's create it
            iam_policy_bucket_read["Statement"][1]["Resource"] = [
                "arn:aws:s3:::{}/*".format(args.bucket),
                "arn:aws:s3:::{}".format(args.bucket)
                ]
            response = iam.create_policy(
                PolicyName=args.policy,
                PolicyDocument=str(iam_policy_bucket_read).replace("'",'"')
                )
            if response["ResponseMetadata"]["HTTPStatusCode"] is not 200:
                print(response)
                print("Error: policy creation failed.")
            arn = response["Policy"]["Arn"]
    except Exception as e:
        print(e)
    return arn

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

# (sample messages to use at the right spot)
# WARNING: -r ignored because policy {} already exists.
# Attaching existing policy {}.

    # make s3 connections
    aws_region = 'us-east-1'
    iam = boto3.client('iam')
    s3 = boto3.client('s3', aws_region)

    # make sure bucket exists
    confirm_or_create_bucket(aws_region, s3, args.bucket)

    # make sure policy exists
    arn = confirm_or_create_policy(iam, args)
        
    # make sure user exists
    try:
        response = iam.create_user(
            UserName=args.user,
            Tags=[
                {
                    'Key':'created-by',
                    'Value':'govready:es-credentials'
                    }
                ]
            )
    except ClientError as e:
        if e.response["Error"]["Code"] == 'EntityAlreadyExists':
            pass
        else:
            print(e)

    # attach policy
    response = iam.attach_user_policy(
        UserName=args.user,
        PolicyArn=arn
        )

if __name__ == "__main__":
    exit(main())
