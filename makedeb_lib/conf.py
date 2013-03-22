# -*- coding: utf-8 -*-

import os
from xml.dom.minidom import parse

sample="""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<makedeb>
	<control>
		<version>0.1</version>
		<name>@@name@@</name>
		<maintener>Thomas Maurice</maintener>
		<mail>thomas.maurice@example.com</mail>
		<desc>Projet d'exemple</desc>
		<homepage>None</homepage>
		<category>1</category>
		<deps>
			<package>bash</package>
		</deps>
	</control>

	<dirs>
		<dir>/usr/local/bin</dir>
		<dir>/usr/local/man/man1</dir>
	</dirs>

	<files>
		<file if=\"@@name@@\" of=\"/usr/local/bin\" />
		<file if=\"man/@@name@@.1.gz\" of=\"/usr/local/man/man1\" />
	</files>
</makedeb>
"""

def tryFile(f):
	try:
		doc = parse(f)
		root = doc.documentElement
		if root.localName == "makedeb":
			return True
	except:
		return False

def getFile():
	"""
		Scanne le répertoire courant à la recherche du fichier
		xml qui va bien (qui a un <makedeb></makedeb> comme
		noeud root)
	"""
	l=os.listdir(".")
	for i in l:
		if(tryFile(i)):
		  return i
	
	return ""
		
	
