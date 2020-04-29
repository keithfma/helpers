#!/usr/local/python3

import boto3

import argparse
import configparser
from os.path import expanduser
from pathlib import Path
from sys import stdout


# TODO: add a CLI interface with required profile name and optional file name
#   and session name
config_path = Path('~/.aws/config')
profile_name = 'stage'
session_name = 'kma-test'

# read the AWS config file
config = configparser.ConfigParser()
config.read(config_path.expanduser())

# find the requested profile, or die trying
profile_key = f'profile {profile_name}'
try: 
    section = config[profile_key]
except KeyError as err:
    msg = f'No record for profile "{profile_name}" found in config file at {config_path}'
    raise ValueError(msg) from e
    
# get the ARN, or die trying
try:
    role_arn = section['role_arn'] 
except KeyError as err:
    msg = f'Profile "{profile_name}" lacks a role_arn definition'
    raise KeyError(msg) from err

# create the session and retrieve the credentials
sts_client = boto3.client('sts')
assumed_role = sts_client.assume_role(RoleArn=role_arn, RoleSessionName=session_name)
credentials = assumed_role['Credentials']

# shell commands to set enviroment vars to stdout
stdout.write(f"""
export AWS_ACCESS_KEY_ID='{credentials['AccessKeyId']}'
export AWS_SECRET_ACCESS_KEY='{credentials['SecretAccessKey']}'
export AWS_SESSION_TOKEN='{credentials['SessionToken']}'
""")

