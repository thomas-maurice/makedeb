# -*- coding: utf-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
import os
import script

class Project:
	def __init__(self, xmlfile):
		"""
			Initialise la classe et lance le parsing
			du fichier du paquet
		"""
		# Définition des variables
		# Le document XML
		self.doc = parse(xmlfile)
		# Matrice des [infile, outfile]
		self.files = []
		# Tableau des répertoires à créer
		self.dirs = []
		# Dépendances
		self.deps = []
		# Version du paquet
		self.version = ""
		# Nom
		self.name = ""
		# Maintener, mail, homepage
		self.maintener = ""
		self.mail = ""
		self.homepage = ""
		# Description
		self.desc = ""
		# Categorie
		self.category = ""
		# pre|post inst et rm
		self.preinst = ""
		self.postinst = ""
		self.prerm = ""
		self.postrm = ""
    
		self.parse()
  
	def parse(self):
		"""
			Lis le fichier XML contenant les infos du paquet et les stock
			dans la classe.
		"""
		# Récupération de l'élément racine
		root = self.doc.documentElement
		control = root.getElementsByTagName("control")
		dirs = root.getElementsByTagName("dirs")
		files = root.getElementsByTagName("files")
    
		# Parse de la liste des fichiers
		for element in files[0].childNodes:
			if element.nodeType == element.ELEMENT_NODE and element.localName == "file":
				self.files.append( [element.getAttributeNode("if").nodeValue,
														element.getAttributeNode("of").nodeValue])
														
		# Parse de la liste des répertoires	
		for element in dirs[0].childNodes:
			if element.nodeType == element.ELEMENT_NODE and element.localName == "dir":
				self.dirs.append(element.childNodes[0].nodeValue)
		
		# Parse du control
		for element in control[0].childNodes:
			# Elements entre tags
			if element.nodeType == element.ELEMENT_NODE:
				if element.localName == "version":
					self.version = element.childNodes[0].nodeValue
				elif element.localName == "name":
					self.name = element.childNodes[0].nodeValue
				elif element.localName == "maintener":
					self.maintener = element.childNodes[0].nodeValue
				elif element.localName == "mail":
					self.mail = element.childNodes[0].nodeValue
				elif element.localName == "homepage":
					self.homepage = element.childNodes[0].nodeValue
				elif element.localName == "category":
					self.category = element.childNodes[0].nodeValue
				elif element.localName == "desc":
					self.desc = element.childNodes[0].nodeValue
				elif element.localName == "preinst":
					self.preinst = element.childNodes[0].nodeValue
				elif element.localName == "postinst":
					self.postinst = element.childNodes[0].nodeValue
				elif element.localName == "prerm":
					self.prerm = element.childNodes[0].nodeValue
				elif element.localName == "postrm":
					self.postrm = element.childNodes[0].nodeValue
					
			# Parse des dépendances
			if element.localName == "deps":
				for pack in element.childNodes:
					if pack.nodeType == pack.ELEMENT_NODE and pack.localName == "package":
						self.deps.append(pack.childNodes[0].nodeValue)
			
	def outputScript(self):
		s = script.Script(self)
		s.make()
