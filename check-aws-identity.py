#!/usr/bin/env python

################################################################
#
# check-aws-identity.py - view which AWS identity boto3 will use
#
# Usage: check-aws-identity.py
#
# No arguments needed.
#
################################################################

# for control-C handling
import sys
import signal

# AWS/S3 interface
import boto3

# Gracefully exit on control-C
signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

def main():

    # make aws connection
    sts = boto3.client('sts')

    # check API identity
    # TODO: get the account alias, too: http://boto.readthedocs.org/en/latest/ref/iam.html#boto.iam.connection.IAMConnection.get_account_alias
    response = sts.get_caller_identity()
    my_identity_account = response["Account"]
    my_identity_arn = response["Arn"].replace("arn:aws:iam::{}:".format(my_identity_account),"")
    print('Using account #{}, "{}".'.format(my_identity_account, my_identity_arn))

if __name__ == "__main__":
    exit(main())
