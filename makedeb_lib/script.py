# -*- coding: utf-8 -*-

import os

class Script:
	def __init__(self, project):
		"""
			Défini les éléments du script
		"""
		# Variables
		# Fichiers
		self.files = project.files
		# Tableau des répertoires à créer
		self.dirs = project.dirs
		# Dépendances
		self.deps = project.deps
		# Version du paquet
		self.version = project.version
		# Nom
		self.name = project.name
		# Maintener, mail, homepage
		self.maintener = project.maintener
		self.mail = project.mail
		self.homepage = project.homepage
		# Description
		self.desc = project.desc
		# Categorie
		self.category = project.category
		# pre|post inst et rm
		self.preinst = project.preinst
		self.postinst = project.postinst
		self.prerm = project.prerm
		self.postrm = project.postrm
		
		self.script = "#!/bin/bash\n\n"
	
	def makeComments(self):
		self.script += "# Automatic script to generate the debian package\n"
		"# For the program libluawrap\n\n"

	def makeVariables(self):
		self.script += "# General variables used for the script\n"
		self.script += "name=\"" + self.name + "\"\n"
		self.script += "version=" + self.version + "\n"
		self.script += "maintener=\"" + self.maintener + "\"\n"
		self.script += "mail=\"" + self.mail + "\"\n"
		self.script += "desc=\"" + self.desc + "\"\n"
		self.script += "homepage=\"" + self.homepage + "\"\n"
		self.script += "category=" + self.category + "\n"
		self.script += "temp=deb-pkg-tmp\n"
		self.script += "size=0\n"
		self.script += "deps="
		for i in range(0, len(self.deps)):
			if i == 0:
				self.script += self.deps[0]
			else:
				self.script += "," + self.deps[i]
		self.script += "\n\n"
		
	def makeSize(self):
		for i in self.files:
			self.script += "if ! [ -e \"" + i[0] + "\" ]; then echo \"Error, file " + i[0] + " missing, aborting.\";rm -rf $temp; exit -1; fi;\n"
			self.script += "let \"size=$size+`du --block-size=1 \"" + i[0] + "\" | awk '{print $1;}'`\"\n"
		self.script += "let \"ts=$size/1024\"\n\n"
	
	def makeControl(self):
		self.script += "mkdir -p $temp/DEBIAN\n"
		self.script += "control=$temp/DEBIAN/control\n"
		self.script += "touch $control\n"
		self.script += "echo -e \"Package: $name\" > $control\n"
		self.script += "echo -e \"Version: $version\" >> $control\n"
		self.script += "echo -e \"Section: base\" >> $control\n"
		self.script += "echo -e \"Priority: optional\" >> $control\n"
		self.script += "echo -e \"Architecture: all\" >> $control\n"
		self.script += "echo -e \"Depends: bash,$deps\" >> $control\n"
		self.script += "echo -e \"Maintainer: $maintener\" >> $control\n"
		self.script += "echo -e \"Description: $desc\" >> $control\n"
		self.script += "echo -e \"Installed-Size: $ts\" >> $control\n"
		self.script += "echo -e \"Homepage: $homepage\" >> $control\n"
		self.script += "\n"
		
		# Si les fichiers pre|post inst et rm sont spécifiés
		if self.preinst != "":
			self.script += "cp " + self.preinst + " ${temp}/DEBIAN/preinst\n"
		if self.postinst != "":
			self.script += "cp " + self.postinst + " ${temp}/DEBIAN/postinst\n"
		if self.prerm != "":
			self.script += "cp " + self.prerm + " ${temp}/DEBIAN/prerm\n"
		if self.postrm != "":
			self.script += "cp " + self.postrm + " ${temp}/DEBIAN/postrm\n\n"
		
	def makeClean(self):
		self.script += "if [ \"$1\" = \"--clean\" ]; then\n"
		self.script += "	echo \"Cleaning...\"\n"
		self.script += "	echo \" * $temp\"\n"
		self.script += "	rm -rf $temp\n"
		self.script += "	echo \" * ${name}${version}.deb\"\n"
		self.script += "	rm -rf ${name}${version}.deb\n"
		self.script += "	echo \" * $0\"\n"
		self.script += "	rm -rf $0\n"
		self.script += "	exit\n"
		self.script += "fi\n\n"
	
	def makeDirs(self):
		for i in self.dirs:
			self.script += "mkdir -p ${temp}" + i + "\n"
		self.script += "\n"
	
	def makeFiles(self):
		for i in self.files:
			self.script += "cp -r " + i[0] + " ${temp}" + i[1] + "\n"
		self.script += "\n"
	
	def finalize(self):
		self.script += "dpkg-deb --build $temp " + self.name + self.version + ".deb >> " + self.name + ".log\n"
		self.script += "rm -r $temp " + self.name + ".log\n"
		self.script += "echo ${name}${version}.deb generated."
	
	def make(self):
		self.makeComments()
		self.makeVariables()
		self.makeClean()
		self.makeSize()
		self.makeControl()
		self.makeDirs()
		self.makeFiles()
		self.finalize()
		
		s = open(self.name + "_makedeb.sh", 'w')
		s.write(self.script.encode('utf-8','ignore'))
		s.close()
		
		os.chmod(self.name + "_makedeb.sh", 0744)
		print "Executing the script..."
		os.execl(self.name + "_makedeb.sh", "")
