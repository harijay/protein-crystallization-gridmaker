# To change this template, choose Tools | Templates
# and open the template in the editor.



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import reportlab.lib.pagesizes as pagesizes
from reportlab.lib.units import inch,mm,cm
import buffercomponent, component, plate, masterplate,platepdfwriter
from platepdfwriter import Platepdfwriter as oldpdf

class PlateLandscapewriter():
    fontsize_to_fit = 6
    def __init__(self,filename):
        self.filename = r"%s" % filename
        self.myold = oldpdf(self.filename)
        self.canvas_obj = canvas.Canvas(self.filename,pagesize=pagesizes.landscape(letter))
        self.canvas_obj.grid(self.make_listx(),self.make_listy())
        self.canvas_obj.setFont("Times-Roman", self.fontsize_to_fit)
        self.label_axes()

    def make_listx(self):
        return self.myold.make_listy()

    def make_listy(self):
        return self.myold.make_listx()

    def label_axes(self):
        count = 0
        labelposnumx = []
        labelposnumy = 8*inch
        self.canvas_obj.setFont("Times-Roman",12)

        for i in range(12):
             labelposnumx.append(3.0*cm + 2.0*i*cm)

        labelposalphax = 1.1*cm
        labelposalphay = []

        for i in range(8):
            labelposalphay.append(3.3*cm + 2.2*i*cm)
        count = 0

        for labelindex in labelposnumx:
            self.canvas_obj.drawString(labelindex,labelposnumy,u"%s" %  self.myold.mynums[count])
            count = count + 1
            
        count  = 0
        
        backwardalphas = self.myold.alphas[::-1]
        for labelalpha in labelposalphay:
            self.canvas_obj.drawString(labelposalphax,labelalpha,u"%s" %  backwardalphas[count])
            count = count + 1

        self.canvas_obj.setFont("Times-Roman", self.fontsize_to_fit)

    def gen_pdf_human(self,masterplate):
        masterplate = masterplate
        import os,datetime
        self.canvas_obj.drawString(55,38,"DispenseFilePrefix: %s" % str(os.path.splitext(self.filename)[0] ))
        self.canvas_obj.drawString(55,30,"%s" % datetime.datetime.now().ctime())
        pos = 1

        for x in self.make_listx()[:-1]:
            for y in self.make_listy()[:-1]:
                backwardalphas = masterplate.alphas[::-1]
                ind_num = masterplate.nums[self.make_listx().index(x)]
                ind_alpha = backwardalphas[self.make_listy().index(y)]
                self.canvas_obj.drawString(x,y,u"%s" % (ind_alpha + str(ind_num)))
                mywell = masterplate.getwell(ind_alpha,ind_num)
                count = 0
                phcalcer = []
                spacing = 0 
                # Total components to be written into this well is
                total_components = len(mywell.wellcomponentdict.keys())
                try :
                    spacing = 2.0*cm/total_components
                except ZeroDivisionError, z:
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
                            self.canvas_obj.drawString(x+0.5*mm,y+count*spacing,u"%-10s:%-4.3f" % (printed_solvent,conc))
                    except KeyError, h:
                        pass
        
                    try:
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
                                    self.canvas_obj.drawString(x+5*mm,y+0.5*mm,u"%4s : %2.2f" % ("pH final",ph))
                    except KeyError, k:
                        pass
#        self.canvas_obj.showPage()
        self.canvas_obj.save()

    def gen_pdf(self,masterplate):
        masterplate = masterplate
        import os,datetime
        self.canvas_obj.drawString(55,38,"DispenseFilePrefix: %s" % str(os.path.splitext(self.filename)[0] ))
        self.canvas_obj.drawString(55,30,"%s" % datetime.datetime.now().ctime())
        pos = 1
        solvent_object_list = []


        for x in self.make_listx()[:-1]:
            for y in self.make_listy()[:-1]:
                backwardalphas = masterplate.alphas[::-1]
                ind_num = masterplate.nums[self.make_listx().index(x)]
                ind_alpha = backwardalphas[self.make_listy().index(y)]
                self.canvas_obj.drawString(x,y,u"%s" % (ind_alpha + str(ind_num)))
                mywell = masterplate.getwell(ind_alpha,ind_num)
                count = 0
                phcalcer = []
                spacing = 0
                wellvol = 0.0
                # Total components to be written into this well is
                total_components = len(mywell.wellcomponentdict.keys())
                try :
                    spacing = 2.0*cm/(total_components+1)
                except ZeroDivisionError , z :
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
                        self.canvas_obj.drawString(x+0.5*mm,y+count*spacing,u"%s, %.1f\xB5l" % (printed_solvent,mywell.wellcomponentdict[solvent]))
                        wellvol = wellvol + mywell.wellcomponentdict[solvent]
                        if mywell.component_name_object_map[solvent] not in solvent_object_list:
                            solvent_object_list.append(mywell.component_name_object_map[solvent])
                    except KeyError, h:
                        pass

                    try:
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
                                    self.canvas_obj.drawString(x+5*mm,y+0.5*mm,u"%4s : %2.2f" % ("pH final",ph))
                    except KeyError, k:
                        pass

                self.canvas_obj.drawString(x + 5*mm,y+(count+1)*spacing,u"Total: %.1f\xB5l" % wellvol)
        solvent_spacing = 10.5*inch / len(solvent_object_list)
        for x in range(len(solvent_object_list)):
            self.canvas_obj.drawString(55+ x*solvent_spacing,22,u"%s: %.1f\xB5l" %(solvent_object_list[x].name,masterplate.get_vol_component_used(solvent_object_list[x])))

#        self.canvas_obj.showPage()
        self.canvas_obj.save()

if __name__=="__main__":
    atest = PlateLandscapewriter("ldtest.pdf")
    mp = masterplate.Masterplate(2000)

    # Define each plate with the left corner well and right corner well . Feed the plate its containing master plate i.e
    pwhole = plate.Plate("A1","H12",mp)
    p = plate.Plate("A1","D6",mp)
    p2 = plate.Plate("A7","D12",mp)
    p3 = plate.Plate("E1","H6",mp)
    p4 = plate.Plate("E7","H12",mp)

    # Define a component with concentration  units that you keep constant for this component. i.e
    # if you use percent then you remember to use percent everytime you want to dispense this component

    peg400 = component.Component("peg400",50,100000)

    # Now we will lay down a peg gradient along the x axis
    p.gradient_along_x(peg400,18,25)
    p2.gradient_along_x(peg400,18,25)
    p3.gradient_along_x(peg400,18,25)
    p4.gradient_along_x(peg400,18,25)


    # Now lets define each buffer component

    b1 = component.Component("Arginine",1000,100000)
    b2 = component.Component("CaCl2-dihydrate",1000,100000)
    b3 = component.Component("Samarium",1000,100000)
    b4 = component.Component("Argentum",1000,100000)

    # Now we use the rather wordy push_buffer_to_row_on_masterplate method to populate with buffer for each row
    # In example3 you will see the shortcut methods for the same procedure. Also the push_component_to_column_on_masterplate(self,masterplate,Component,finalconc,columnnum) from the
    # plate.Plate class will do the same except for the column instead of row

    p.push_buffer_to_row_on_masterplate(b1,100,"A")
    p.push_buffer_to_row_on_masterplate(b2,100,"B")
    p.push_buffer_to_row_on_masterplate(b3,100,"C")
    p.push_buffer_to_row_on_masterplate(b4,100,"D")

    p2.push_buffer_to_row_on_masterplate(b1,100,"A")
    p2.push_buffer_to_row_on_masterplate(b2,100,"B")
    p2.push_buffer_to_row_on_masterplate(b3,100,"C")
    p2.push_buffer_to_row_on_masterplate(b4,100,"D")

    p3.push_buffer_to_row_on_masterplate(b1,100,"E")
    p3.push_buffer_to_row_on_masterplate(b2,100,"F")
    p3.push_buffer_to_row_on_masterplate(b3,100,"G")
    p3.push_buffer_to_row_on_masterplate(b4,100,"H")

    p4.push_buffer_to_row_on_masterplate(b1,100,"E")
    p4.push_buffer_to_row_on_masterplate(b2,100,"F")
    p4.push_buffer_to_row_on_masterplate(b3,100,"G")
    p4.push_buffer_to_row_on_masterplate(b4,100,"H")

    salt = component.Component("CaAc2",1000,100000)

    # Finally we add a constant salt additive to the entire sub plate. Plate 1 has 25 mM , plate 2 , 50 mM , plate 3 , 100 mM , and plate 4 ,150 mM
    # This method is also called plate.Plate.constant_salt(self,masterplate,Component,finalconc):
    # so you could very well say p.constant_salt(salt,25)

    p.push_component_uniform_to_masterplate(salt,25)
    p2.push_component_uniform_to_masterplate(salt,50)
    p3.push_component_uniform_to_masterplate(salt,100)
    p4.push_component_uniform_to_masterplate(salt,150)



    water = component.Component("100.00% Water",1000,300000)

    buffer1 = buffercomponent.SimpleBuffer("pH 7.0",0.5,100000,7.0,8.4)
    buffer2 = buffercomponent.SimpleBuffer("ph 8.0",0.5,100000,8.2,8.4)
    crap6 = component.Component("aga5trg",100,100000)
    pwhole.ph_gradient_alongy(buffer1,buffer2,0.1,7.2,8.0)

    p.fill_water(water)
    p2.fill_water(water)
    p3.fill_water(water)
    p4.fill_water(water)
    p4.fill_water(water)




    
#    atest.gen_pdf_human(mp)
    atest.gen_pdf(mp)
#    atest.canvas_obj.showPage()
    atest.canvas_obj.save()
