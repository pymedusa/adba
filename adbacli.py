#!/usr/bin/env python3

import argparse
import inspect
import logging
import os
import sys
import adba
import pprint

stateToUDP = dict(unknown=0, hdd=1, cd=2, deleted=3)
viewedToUDP = dict(unwatched=0, watched=1)
blacklistFields = list(('unused', 'retired', 'reserved'))
fileTypes = '.avi,.mp4,.mkv,.ogm'

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=['hash', 'mylistadd', 'mylistdel', 'mylistaddwithfields', 'getfields', 'listfields'],
help='Command to execute. hash: Hash the file and print its ed2k hash. mylistadd: Hash the file and add it to AniDB MyList. If the file was there, it will be updated. mylistdel: Hash the file and delete it from AniDB MyList. getfields: Hash the file and retrieve requested fields for the hashed file. listfields: Lists all the available fields that can be requested from AniDB.')
parser.add_argument('--file-types', default=fileTypes,
help='A comma delmited list of file types to be included when searching directories. Default: ' + fileTypes)
parser.add_argument('--out-file', action='store', default=None,
help='Write output to specified file instead of STDOUT.')
parser.add_argument('-u', '--username', action='store', default=None,
help='User name needed to communicate with AniDB.')
parser.add_argument('-p', '--password', action='store', default=None,
help='Password needed to communicate with AniDB.')
parser.add_argument('--state', choices=['unknown', 'hdd', 'cd', 'deleted'], default='hdd',
help='Sets the file state to unknown/hdd/cd/deleted. Default: hdd')
parser.add_argument('--watched', action='store_true',
help='Marks the file as watched.')
parser.add_argument('--source', action='store', default=None,
help='Sets the file source (any string).')
parser.add_argument('--storage', action='store', default=None,
help='Sets file storage (any string).')
parser.add_argument('--other', action='store', default=None,
help='Sets other remarks (any string).')
parser.add_argument('--fields', action='store', default=None,
help='A comma delimited list of fields requested from AniDB.')
parser.add_argument('files', nargs='*', default=[],
help='All files and/or folders to be processed.')

args, otherArgs = parser.parse_known_args()

fileParser = argparse.ArgumentParser()
fileParser.add_argument('files', nargs='*', default=[],
help='All files and/or folders to be processed.')

fileArgs = fileParser.parse_args(otherArgs)

allFiles = args.files + fileArgs.files

# Function to convert an object's attributes to a dictionary for lookup
def attrToDict(obj):
	pr = dict()
	for name in dir(obj):
		value = getattr(obj, name)
		if not name.startswith('__') and not inspect.ismethod(value):
			pr[name] = value
	return pr

# Redirect sys.stdout if requested
if args.out_file:
	sys.stdout = open(args.out_file, 'w')

# Check if fields are required
if args.command in ['mylistaddwithfields', 'getfields']:
	if not args.fields:
		print("Fields to retrieve are required for " + args.command + ".")
		sys.exit(0)

# Convert state to UDP
args.state = stateToUDP[args.state]

# Convert watched to UDP
if args.watched:
	args.watched=viewedToUDP['watched']
else:
	args.watched=viewedToUDP['unwatched']

# Parse positional arguments passed in and convert all to files
fileList = list()
validExtensions = args.file_types.lower().split(',')
for entry in list(allFiles):
	if os.path.isfile(entry):
		if any(os.path.splitext(entry)[1].lower() == valid for valid in validExtensions):
			fileList.append(entry)
	elif os.path.isdir(entry):
		for dirpath, dirnames, filenames in os.walk(entry):
			for filename in filenames:
				if any(os.path.splitext(filename)[1].lower() == valid for valid in validExtensions):
					fileList.append(filename)

# Check if files are required
if args.command in ['hash', 'mylistadd', 'mylistdel', 'mylistaddwithfields', 'getfields']:
	if len(fileList) == 0:
		print("Files and/or directories containing valid files are required for " + args.command + ".")
		sys.exit(0)

# Check if login is required and create connection if have login credentials
if args.command in ['mylistadd', 'mylistdel', 'mylistaddwithfields', 'getfields']:
	if not args.username or not args.password:
		print("User and password required for " + args.command + ".")
		sys.exit(0)
	connection = adba.Connection(log=False)
	try:
		connection.auth(args.username, args.password)
	except Exception as e :
		print(("exception msg: " + str(e)))

# Execute command
if args.command == 'hash':
	# Hash the file
	for thisFile in fileList:
		thisED2K = adba.aniDBfileInfo.get_ED2K(thisFile, forceHash=True)
		print(thisED2K)
elif args.command == 'mylistadd':
	# First try to add the file, then try to edit
	if connection.authed():
		for thisFile in fileList:
			episode = adba.Episode(connection, filePath=thisFile)
			try:
				episode.edit_to_mylist(state=args.state, viewed=args.watched, source=args.source, storage=args.storage, other=args.other)
				print(thisFile + " successfully edited in AniDB MyList.")
			except:
				episode.add_to_mylist(state=args.state, viewed=args.watched, source=args.source, storage=args.storage, other=args.other)
				print(thisFile + " successfully added to AniDB MyList.")
elif args.command == 'mylistdel':
	# Delete the file
	if connection.authed():
		for thisFile in fileList:
			episode = adba.Episode(connection, filePath=thisFile)
			try:
				episode.delete_from_mylist()
				print(thisFile + " successfully removed from AniDB MyList.")
			except:
				print(thisFile + " could not be removed from AniDB MyList.")
elif args.command == 'mylistaddwithfields':
	# Parse requested field(s)
	requestedFields = list(args.fields.lower().split(','))
	# Separate fields by request type
	maper = adba.aniDBmaper.AniDBMaper()
	maperFileF = set(maper.getFileMapF())
	maperFileA = set(maper.getFileMapA())
	requestF = list(maperFileF & set(requestedFields))
	requestA = list(maperFileA & set(requestedFields))
	# Add/edit the file to AniDB and print the retrieved field(s)
	if connection.authed():
		for thisFile in fileList:
			episode = adba.Episode(connection, filePath=thisFile, load=True, paramsF=requestF, paramsA=requestA)
			try:
				episode.edit_to_mylist(state=args.state, viewed=args.watched, source=args.source, storage=args.storage, other=args.other)
			except:
				episode.add_to_mylist(state=args.state, viewed=args.watched, source=args.source, storage=args.storage, other=args.other)
			episodeDict = attrToDict(episode)
			print("filename\t" + thisFile)
			for field in requestedFields:
				print(field + "\t" + str(episodeDict[field]))
elif args.command == 'getfields':
	# Parse requested field(s)
	requestedFields = list(args.fields.lower().split(','))
	# Separate fields by request type
	maper = adba.aniDBmaper.AniDBMaper()
	maperFileF = set(maper.getFileMapF())
	maperFileA = set(maper.getFileMapA())
	requestF = list(maperFileF & set(requestedFields))
	requestA = list(maperFileA & set(requestedFields))
	# Retrieve the requested field(s)
	if connection.authed():
		for thisFile in fileList:
			episode = adba.Episode(connection, filePath=thisFile, load=True, paramsF=requestF, paramsA=requestA)
			episodeDict = attrToDict(episode)
			print("filename\t" + thisFile)
			for field in requestedFields:
				print(field + "\t" + str(episodeDict[field]))
elif args.command == 'listfields':
	# Print all the possible field(s) that can be requested, remove blacklisted fields
	maper = adba.aniDBmaper.AniDBMaper()
	maperFileF = list(maper.getFileMapF())
	maperFileA = list(maper.getFileMapA())
	allFields = maperFileF + maperFileA
	validFields = [field for field in allFields if field not in blacklistFields]
	print('\t'.join(validFields))

# Logout if connection active
if args.command in ['mylistadd', 'mylistdel', 'mylistaddwithfields', 'getfields']:
	connection.logout(True)

sys.exit(0)
