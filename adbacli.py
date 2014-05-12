#!/usr/bin/env python

import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument('anidb-command', choices=['hash', 'mylistadd', 'getfields', 'listfields'],
help='Command to execute. hash: Hash the file and print its ed2k hash. mylistadd: Hash the file and add it to AniDB. If the file was there, it will be updated. getfields: Hash the file and retrieve requested fields for the hashed file. listfields: Lists all the available fields that can be requested from AniDB.')
parser.add_argument('--state', choices=['unknown', 'hdd', 'cd', 'deleted'],
help='Sets the file state to unknown/hdd/cd/deleted.')
parser.add_argument('--watched', action='store_true',
help='Marks the file as watched.')
parser.add_argument('--watchdate', action='store',
help='Sets the date the file was watched.')
parser.add_argument('--source', action='store',
help='Sets the file source (any string).')
parser.add_argument('--storage', action='store',
help='Sets file storage (any string).')
parser.add_argument('--other', action='store',
help='Sets other remarks (any string).')
parser.add_argument('--file-fields', action='store',
help='A comma delimited list of file fields requested from AniDB.')
parser.add_argument('--anime-fields', action='store',
help='A comma delimited list of anime fields requested from AniDB.')

args = parser.parse_args()

if args.anidb_command == 'hash':
	# Hash the file
elif args.anidb_command == 'mylistadd':
	# First try to add the file
elif args.anidb_command == 'getfields':
	# Retrieve the requested fields
elif args.anidb_command == 'listfields':
	# Print all the possible fields that can be requested

sys.exit(0)
