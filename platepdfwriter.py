# To change this template, choose Tools | Templates
# and open the template in the editor.



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch,mm
import well

class Platepdfwriter():
    scale_mult_x = 3.5
    scale_mult_y = 1.6
    fontsize_to_fit = 6
    mydicts = {}

    def __init__(self,filename):
        self.filename = filename + ".pdf"

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

    def gen_pdf(self,masterplate):
        self.gen_lists(masterplate)
        canvas_obj = canvas.Canvas(self.filename,pagesize=letter)
        canvas_obj.grid(self.make_listx(),self.make_listy())
        canvas_obj.setFont("Times-Roman", self.fontsize_to_fit)
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
                    canvas_obj.rotate(90)
                    try:
                        canvas_obj.drawString(y+1*mm,-x-3*pos*mm,u"%s,%.1f\xB5l" % (printed_solvent,masterplate.getwell(yplate,xplate).wellcomponentdict[solvent]))
                    except KeyError, e:
                        canvas_obj.drawString(y+1*mm,-x-3*pos*mm,u"%s,%.1f\xB5l" % (printed_solvent,0))
                    canvas_obj.rotate(-90)
            pos = pos + 1
        canvas_obj.showPage()
        canvas_obj.save()
    #    c.grid([inch, 2*inch, 3*inch, 4*inch], [0.5*inch, inch, 1.5*inch, 2*inch, 2.5*inch])

