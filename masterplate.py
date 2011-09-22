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
import buffercomponent

class Masterplate(object):
    # A master plate class . Holds the plate dictionary and methods to return static well instances 
#   alphas = map(chr, range(65, 73))
#   nums = [1,2,3,4,5,6,7,8,9,10,11,12]
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
        filename = str(filename)
        import pprint
        import csv
        #Check to see if there are more than 8 reagents - since hamilton deck holds only 8 reagents
        numplates = 0
        if len(well.Well.wellcomponentlist.componentfactory) > 8:
            numplates = len(well.Well.wellcomponentlist.componentfactory)/8 + 1
            print "Numplates is now" , numplates
        #print "Numplates" , numplates
        #Adding one in cases where there is only one list then range returns empty list
        file_suffixes_array = range(numplates + 1)
        fileroot , ext = os.path.splitext(str(filename))

        outfilehandles = []
        
        for suffix in file_suffixes_array:
            outfilehandles.append(csv.writer(open(r"%s_%s%s" % (fileroot,suffix + 1 ,ext),r"wb")))

    
        solvent_blocks = [well.Well.wellcomponentlist.componentfactory.keys()[i:i+8] for i in range(0,len(well.Well.wellcomponentlist.componentfactory),8)]
        #pprint.pprint(solvent_blocks)
        for current_solvent_name_list in solvent_blocks:
            current_handle = outfilehandles.pop(0)
            outrow = []
            outrow.append("Plate")
            outrow.append("index")

            for solvent in current_solvent_name_list:
                outrow.append(solvent)
            current_handle.writerow(outrow)

            
                # well.Well.wellcomponentlist.componentfactory is a dictionary of compound names given by user keys and corresponding component objects values
            for k in self.ordered_keys_hamilton:
                outrow = []
                outrow.append("Plate %s" % platenumber)
                outrow.append(k)
                # Hardcoding x index to first character : Not good idea if plate alphabet goes beyond Z to AB etc
                yplate = k[0]
                xplate = int(k[1:])
                #           print "Checking: %s, %s" % (yplate,xplate), 
                for solvent in current_solvent_name_list:
                    try:
                        outrow.append(int(round(self.getwell(yplate,xplate).wellcomponentdict[solvent])))
                    except KeyError, e:
                        outrow.append(0)
                current_handle.writerow(outrow)
            
            
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

    def write_csv_well_by_well(self,filename):
            f =  open(filename,"w")
            for y in self.alphas:
                for x in self.nums:
                    well = self.getwell(y,x)
                    stuffinthiswell = []
                    phcalcer = []
                    itms =  well.wellcomponentdict.items()
                    itms.sort()
                    for solvent,value  in itms:
                        conc = float(well.wellcomponentdict[solvent] * well.component_name_object_map[solvent].stockconc)/float(self.volofeachwell)
                        stuffinthiswell.append(",".join([str(conc),solvent]))
                    # For buffers put the computed pH
                        if isinstance(well.component_name_object_map[solvent],buffercomponent.SimpleBuffer):
                            phcalcer.append(well.component_name_object_map[solvent])
                            if len(phcalcer) == 2 :
                            # Calculate pH and then print to sheet
                                if phcalcer[0].pka != phcalcer[1].pka:
                                    pass
                                else:
                                    import math
                                    numerator = phcalcer[0].get_conc_base()*well.wellcomponentdict[phcalcer[0].name] + phcalcer[1].get_conc_base()*well.wellcomponentdict[phcalcer[1].name]
                                    denominator = phcalcer[0].get_conc_acid()*well.wellcomponentdict[phcalcer[0].name]+ phcalcer[1].get_conc_acid()*well.wellcomponentdict[phcalcer[1].name]
                                    ph = phcalcer[0].pka + math.log10(numerator/ denominator)
                                   # stuffinthiswell.append("PHCALCED")
                                    stuffinthiswell.append(str(ph))

                    f.write("%s%s" % (y,x) + ",") 
                    f.write(",".join(stuffinthiswell)+ "\n")
           

def main():
    sys.path.append("/Users/hari")
    import masterplate
    testplate = masterplate.Masterplate(2000,96)
    testplate.makefileforhamilton("masterplate_main",1)
    testplate.write_csv_well_by_well("masterplate_csv_well_by_well.csv")
#   testplate.printwellinfo()
    print testplate.get_style()
    testplate.writepdf("masterplate_main.pdf")
    pass


if __name__ == '__main__':
    main()

