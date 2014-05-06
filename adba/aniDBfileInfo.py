#!/usr/bin/env python
#
# This file is part of aDBa.
#
# aDBa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# aDBa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with aDBa.  If not, see <http://www.gnu.org/licenses/>.


import hashlib
import os
import xml.etree.cElementTree as etree
from functools import reduce


# http://www.radicand.org/blog/orz/2010/2/21/edonkey2000-hash-in-python/
def get_file_hash(filePath):
	""" Returns the ed2k hash of a given file."""
	if not filePath:
		return None
	md4 = hashlib.new('md4').copy
	ed2kChunkSize=9728000

	def gen(f):
		while True:
			x = f.read(ed2kChunkSize)
			if x: yield x
			else: return

	def md4_hash(data):
		m = md4()
		m.update(data)
		return m

	with open(filePath, 'rb') as f:
		FileSize=os.path.getsize(filePath)
		#if file size is small enough the ed2k hash is the same as the md4 hash
		if (FileSize<=ed2kChunkSize):
			FullFile=f.read()
			return md4_hash(FullFile).hexdigest()
		else:
			a = gen(f)
			hashes = [md4_hash(data).digest() for data in a]
			combinedhash=bytearray()
			for hash in (hashes):
				combinedhash.extend(hash)
			return md4_hash(combinedhash).hexdigest()

def get_file_size(path):
	size = os.path.getsize(path)
	return size



def read_anidb_xml(filePath):
	if not filePath:
		filePath = os.path.join(os.path.dirname(os.path.abspath( __file__ )), "animetitles.xml")
	return read_xml_into_etree(filePath)


def read_tvdb_map_xml(filePath):
	if not filePath:
		filePath = os.path.join(os.path.dirname(os.path.abspath( __file__ )), "anime-list.xml")
	return read_xml_into_etree(filePath)


def read_xml_into_etree(filePath):
		if not filePath:
			return None
		
		f = open(filePath,"r")
		xmlASetree = etree.ElementTree(file = f)
		return xmlASetree
	
