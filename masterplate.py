#!/usr/bin/env python
# encoding: utf-8
"""
masterplate.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""
import os.path

import sys

import well
import csv
import pdfwriterlandscape
import   awarepdfwriter
class Masterplate(object):
	# A master plate class . Holds the plate dictionary and methods to return static well instances 
#	alphas = map(chr, range(65, 73))
#	nums = [1,2,3,4,5,6,7,8,9,10,11,12]
	ordered_keys = []
	ordered_keys_hamilton = []
	welldict = {}
	volofeachwell = None
	
	def __init__(self,volofeachwell,style=96):
		Masterplate.volofeachwell = volofeachwell
                self.alphadict = {96 : map(chr,range(65,73)),\
                                  24 : map(chr,range(65,69)),\
                                 384 : map(chr,range(65,81))}
                self.numdict = {96: range(1,13,1),24:range(1,7,1),384:range(1,25,1)}
                self.alphas = self.alphadict[style]
                self.nums = self.numdict[style]
		for a in self.alphas:
			for i in self.nums:
				key = "%s" % a + "%s" % i
				self.ordered_keys.append(key)
				self.welldict[key] = well.Well(a,i,Masterplate.volofeachwell)
		for i in self.nums:
			for a in self.alphas:
				key = "%s" % a + "%s" % i
				self.ordered_keys_hamilton.append(key)
		print self.ordered_keys_hamilton
				
	def getwell(self,alpha,num):
		key = "%s" % alpha + "%s" % num
		return self.welldict[key]

        def get_style(self):
            return len(self.nums) * len(self.alphas)
		
	def printwellinfo(self):
		for k in self.ordered_keys :
			print self.welldict[k].about()
			
	def makefileforhamilton(self,filename,platenumber=1):
		import pprint
		import csv
		outrow = []
		outrow.append("Plate")
		outrow.append("index")
		outfile_handle = outfile = open(r"%s" % str(filename),r"wb")
		outfile = csv.writer(outfile)
		for solvent in well.Well.wellcomponentlist.componentfactory:
			outrow.append(solvent)
		outfile.writerow(outrow)
		# well.Well.wellcomponentlist.componentfactory is a dictionary of compound names given by user keys and corresponding component objects values
		for k in self.ordered_keys_hamilton:
			outrow = []
			outrow.append("Plate %s" % platenumber)
			outrow.append(k)
			# Hardcoding x index to first character : Not good idea if plate alphabet goes beyond Z to AB etc
			yplate = k[0]
			xplate = int(k[1:])
#			print "Checking: %s, %s" % (yplate,xplate), 
			for solvent in well.Well.wellcomponentlist.componentfactory:
				try:
					outrow.append(int(round(self.getwell(yplate,xplate).wellcomponentdict[solvent])))
				except KeyError, e:
					outrow.append(0)
			outfile.writerow(outrow)
			
			
	def printsolventlistsnapshot(self):
		self.getwell("A",1).getmastercomponentlist().listcontents()


	def makefileforformulatrix(self,filename):
                import os
                if ".dl.txt" in filename:
#                    print filename
#                    print "Writing filename: %s" % filename
                    pass
                else:
                    filename = "".join(os.path.splitext(filename)[0] + ".dl.txt")
                    print "Writing filename: %s" % filename
					
					
		outfile = open(r"%s" % str(filename),r"wb")
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
            if "pdf" in filename:
                pass
            else:
                filename = "".join([os.path.splitext(filename)[0],".pdf"])
            outfile = "%s_volumes.pdf" % filename
            mypdf = pdfwriterlandscape.PlateLandscapewriter(filename)
            mypdf.gen_pdf(self)

        def printpdfhuman(self,filename):
            if "pdf" in filename:
                pass
            else:
                filename = "".join([os.path.splitext(filename)[0],".pdf"])
            outfile = "%s.pdf" % filename
            mypdf = pdfwriterlandscape.PlateLandscapewriter(filename)
            mypdf.gen_pdf_human(self)

        def writepdf(self,filename):
            if "pdf" in filename:
                pass
            else:
                filename = "".join([os.path.splitext(filename)[0],".pdf"])
            pdf = awarepdfwriter.Pdfwriter(filename)
            pdf.gen_pdf(self)


        def get_vol_component_used(self,component):
            solventvol = 0
            if component.name not in well.Well.wellcomponentlist.componentfactory:
                raise plateliberror.PlatelibException("Component %s not used in plate" % component.name)
            else:
                for y in self.alphas:
                    for x in self.nums:
                        try:
                            vol = self.getwell(y,x).wellcomponentdict[component.name]
                            solventvol = solventvol + vol
                        except KeyError, e:
                            pass
            return solventvol

        def write_csv_well_by_well(self):
            f =  open("testingcsv.csv","w")
            for y in self.alphas:
                for x in self.nums:
                    well = self.getwell(y,x)
                    stuffinthiswell = []
                    for solvent,value  in well.wellcomponentdict.items():
                        conc = float(well.wellcomponentdict[solvent] * well.component_name_object_map[solvent].stockconc)/float(self.volofeachwell)
                        stuffinthiswell.append(",".join([solvent,str(conc)]))
                    f.write("%s%s" % (y,x) + ",") 
                    f.write(",".join(stuffinthiswell)+ "\n")
        

def main():
	sys.path.append("/Users/hari")
	import masterplate
	testplate = masterplate.Masterplate(2000,96)
	testplate.makefileforhamilton("masterplate_main",1)
	
#	testplate.printwellinfo()
        print testplate.get_style()
        testplate.writepdf("masterplate_main.pdf")
	pass


if __name__ == '__main__':
	main()

