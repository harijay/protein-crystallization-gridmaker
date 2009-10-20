# To change this template, choose Tools | Templates
# and open the template in the editor.
import reportlab
from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes as pagesizes
from reportlab.lib.units import inch,mm,cm
from reportlab.lib.pagesizes import letter
import masterplate,well,component,buffercomponent,plate
import os,datetime

class Pdfwriter():

    def __init__(self,filename):
        self.filename = filename

        self.canvas = reportlab.pdfgen.canvas.Canvas(self.filename,pagesize =pagesizes.landscape(letter) )
        self.alphadict = {96 : map(chr,range(65,73))[::-1],\
             24 : map(chr,range(65,69))[::-1],\
             384 : map(chr,range(65,81))[::-1]}

    def optimum_font_grid_label(self,style):
        fontsizedict = {24:10,96:10,384:6}
        return fontsizedict[style]

    def optimum_font_well_text(self,style):
        fontsizedict = {24:10,96:6,384:3}
        return fontsizedict[style]

    def optimum_font_axes_label(self,style):
        fontsizedict = {24:12,96:10,384:5}
        return fontsizedict[style]

    def xlabel_centering_offset(self,style):
        offsetdict =  {24:2*mm,96:3*mm,384:2*mm}
        return offsetdict[style]

    def ylabel_centering_offset(self,style):
        offsetdict =  {24:0*mm,96:0*mm,384:0*mm}
        return offsetdict[style]

    def optimum_component_info_fontsize(self,numbercomponents):
        return 14 - numbercomponents

    def make_grid(self,style=96):
        self.style = style
        xoffset = 0.5*inch
        yoffset = 0.7*inch

        self.xgrid = []
        self.ygrid = []
        hsplitdict = {24:6,96:12,384:24}
        vsplitdict =  {24:4,96:8,384:16}

        nums = range(1,25,1)

        hspacing = (10.0/hsplitdict[style])*inch
        vspacing = (7.0/vsplitdict[style])*inch

        # Split x coords 6 times for 24 well,  12 times for 96 and 24 times for 96
        for x in range(0,(hsplitdict[style])+1,1):
            xcoord = xoffset + x*hspacing
            self.xgrid.append(xcoord)
    

        for y in range(0,(vsplitdict[style])+1,1):
            ycoord = yoffset + y*vspacing
            self.ygrid.append(ycoord)

        self.canvas.grid(self.xgrid,self.ygrid)
        

        for x in self.xgrid[:-1]:
            for y in self.ygrid[:-1]:
                label = "%s%s" % (self.alphadict[style][self.ygrid.index(y)],self.xgrid.index(x)+1)
                self.canvas.setFont("Times-Roman", self.optimum_font_grid_label(style))
                self.canvas.drawString(x+0.2*mm,y+0.2*mm,label)

        self.canvas.drawString(self.xgrid[0],40,"DispenseFilePrefix: %s" % str(os.path.splitext(self.filename)[0] ))
        self.canvas.drawString(self.xgrid[0],30,"%s" % datetime.datetime.now().ctime())

        labelxoffset = ((self.xgrid[2] - self.xgrid[1])/2) -self.xlabel_centering_offset(style)

        self.canvas.setFont("Times-Roman", self.optimum_font_axes_label(style))
        
        for i,x in enumerate(self.xgrid[:-1]):
            self.canvas.drawString(self.xgrid[i] + labelxoffset, 7.9*inch,"%s" % (i + 1))


        labelyoffset = ((self.ygrid[2] - self.ygrid[1])/2) -self.ylabel_centering_offset(style)

        for i,y in enumerate(self.ygrid[:-1]):
            self.canvas.drawString(0.2*inch,self.ygrid[i] + labelyoffset,"%s" % self.alphadict[style][self.ygrid.index(y)])


    def make_volumes_page(self,masterplate):
        # Make the grid
        self.make_grid(masterplate.get_style())
        solvent_object_list = []
        totalvertspace= self.ygrid[2]-self.ygrid[1]
        totalhorizspace = self.xgrid[2]-self.xgrid[1]
        self.canvas.setFont("Times-Roman", self.optimum_font_well_text(masterplate.get_style()))
        for x in self.xgrid[:-1]:
            for y in self.ygrid[:-1]:
                aindex = self.alphadict[masterplate.get_style()][self.ygrid.index(y)]
                numindex = self.xgrid.index(x)+1
                mywell = masterplate.getwell(aindex,numindex)
                count = 0
                phcalcer = []
                wellvol = 0.0
                # Total components to be written into this well is
                total_components = len(mywell.wellcomponentdict.keys())
                try :
                    spacing = totalvertspace/(total_components+2)
                except ZeroDivisionError , z :
                    spacing = 0
                    pass

                for solvent in sorted(mywell.wellcomponentdict.keys())[::-1]:
                    count = count + 1
                    if len (solvent) > 10:
                        printed_solvent = "".join(solvent.split())[:10]
                    else:
                        printed_solvent = solvent
                    try:
#                        print mywell.wellcomponentdict[solvent] , mywell.component_name_object_map[solvent].stockconc , masterplate.volofeachwell
                        conc = float(mywell.wellcomponentdict[solvent] * mywell.component_name_object_map[solvent].stockconc)/float(masterplate.volofeachwell)
                        self.canvas.drawString(x+0.5*mm,y+count*spacing,u"%s, %.1f\xB5l" % (printed_solvent,mywell.wellcomponentdict[solvent]))
                        wellvol = wellvol + mywell.wellcomponentdict[solvent]
                        if mywell.component_name_object_map[solvent] not in solvent_object_list:
                            solvent_object_list.append(mywell.component_name_object_map[solvent])
                    except KeyError, h:
                        pass

                    try:
                        if isinstance(mywell.component_name_object_map[solvent],buffercomponent.SimpleBuffer):
                            phcalcer.append(mywell.component_name_object_map[solvent])
                            if len(phcalcer) == 2 :
                            # Calculate pH and then print to sheet
                                if phcalcer[0].pka != phcalcer[1].pka:
                                    pass
                                else:
                                    import math
                                    numerator = phcalcer[0].get_conc_base()*mywell.wellcomponentdict[phcalcer[0].name] + phcalcer[1].get_conc_base()*mywell.wellcomponentdict[phcalcer[1].name]
                                    denominator = phcalcer[0].get_conc_acid()*mywell.wellcomponentdict[phcalcer[0].name]+ phcalcer[1].get_conc_acid()*mywell.wellcomponentdict[phcalcer[1].name]
                                    ph = phcalcer[0].pka + math.log10(numerator/ denominator)
                                    self.canvas.drawString(x+totalhorizspace/3,y+(count+1)*spacing,u"%4s : %2.2f" % ("pH final",ph))
                                    count = count + 1
                    except KeyError, k:
                        pass

                self.canvas.drawString(x+totalhorizspace/3,y+ spacing/20,u"Total: %.1f\xB5l" % wellvol)
        solvent_string = []

        for x in range(len(solvent_object_list)):
            solvent_string.append(u"%s C:%s Use:%.1f\xB5l " %(solvent_object_list[x].name,solvent_object_list[x].stockconc,masterplate.get_vol_component_used(solvent_object_list[x])))
        self.canvas.setFont("Times-Roman", self.optimum_component_info_fontsize(len(solvent_object_list)))
        self.canvas.drawString(self.xgrid[0],20,"  ,  ".join(solvent_string))
#        self.canvas_obj.showPage()
        self.canvas.showPage()

    def make_concentrations_page(self,masterplate):
        self.make_grid(masterplate.get_style())
        totalvertspace= self.ygrid[2]-self.ygrid[1]
        totalhorizspace = self.xgrid[2]-self.xgrid[1]
        self.canvas.setFont("Times-Roman", self.optimum_font_well_text(masterplate.get_style()))
        for x in self.xgrid[:-1]:
            for y in self.ygrid[:-1]:
                aindex = self.alphadict[masterplate.get_style()][self.ygrid.index(y)]
                numindex = self.xgrid.index(x)+1
                mywell = masterplate.getwell(aindex,numindex)
                count = 0
                phcalcer = []
                spacing = 0
                # Total components to be written into this well is
                total_components = len(mywell.wellcomponentdict.keys())
                try :
                    spacing = totalvertspace/(total_components+2)
                except ZeroDivisionError , z :
                    spacing = 0
                    pass
                for solvent in sorted(mywell.wellcomponentdict.keys())[::-1]:
                    count = count + 1
                    if len (solvent) > 10:
                        printed_solvent = "".join(solvent.split())[:10]
                    else:
                        printed_solvent = solvent
                    try:
                        if "100.00 % Water" not in mywell.component_name_object_map[solvent].name:
                            conc = float(mywell.wellcomponentdict[solvent] * mywell.component_name_object_map[solvent].stockconc)/float(masterplate.volofeachwell)
                            self.canvas.drawString(x+0.5*mm,y+count*spacing,u"%-10s:%-4.3f" % (printed_solvent,conc))
                    except KeyError, h:
                        pass

                    try:
                        if isinstance(mywell.component_name_object_map[solvent],buffercomponent.SimpleBuffer):
                            phcalcer.append(mywell.component_name_object_map[solvent])
                            if len(phcalcer) == 2 :
                            # Calculate pH and then print to sheet
                                if phcalcer[0].pka != phcalcer[1].pka:
                                    pass
                                else:
                                    import math
                                    numerator = phcalcer[0].get_conc_base()*mywell.wellcomponentdict[phcalcer[0].name] + phcalcer[1].get_conc_base()*mywell.wellcomponentdict[phcalcer[1].name]
                                    denominator = phcalcer[0].get_conc_acid()*mywell.wellcomponentdict[phcalcer[0].name]+ phcalcer[1].get_conc_acid()*mywell.wellcomponentdict[phcalcer[1].name]
                                    ph = phcalcer[0].pka + math.log10(numerator/ denominator)
                                    self.canvas.drawString(x+totalhorizspace/3,y+(count+1)*spacing,u"%4s : %2.2f" % ("pH final",ph))
                                    count = count + 1
                    except KeyError, k:
                        pass
        self.canvas.showPage()
        
    def gen_pdf(self,masterplate):
        self.make_volumes_page(masterplate)
        self.make_concentrations_page(masterplate)
        self.canvas.save()
                
if __name__=="__main__":
    c = Pdfwriter("multipagestyle.pdf")
    
    plateindexdict = {24:("A1","D6"),96:("A1","H12"),384:("A1","P24")}

    for style in [24,96,384]:
        a,i = plateindexdict[style]
        m = masterplate.Masterplate(2000,style)
        p = plate.Plate(a,i,m)
        cacl2 = component.Component("CaCl2",3,3000000)
        w = component.Component("100.00 % Water",55.5,5000000)
        b1 = buffercomponent.SimpleBuffer("tris pH 7.2" , 1,1000000,7.2,8.1)
        b2 = buffercomponent.SimpleBuffer("tris pH 8.0" , 1,1000000,8.0,8.1)
        p.gradient_along_x(component.Component("peg400",50,500000),22,35)
        p.ph_gradient_alongy(b1, b2, 0.1, 7.3, 8.0)
        p.gradient_along_x(cacl2,0.1,0.3)
        p.fill_water(w)
        c.gen_pdf(m)
   


