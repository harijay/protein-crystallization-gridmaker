#!/usr/bin/env python
# encoding: utf-8
"""
masterplate.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""

import sys

import well
import csv
import platepdfwriter

class Masterplate(object):
	# A master plate class . Holds the plate dictionary and methods to return static well instances 
	alphas = map(chr, range(65, 73))
	nums = [1,2,3,4,5,6,7,8,9,10,11,12]
	ordered_keys = []
	welldict = {}
	volofeachwell = None
	
	def __init__(self,volofeachwell):
		Masterplate.volofeachwell = volofeachwell
		for a in self.alphas:
			for i in self.nums:
				key = "%s" % a + "%s" % i
				self.ordered_keys.append(key)
				self.welldict[key] = well.Well(a,i,Masterplate.volofeachwell)
				
	def getwell(self,alpha,num):
		key = "%s" % alpha + "%s" % num
		return self.welldict[key]
		
	def printwellinfo(self):
		for k in self.ordered_keys :
			print self.welldict[k].about()
	
	def printsolventlistsnapshot(self):
		self.getwell("A",1).getmastercomponentlist().listcontents()
	
	def makefileforformulatrix(self,filename):
		outfile = open("%s" % filename,"wb")
		tabwriter = csv.writer(outfile,dialect=csv.excel_tab)
		header = []
		header.extend(["DeepWell.pd.txt","",""])
		tabwriter.writerow(header)
		#outfile.write("\n")
		solventline = []
		for solvent in well.Well.wellcomponentlist.componentfactory:
			solventline.extend(["%s" % solvent,"",""])
			for y in self.alphas:
				for x in self.nums:
					try:
						vol = self.getwell(y,x).wellcomponentdict[solvent] 		
						solventline.append("%s" % vol)
					except KeyError, e:
						solventline.append("%s" % int(0))
			tabwriter.writerow(solventline)
			solventline = []			
			#outfile.write("\n")
		outfile.close()

        def printpdf(self,filename):
            outfile = "%s.pdf" % filename
            mypdf = platepdfwriter.Platepdfwriter(filename)
            mypdf.gen_pdf(self)


def main():
	sys.path.append("/Users/hari")
	import gridder
	from gridder import masterplate
	testplate = masterplate.Masterplate(2000)
	testplate.printwellinfo()
	pass


if __name__ == '__main__':
	main()

