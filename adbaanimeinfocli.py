#!/usr/bin/env python3
import argparse
import os
import sys
import adba
parser = argparse.ArgumentParser()
parser.add_argument('command', choices=['animeinfo', 'logout'],help='Get info or log out')
parser.add_argument('AID',help='AID of Series wishing to find info for')
parser.add_argument('--out-file', action='store', default=None, help='Write output to specified file instead of STDOUT.')
parser.add_argument('-u', '--username', action='store', default=None,help='User name needed to communicate with AniDB.')
parser.add_argument('-p', '--password', action='store', default=None,help='Password needed to communicate with AniDB.')

args=parser.parse_args()

# Start logging
FileListener = adba.StartLogging()