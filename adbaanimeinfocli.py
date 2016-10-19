#!/usr/bin/env python3
import argparse
import os
import sys
import adba


blacklistFields = list(('unused', 'retired', 'reserved', 'IsDeprecated'))

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=['animeinfo', 'logout'],help='Get info or log out')
parser.add_argument('AID',help='AID of Series wishing to find info for')
parser.add_argument('--out-file', action='store', default=None, help='Write output to specified file instead of STDOUT.')
parser.add_argument('-u', '--username', action='store', default=None,help='User name needed to communicate with AniDB.')
parser.add_argument('-p', '--password', action='store', default=None,help='Password needed to communicate with AniDB.')
args=parser.parse_args()

# Start logging
FileListener = adba.StartLogging()

if args.out_file:
	sys.stdout = open(args.out_file, 'w', encoding='UTF-8')


# Issue logout of session
if args.command == 'logout':
	connection = adba.Connection(commandDelay=2.1)
	connection.logout()
	sys.exit(0)

# we now need to login to actually get the anime info

connection = adba.Connection()

try:
	connection.auth(args.username,args.password)
	print('Authing to system')
except Exception as e:
	print('Exception: %s', e)
	sys.exit(1)

if connection.authed():
	try:
		maper=adba.aniDBmaper.AniDBMaper()
		animeFieldsWanted=maper.getAnimeMapA()
		animeFieldsWanted=animeFieldsWanted[0:10]
		animeMaper=[field for field in animeFieldsWanted if field not in blacklistFields]

		animeInfo=adba.Anime(connection,aid=args.AID,load=True,paramsA=animeMaper)
		print(animeInfo.rawData)
	except Exception as e:
		print('Exception: %s', e)
		connection.stayloggedin()
		sys.exit(1)

# some clean up tasks that must happen every time
connection.stayloggedin()
adba.StopLogging(FileListener)