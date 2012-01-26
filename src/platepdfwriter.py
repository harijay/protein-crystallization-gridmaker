# To change this template, choose Tools | Templates
# and open the template in the editor.



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch,mm
import buffercomponent, well

class Platepdfwriter():
    scale_mult_x = 3.5
    scale_mult_y = 1.6
    fontsize_to_fit = 6
    mydicts = {}
    alphas = ["A","B","C","D","E","F","G","H"]
    mynums = [1,2,3,4,5,6,7,8,9,10,11,12]

    def __init__(self,filename):
        self.filename = filename
        self.canvas_obj = canvas.Canvas(self.filename,pagesize=letter)
        
        self.canvas_obj.grid(self.make_listx(),self.make_listy())
        self.label_axes()
        self.canvas_obj.setFont("Times-Roman", self.fontsize_to_fit)


    def label_axes(self):
        count = 0
        cx = self.make_listx()
        cy = self.make_listy()

        for val in cx[:-1]:
            self.canvas_obj.rotate(90)
            self.canvas_obj.drawString(30,-40+(-val*0.35*mm),u"%s" %  self.alphas[count])
            count = count + 1
            self.canvas_obj.rotate(-90)
        count = 0
        for val in cy[:-1]:
            self.canvas_obj.rotate(90)
            self.canvas_obj.drawString(val+5*mm,-60,u"%s" %  self.mynums[count])
            count = count + 1
            self.canvas_obj.rotate(-90)


    def make_listx(self):
        xlist = []
        for i in range(9):
            xlist.append(inch*(i+1)*0.25*self.scale_mult_x)
    #    print xlist
        return xlist

    def make_listy(self):
        ylist = []
        for i in range(13):
            ylist.append(inch*(i+1)*0.5*self.scale_mult_y)
    #    print ylist
        return ylist

    def gen_lists(self,masterplate):
        vols = []
        for solvent in well.Well.wellcomponentlist.componentfactory:
            self.mydicts[solvent] = vols
            for y in masterplate.alphas:
		for x in masterplate.nums:
                    try:
                        vol = masterplate.getwell(y,x).wellcomponentdict[solvent]
                        self.mydicts[solvent].append("%s" % vol)
                    except KeyError, e:
                        self.mydicts[solvent].append("%s" % 0)
            vols = []
        print self.mydicts

    def gen_verbose_pdf(self,masterplate):
        pos = 1
        for solvent in well.Well.wellcomponentlist.componentfactory:
            if len (solvent) > 10:
                printed_solvent = "".join(solvent.split())[:10]
            else:
                printed_solvent = solvent 
            for y in self.make_listy()[:-1]:
                for x in self.make_listx()[:-1]:
                    xplate = masterplate.nums[self.make_listy().index(y)]
                    yplate = masterplate.alphas[self.make_listx().index(x)]
                    self.canvas_obj.rotate(90)
                    try:
                        self.canvas_obj.drawString(y+1*mm,-x-3*pos*mm,u"%s,%.1f\xB5l" % (printed_solvent,masterplate.getwell(yplate,xplate).wellcomponentdict[solvent]))
                    except KeyError, e:
                        self.canvas_obj.drawString(y+1*mm,-x-3*pos*mm,u"%s,%.1f\xB5l" % (printed_solvent,0))
                    self.canvas_obj.rotate(-90)
            pos = pos + 1
        self.canvas_obj.showPage()
        self.canvas_obj.save()
    def gen_pdf_human(self,masterplate):
        import os
        clabel_x = range(10,700,int(700/6))
        print clabel_x
        self.canvas_obj.rotate(90)
        self.canvas_obj.drawString(10,-10,"DispenseFilePrefix: %s" % str(os.path.splitext(self.filename)[0] ))
        self.canvas_obj.rotate(-90)
        pos = 1
        component_data_written = []
        component_poscount = 0
        newline = 0
        for y in self.make_listy()[:-1]:
            for x in self.make_listx()[:-1]:
                plate_num = masterplate.nums[self.make_listy().index(y)]
                plate_alpha = masterplate.alphas[self.make_listx().index(x)]
                mywell = masterplate.getwell(plate_alpha,plate_num)
                self.canvas_obj.rotate(90)
                count = 0
                phcalcer = []
                
                for solvent in sorted(mywell.wellcomponentdict.keys()):
                    count = count + 1
                    if len (solvent) > 10:
                        printed_solvent = "".join(solvent.split())[:10]
                    else:
                        printed_solvent = solvent
                    try:
                        current_component = mywell.component_name_object_map[solvent]
                        if  current_component not in component_data_written:
                            component_data_written.append(current_component)
                            try:
                                self.canvas_obj.setFont("Times-Roman", 5)
                                if component_poscount >= 6 :
                                    component_poscount = component_poscount - 6
                                    newline = 10

                                self.canvas_obj.drawString(clabel_x[component_poscount],-30 - newline,"Component:%s,%4.2f,%6.2f" % (current_component.name,current_component.stockconc,current_component.vol))
                                print newline,component_poscount,clabel_x[component_poscount],"Component:%s , %4.2f , %6.2f" % (current_component.name,current_component.stockconc,current_component.vol)
                                self.canvas_obj.setFont("Times-Roman", self.fontsize_to_fit)
                                component_poscount = component_poscount + 1
                            except IndexError, iex:
                                pass
                        else :
                            pass

                        conc = float(mywell.wellcomponentdict[solvent] * mywell.component_name_object_map[solvent].stockconc)/float(masterplate.volofeachwell)
                        self.canvas_obj.drawString(y+1*mm,-x-count*3.5*mm,u"%10s:  %-6.2f" % (printed_solvent,conc))
                    except KeyError , k:
                        pass


                    if solvent in mywell.component_name_object_map.keys():
                        if isinstance(mywell.component_name_object_map[solvent], buffercomponent.SimpleBuffer):
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
                                    count = count + 1
                                    self.canvas_obj.drawString(y+1*mm,-x-count*3.5*mm,"ph final:%.2f" % ph)
                    
#                for solvent in mywell.wellcomponentdict:
#                    print solvent,mywell.wellcomponentdict[solvent]
#                    print y+1*mm,x-4*pos*mm
#                    self.canvas_obj.drawString(y+1*mm,-x-4*pos*mm,u"%s,%.1f\xB5l" % (solvent,mywell.wellcomponentdict[solvent]))
#                    pos = pos + 1


                self.canvas_obj.rotate(-90)

        self.canvas_obj.showPage()
        self.canvas_obj.save()

    def gen_pdf(self,masterplate):
        pos = 1
        for y in self.make_listy()[:-1]:
            for x in self.make_listx()[:-1]:
                plate_num = masterplate.nums[self.make_listy().index(y)]
                plate_alpha = masterplate.alphas[self.make_listx().index(x)]
                mywell = masterplate.getwell(plate_alpha,plate_num)
                self.canvas_obj.rotate(90)
                count = 0
                phcalcer = []

                for solvent in sorted(mywell.wellcomponentdict.keys()):
                    count = count + 1
                    if len (solvent) > 10:
                        printed_solvent = "".join(solvent.split())[:10]
                    else:
                        printed_solvent = solvent
                    self.canvas_obj.drawString(y+1*mm,-x-count*3.5*mm,u"%s,%.1f\xB5l" % (printed_solvent,mywell.wellcomponentdict[solvent]))


                    if solvent in mywell.component_name_object_map.keys():
                        if isinstance(mywell.component_name_object_map[solvent], buffercomponent.SimpleBuffer):
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
                                    count = count + 1
                                    self.canvas_obj.drawString(y+1*mm,-x-count*3.5*mm,"ph final:%.2f" % ph)
#                for solvent in mywell.wellcomponentdict:
#                    print solvent,mywell.wellcomponentdict[solvent]
#                    print y+1*mm,x-4*pos*mm
#                    self.canvas_obj.drawString(y+1*mm,-x-4*pos*mm,u"%s,%.1f\xB5l" % (solvent,mywell.wellcomponentdict[solvent]))
#                    pos = pos + 1
                self.canvas_obj.rotate(-90)
            
        self.canvas_obj.showPage()
        self.canvas_obj.save()

    #    c.grid([inch, 2*inch, 3*inch, 4*inch], [0.5*inch, inch, 1.5*inch, 2*inch, 2.5*inch])


