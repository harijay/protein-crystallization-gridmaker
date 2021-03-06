#!/usr/bin/env python
# encoding: utf-8
"""
plate.py

Created by Hariharan Jayaram on 2009-01-25.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""

import plateliberror, buffercomponent, component, masterplate

class Plate(object):
    # The all singing all dancing plate class
    # To create a plate plate = Plate ("A1", "H12") creates a full 96 well plate
    # To create a smaller plate plate = Plate("A1", "D6").
    # Main methods used are in section   REFINED methods to fill components
    gridstart = None
    gridend = None
    numwells = None
    numalongalpha = None
    numalongnum = None
    xgradientlist = None

    def __init__(self,gridstart,gridend,masterplate):
        self.masterplate = masterplate
        self.gridstart = gridstart
        self.gridend = gridend
        self.gridminnum = int(self.gridstart[1:])
        self.gridmaxnum = int(self.gridend[1:])
        self.gridminalpha = self.gridstart[0]
        self.gridmaxalpha = self.gridend[0]
        self.alphas = self.masterplate.alphas[self.masterplate.alphas.index(self.gridminalpha):(self.masterplate.alphas.index(self.gridmaxalpha)+1)]
        self.nums = self.masterplate.nums[self.masterplate.nums.index(self.gridminnum):(self.masterplate.nums.index(self.gridmaxnum)+1)]
        self.calcnumwells()
        self.xgradientlist = []
        self.ygradientlist = []

    def calcnumwells(self):
        self.numalongalpha = ord(self.gridmaxalpha)-ord(self.gridminalpha)+1
        self.numalongnum = self.gridmaxnum - self.gridminnum + 1
        return self.numalongalpha * self.numalongnum

    def calcgradientalongnum(self,start,end):
        self.xgradientlist = []
        self.xgradientlist.append(start)
        wellstofill = self.numalongnum
        step = None
        try:
            step = float(end - start) / (wellstofill - 1)
        except ZeroDivisionError:
            # If the plate has no wells
            raise plateliberror.PlatelibException(
                "No wells in plate definition : Cannot dispense . Check plate definitions")
        i = start
        while len(self.xgradientlist) < (self.numalongnum-1):
            i = i + step
            self.xgradientlist.append(i)
        self.xgradientlist.append(end)

        return self.xgradientlist

    def specifygradientalongnum(self,list):
        self.xgradientlist = []
        # Specify the pergentages of peg required for the wells
        if len(list) < self.numalongnum:
            raise plateliberror.PlatelibException("Too few inputs in gradient along x list")
        else:
            self.xgradientlist = list
        return self.xgradientlist

    def calcgradientalongalpha(self,start,end):
        self.ygradientlist = []
        self.ygradientlist.append(start)
        wellstofill = self.numalongalpha
        step = float(end-start)/(wellstofill-1)
        i = start
        while len(self.ygradientlist)< (self.numalongalpha -1):
            i = i + step
            self.ygradientlist.append(i)
        self.ygradientlist.append(end)
        return self.ygradientlist

    def specifygradientalongalpha(self,list):
        self.ygradientlist = []
        # Specify the pergentages of peg required for the wells
        if len(list) < self.numalongalpha:
            raise plateliberror.PlatelibException("Too few inputs in gradient along y list")
        else:
            self.ygradientlist = list
        return self.ygradientlist

    def specifyconstantalongalpha(self,fixedvalue):
        self.ygradientlist = []
        self.calcgradientalongalpha(fixedvalue,fixedvalue)
        return self.ygradientlist

    def specifyconstantalongnum(self,fixedvalue):
        self.xgradientlist = []
        self.calcgradientalongnum(fixedvalue,fixedvalue)
        return self.xgradientlist

# Methods to write to the master plate dictionary	

    def pushtomasterplate(self,Component,start,end,gradientdirection):
        # Sets the well components in self.masterplate.platedict()

        if gradientdirection == "alongalpha":
            self.calcgradientalongalpha(start,end)
            for y in self.alphas:
                for x in self.nums:
                    welltofill = self.masterplate.getwell(y,x).addcomponent(Component,float(self.ygradientlist[self.alphas.index(str(y))]))
        if gradientdirection == "alongnum":
            self.calcgradientalongnum(start,end)
            for y in self.alphas:
                for x in self.nums:
                    welltofill = self.masterplate.getwell(y,x).addcomponent(Component,float(self.xgradientlist[self.nums.index(x)]))
        if gradientdirection == "constant":
            self.specifyconstantalongalpha(start)
            self.specifyconstantalongnum(start)
            for y in self.alphas:
                for x in self.nums:
                    welltofill = self.masterplate.getwell(y,x).addcomponent(Component,float(self.ygradientlist[self.alphas.index(str(y))]))

    def pushlisttomasterplate(self,Component,gradientlist,gradientdirection):
        if gradientdirection == "alongalpha":
            self.specifygradientalongalpha(gradientlist)
            for y in self.alphas:
                for x in self.nums:
                    welltofill = self.masterplate.getwell(y,x).addcomponent(Component,float(self.ygradientlist[self.alphas.index(str(y))]))

        if gradientdirection == "alongnum":
            self.specifygradientalongnum(gradientlist)
            for y in self.alphas:
                for x in self.nums:
                    welltofill = self.masterplate.getwell(y,x).addcomponent(Component,float(self.xgradientlist[self.nums.index(x)]))

#  REFINED methods to fill components 
    def push_component_to_row_on_masterplate(self,Component,finalconc,rowalpha):
        try:
            rowalpha = rowalpha[0]
        except Exception:
            raise plateliberror.PlatelibException("Specified plate index %s not in sub plate : cannot fill component to row" % rowalpha )
        if rowalpha not in self.alphas:
            raise plateliberror.PlatelibException("Specified plate alphabet index not in sub plate")
        self.specifyconstantalongnum(finalconc)
        for x in self.nums:
            welltofill = self.masterplate.getwell(rowalpha,x).addcomponent(Component,float(self.xgradientlist[self.nums.index(x)]))

    def push_component_uniform_to_masterplate(self,Component,finalconc):
        self.pushtomasterplate(Component,finalconc,finalconc,"constant")

    def constant_salt(self,Component,finalconc):
        self.pushtomasterplate(Component,finalconc,finalconc,"constant")

    def constant_concentration(self,Component,finalconc):
        self.pushtomasterplate(Component,finalconc,finalconc,"constant")

    def push_component_to_column_on_masterplate(self,Component,finalconc,columnnum):
        if columnnum not in self.nums:
            raise plateliberror.PlatelibException("Specified column number not in sub plate")
        self.specifyconstantalongalpha(finalconc)
        for y in self.alphas:
            welltofill = self.masterplate.getwell(y,columnnum).addcomponent(Component,float(self.ygradientlist[self.alphas.index(y)]))

    def push_buffer_to_column_on_masterplate(self,Component,finalconc,columnnum):
        self.push_component_to_column_on_masterplate(Component,finalconc,columnnum)


    def push_buffer_to_row_on_masterplate(self,Component,finalconc,rowalpha):
        self.push_component_to_row_on_masterplate(Component,finalconc,rowalpha)

    def push_gradient_start_stop_x(self,Component,start,stop):
        self.pushtomasterplate(Component,start,stop,"alongnum")

    def gradient_along_x(self,Component,start,stop):
        self.pushtomasterplate(Component,start,stop,"alongnum")

    def gradientlist_along_x(self,Component,gradientlist):
        self.pushlisttomasterplate(Component,gradientlist,"alongnum")

    def push_gradient_start_stop_y(self,masterplate,Component,start,stop):
        self.pushtomasterplate(Component,start,stop,"alongalpha")

    def gradient_along_y(self,Component,start,stop):
        self.pushtomasterplate(Component,start,stop,"alongalpha")

    def gradientlist_along_y(self,Component,gradientlist):
        self.pushlisttomasterplate(Component,gradientlist,"alongalpha")

    def push_gradient_list_x(self,Component,gradientlist):
        self.pushlisttomasterplate(Component,gradientlist,"alongnum")


    def push_gradient_list_y(self,Component,gradientlist):
        self.pushlisttomasterplate(Component,gradientlist,"alongalpha")


    def fill_water(self,Water):
        for y in self.alphas:
            for x in self.nums:
                welllist = self.masterplate.getwell(y,x).fillwithwater(Water)

    def fill_water_auto(self):
            WATER = component.Component("100.00 % Water",55.5,1000000)
            self.fill_water(WATER)

    def push_component_rowlist(self,Component,finalconc,row_list_alphas):
        for row in row_list_alphas:
            if row not in self.alphas:
                raise plateliberror.PlatelibException("Plate alphabet %s index in rowlist not in plate" % row)
            self.push_buffer_to_row_on_masterplate(Component,finalconc,row)

    def push_component_columnlist(self,Component,finalconc,column_list_nums):
        for col in column_list_nums:
            if col not in self.nums:
                raise plateliberror.PlatelibException("Plate numerical column %s from columnlist not in plate" % col)
            self.push_component_to_column_on_masterplate(Component,finalconc,col)

    def push_components_mapped_to_row(self,simple_component_list,finalconclist,row_list_alphas):
        if len(simple_component_list) == len(finalconclist) == len(row_list_alphas):
            for elem in range(len(simple_component_list)):
                try:
                    self.push_buffer_to_row_on_masterplate(simple_component_list[elem],finalconclist[elem],row_list_alphas[elem])
                except plateliberror.PlatelibException, pex:
                    newmessage = "Please carefully check lists for components , concentrations and row alphabets: %s" % pex.message
                    pex.message = newmessage
                    raise pex
        else:
            raise plateliberror.PlatelibException("Lists Unequal :Please carefully check lists for components , concentrations and row alphabets")

    def push_components_mapped_to_column(self,simple_component_list,finalconclist,col_list_nums):
        if len(simple_component_list) == len(finalconclist) == len(col_list_nums):
            for elem in range(len(simple_component_list)):
                try:
                    self.push_buffer_to_column_on_masterplate(simple_component_list[elem],finalconclist[elem],col_list_nums[elem])
                except plateliberror.PlatelibException, pex:
                    newmessage = "Please carefully check lists for components , concentrations and column numbers: %s" % pex.message
                    pex.message = newmessage
                    raise pex
        else:
            raise plateliberror.PlatelibException("Lists Unequal :Please carefully check lists for components , concentrations and column numbers")


    def ph_gradient_alongx(self,buffer1,buffer2,finalconc,startph,stopph):
        concentrations_buffer1= []
        concentrations_buffer2 = []
        for ph in self.calcgradientalongnum(startph,stopph):
            calcbuffer =  buffercomponent.SimpleBuffer("calcbuffer",1.0,buffer1.vol + buffer2.vol,ph,buffer1.pka)
            volume_ratios = buffer1.volumes_given_counter(buffer2,calcbuffer)
            vtotal = (finalconc*self.masterplate.volofeachwell)/calcbuffer.conc
            v1 = vtotal * volume_ratios[0]
            v2 = vtotal* volume_ratios[1]
            c1 = (v1*buffer1.stockconc)/self.masterplate.volofeachwell
            c2 = (v2*buffer2.stockconc)/self.masterplate.volofeachwell
            concentrations_buffer1.append(c1)
            concentrations_buffer2.append(c2)

        self.push_gradient_list_x(buffer1,concentrations_buffer1)
        self.push_gradient_list_x(buffer2,concentrations_buffer2)


    def ph_gradient_alongy(self,buffer1,buffer2,finalconc,startph,stopph):
        concentrations_buffer1= []
        concentrations_buffer2= []
        for ph in self.calcgradientalongalpha(startph,stopph):
            calcbuffer =  buffercomponent.SimpleBuffer("calcbuffer",1.0,buffer1.vol + buffer2.vol,ph,buffer1.pka)
            volume_ratios = buffer1.volumes_given_counter(buffer2,calcbuffer)
            vtotal = (finalconc*self.masterplate.volofeachwell)/calcbuffer.conc
            v1 = vtotal * volume_ratios[0]
            v2 = vtotal* volume_ratios[1]
            c1 = (v1*buffer1.stockconc)/self.masterplate.volofeachwell
            c2 = (v2*buffer2.stockconc)/self.masterplate.volofeachwell
            concentrations_buffer1.append(c1)
            concentrations_buffer2.append(c2)
        self.push_gradient_list_y(buffer1,concentrations_buffer1)
        self.push_gradient_list_y(buffer2,concentrations_buffer2)

    def ph_list_alongx(self,buffer1,buffer2,finalconc,phlist):
        concentrations_buffer1= []
        concentrations_buffer2= []
        for ph in phlist:
            calcbuffer =  buffercomponent.SimpleBuffer("calcbuffer",1.0,buffer1.vol + buffer2.vol,ph,buffer1.pka)
            volume_ratios = buffer1.volumes_given_counter(buffer2,calcbuffer)
            vtotal = (finalconc*self.masterplate.volofeachwell)/calcbuffer.conc
            v1 = vtotal * volume_ratios[0]
            v2 = vtotal* volume_ratios[1]
            c1 = (v1*buffer1.stockconc)/self.masterplate.volofeachwell
            c2 = (v2*buffer2.stockconc)/self.masterplate.volofeachwell
            concentrations_buffer1.append(c1)
            concentrations_buffer2.append(c2)

        self.push_gradient_list_x(buffer1,concentrations_buffer1)
        self.push_gradient_list_x(buffer2,concentrations_buffer2)

    def ph_list_alongy(self,buffer1,buffer2,finalconc,phlist):
        concentrations_buffer1= []
        concentrations_buffer2= []
        for ph in phlist:
            calcbuffer =  buffercomponent.SimpleBuffer("calcbuffer",1.0,buffer1.vol + buffer2.vol,ph,buffer1.pka)
            volume_ratios = buffer1.volumes_given_counter(buffer2,calcbuffer)
            vtotal = (finalconc*self.masterplate.volofeachwell)/calcbuffer.conc
            v1 = vtotal * volume_ratios[0]
            v2 = vtotal* volume_ratios[1]
            c1 = (v1*buffer1.stockconc)/self.masterplate.volofeachwell
            c2 = (v2*buffer2.stockconc)/self.masterplate.volofeachwell
            concentrations_buffer1.append(c1)
            concentrations_buffer2.append(c2)
        self.push_gradient_list_y(buffer1,concentrations_buffer1)
        self.push_gradient_list_y(buffer2,concentrations_buffer2)

    def maketo100_alongx(self,c1,c2,finalconc,startcomponent1,stopcomponent1):
        unequal_error = plateliberror.PlatelibException("unequal concentrations for %s and %s" % (c1.name , c2.name))
        if c1.stockconc != c2.stockconc:
            raise unequal_error
        concentrations_buffer1= []
        concentrations_buffer2= []
        totalsum = finalconc*self.masterplate.volofeachwell/c1.stockconc
        percent = totalsum/100.0
        for amt1 in self.calcgradientalongnum(startcomponent1,stopcomponent1):
            conc1=  amt1*c1.stockconc*percent/self.masterplate.volofeachwell
            conc2 = (100.0-amt1)*c2.stockconc*percent/self.masterplate.volofeachwell
            concentrations_buffer1.append(conc1)
            concentrations_buffer2.append(conc2)
        self.push_gradient_list_x(c1,concentrations_buffer1)
        self.push_gradient_list_x(c2,concentrations_buffer2)

    def maketo100_alongy(self,c1,c2,finalconc,startcomponent1,stopcomponent1):
        unequal_error = plateliberror.PlatelibException("unequal concentrations for %s and %s" % (c1.name , c2.name))
        if c1.stockconc != c2.stockconc:
            raise unequal_error
        concentrations_buffer1= []
        concentrations_buffer2= []
        totalsum = finalconc*self.masterplate.volofeachwell/c1.stockconc
        percent = totalsum/100.0
        for amt1 in self.calcgradientalongalpha(startcomponent1,stopcomponent1):
            conc1=  amt1*c1.stockconc*percent/self.masterplate.volofeachwell
            conc2 = (100.0-amt1)*c2.stockconc*percent/self.masterplate.volofeachwell
            concentrations_buffer1.append(conc1)
            concentrations_buffer2.append(conc2)
        self.push_gradient_list_y(c1,concentrations_buffer1)
        self.push_gradient_list_y(c2,concentrations_buffer2)

    def maketo100_listx(self,c1,c2,finalconc,listxcomponent1):
        unequal_error = plateliberror.PlatelibException("unequal concentrations for %s and %s" % (c1.name , c2.name))
        if c1.stockconc != c2.stockconc:
            raise unequal_error
        concentrations_buffer1= []
        concentrations_buffer2= []
        totalsum = finalconc*self.masterplate.volofeachwell/c1.stockconc
        percent = totalsum/100.0
        for amt1 in listxcomponent1:
            conc1=  amt1*c1.stockconc*percent/self.masterplate.volofeachwell
            conc2 = (100.0-amt1)*c2.stockconc*percent/self.masterplate.volofeachwell
            concentrations_buffer1.append(conc1)
            concentrations_buffer2.append(conc2)
        self.push_gradient_list_x(c1,concentrations_buffer1)
        self.push_gradient_list_x(c2,concentrations_buffer2)

    def maketo100_listy(self,c1,c2,finalconc,listycomponent1):
        unequal_error = plateliberror.PlatelibException("unequal concentrations for %s and %s" % (c1.name , c2.name))
        if c1.stockconc != c2.stockconc:
            raise unequal_error
        concentrations_buffer1= []
        concentrations_buffer2= []
        totalsum = finalconc*self.masterplate.volofeachwell/c1.stockconc
        percent = totalsum/100.0
        for amt1 in listycomponent1:
            conc1=  amt1*c1.stockconc*percent/self.masterplate.volofeachwell
            conc2 = (100.0-amt1)*c2.stockconc*percent/self.masterplate.volofeachwell
            concentrations_buffer1.append(conc1)
            concentrations_buffer2.append(conc2)
        self.push_gradient_list_y(c1,concentrations_buffer1)
        self.push_gradient_list_y(c2,concentrations_buffer2)

    def components_mapped_row(self,simple_component_list,finalconclist):
        self.push_components_mapped_to_column(simple_component_list,finalconclist,self.alphas)


    def components_mapped_column(self,simple_component_list,finalconclist):
        self.push_components_mapped_to_row(simple_component_list,finalconclist,self.nums)

    def gradient_list_to_row(self,component,concentration_list,row_alpha):
        if row_alpha not in self.alphas:
            raise plateliberror.PlatelibException("Row %s not in plate in gradient_list_to_row" % row_alpha)
        if len(concentration_list) == len(self.nums):
            for index,concentration in enumerate(concentration_list):
                column_num = self.nums[index]
                welltofill = self.masterplate.getwell(row_alpha,column_num).addcomponent(component,float(concentration))
        else:
            raise plateliberror.PlatelibException("Too few concentrations or mistake in plate definition for gradient_list_to_row")

    def gradient_list_to_column(self,component,concentration_list,column_num):
        if column_num not in self.nums:
            raise plateliberror.PlatelibException("Column %d not in plate in gradient_list_to_column" % column_num)
        if len(concentration_list) == len(self.alphas):
            for index,concentration in enumerate(concentration_list):
                row_alpha = self.alphas[index]
                welltofill = self.masterplate.getwell(row_alpha,column_num).addcomponent(component,float(concentration))
        else:
            raise plateliberror.PlatelibException("Wrong number of concentrations or wells in gradient_list_to_column")

    def gradient_list_to_multiple_columns(self,component,concentration_list,column_num_list):
        for column in column_num_list:
            if column not in self.nums:
                raise plateliberror.PlatelibException("Error in inputs to gradient_list_to_multiple_columns")
            else:
                self.gradient_list_to_column(component,concentration_list,column)

    def gradient_list_to_multiple_rows(self,component,concentration_list,row_alpha_list):
        for arow in row_alpha_list:
            if arow not in self.alphas:
                raise plateliberror.PlatelibException("Error in inputs to gradient_list_to_multiple_columns")
            else:
                self.gradient_list_to_row(component,concentration_list,arow)

    def buffer_single_ph_to_row_or_rows(self,buffer1,buffer2,concentration,pHdesired,rows):
        for a_row in rows:
            for a_column in self.nums:
                if a_row not in self.alphas:
                    raise plateliberror.PlatelibException("Illegal Row def: Check inputs to buffer single value to rows")
                else:
                    calcbuffer =  buffercomponent.SimpleBuffer("calcbuffer",1.0,buffer1.vol + buffer2.vol,pHdesired,buffer1.pka)
                    volume_ratios = buffer1.volumes_given_counter(buffer2,calcbuffer)
                    vtotal = (concentration*self.masterplate.volofeachwell)/calcbuffer.conc
                    v1 = vtotal * volume_ratios[0]
                    v2 = vtotal* volume_ratios[1]
                    concentration_buffer1 = (v1*buffer1.stockconc)/self.masterplate.volofeachwell
                    concentration_buffer2 = (v2*buffer2.stockconc)/self.masterplate.volofeachwell
                    welltofill = self.masterplate.getwell(a_row,a_column).addcomponent(buffer1,concentration_buffer1)
                    welltofill = self.masterplate.getwell(a_row,a_column).addcomponent(buffer2,concentration_buffer2)


    def buffer_single_ph_to_column_or_columns(self,buffer1,buffer2,concentration,pHdesired,columns):
        for a_column in columns:
            for a_row in self.alphas:
                if a_column not in self.nums:
                    raise plateliberror.PlatelibException("Illegal Column def. Check inputs to buffer single pH to columns")
                else:
                    calcbuffer =  buffercomponent.SimpleBuffer("calcbuffer",1.0,buffer1.vol + buffer2.vol,pHdesired,buffer1.pka)
                    volume_ratios = buffer1.volumes_given_counter(buffer2,calcbuffer)
                    vtotal = (concentration*self.masterplate.volofeachwell)/calcbuffer.conc
                    v1 = vtotal * volume_ratios[0]
                    v2 = vtotal* volume_ratios[1]
                    concentration_buffer1 = (v1*buffer1.stockconc)/self.masterplate.volofeachwell
                    concentration_buffer2 = (v2*buffer2.stockconc)/self.masterplate.volofeachwell
                    welltofill = self.masterplate.getwell(a_row,a_column).addcomponent(buffer1,concentration_buffer1)
                    welltofill = self.masterplate.getwell(a_row,a_column).addcomponent(buffer2,concentration_buffer2)

    def buffer_ph_to_single_well(self,buffer1,buffer2,concentration,pHdesired,alpha,num):
        calcbuffer =  buffercomponent.SimpleBuffer("calcbuffer",1.0,buffer1.vol + buffer2.vol,pHdesired,buffer1.pka)
        volume_ratios = buffer1.volumes_given_counter(buffer2,calcbuffer)
        vtotal = (concentration*self.masterplate.volofeachwell)/calcbuffer.conc
        v1 = vtotal * volume_ratios[0]
        v2 = vtotal* volume_ratios[1]
        concentration_buffer1 = (v1*buffer1.stockconc)/self.masterplate.volofeachwell
        concentration_buffer2 = (v2*buffer2.stockconc)/self.masterplate.volofeachwell
        welltofill = self.masterplate.getwell(alpha,num).addcomponent(buffer1,concentration_buffer1)
        welltofill = self.masterplate.getwell(alpha,num).addcomponent(buffer2,concentration_buffer2)


    def buffer_multiple_phs_to_single_row(self,buffer1,buffer2,concentration,ph_list,alpha):
        if len(ph_list) == len(self.nums):
            for index, ph in enumerate(ph_list):
                print index,alpha,self.nums[index]
                self.buffer_ph_to_single_well(buffer1,buffer2,concentration,ph,alpha,self.nums[index])
        else:
            raise plateliberror.PlatelibException("Illegal argument in buffer_multiple_phs_to_single_row")

    def buffer_multiple_phs_to_single_column(self,buffer1,buffer2,concentration,ph_list,num):
        if  len(ph_list) == len(self.alphas):
            for index,ph in enumerate(ph_list):
                self.buffer_ph_to_single_well(buffer1,buffer2,concentration,ph,self.alphas[index],num)
        else:
            raise plateliberror.PlatelibException("Illegal argument in buffer_multiple_phs_to_single_column")

    def buffer_ph_list_to_multiple_rows(self,buffer1,buffer2,concentration,ph_list,alpha_list):
        if len(ph_list) != len(self.nums):
            raise plateliberror.PlatelibException("Check buffer ph List to multiple rows, improper number of pHs")
        for row in alpha_list:
            self.buffer_multiple_phs_to_single_row(buffer1,buffer2,concentration,ph_list,row)

    def bufffer_ph_list_to_multiple_columns(self,buffer1,buffer2,concentration,ph_list,num_list):
        if len(ph_list) != len(self.alphas):
            raise plateliberror.PlatelibException("Check buffer ph List to multiple columns, improper number of pHs")
        for column in num_list:
            self.buffer_multiple_phs_to_single_column(buffer1,buffer2,concentration,ph_list,column)

def main():
    peg400 = component.Component("peg400",60,500000)
    salt1 = component.Component("NH42SO4",1000,100000)
    salt2 = component.Component("CaCl2",2000,100000)
    salt3 = component.Component("CaAc2",1000,100000)
    salt4 = component.Component("MgCl2",2000,100000)
    magic = component.Component("Magic",2,1000000)
    water = component.Component("water",100,100000)
    magic2 = component.Component("Magic2",40000,1000000)
    magic3 = component.Component("Magic3",50000,1000000)
    magic4 = component.Component("Magic4",50000,1000000)

    water = component.Component("water",100,100000)
    mp = masterplate.Masterplate(2000)
    p1 = Plate("A1","D6",mp)
    p2 = Plate("A7","D12",mp)
    p3 = Plate("E1","H6",mp)
    p4 = Plate("E7","H12",mp)
    pwhole = Plate("A1","H12",mp)

    # Fill the salts :
    p1.push_component_uniform_to_masterplate(salt1,100)
    p2.push_component_uniform_to_masterplate(salt2,200)
    p3.push_component_uniform_to_masterplate(salt3,100)
    p4.push_component_uniform_to_masterplate(salt4,200)
    pwhole.gradient_list_to_row(magic,[0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12],"C")
    pwhole.gradient_list_to_column(magic2,[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8],3)
    pwhole.gradient_list_to_multiple_columns(magic3,[1,2,3,4,5,6,7,8],[1,5,7])
    pwhole.gradient_list_to_multiple_rows(magic4,[1,2,3,4,5,6,7,8,9,10,11,12],["A","F"])

    # Fill the buffers :
    buffertrislow = buffercomponent.SimpleBuffer("trisph7.5",1.0,100000,7.5,8.03)
    buffertrishigh = buffercomponent.SimpleBuffer("trisph8.5",1.0,100000,9.0,8.03)
#    p1.ph_list_alongx(buffertrislow,buffertrishigh,0.1,[7.7,7.8,7.9,8.0,8.1,8.2])
#    p2.ph_list_alongx(buffertrislow,buffertrishigh,0.1,[7.7,7.8,7.9,8.0,8.1,8.2])
#    p3.ph_list_alongx(buffertrislow,buffertrishigh,0.1,[7.7,7.8,7.9,8.0,8.1,8.2])
#    p4.ph_list_alongx(buffertrislow,buffertrishigh,0.1,[7.7,7.8,7.9,8.0,8.1,8.2])
#
#    pwhole.buffer_single_ph_to_columns(buffertrislow,buffertrishigh,0.1,7.7,[1])
#    pwhole.buffer_single_ph_to_columns(buffertrislow,buffertrishigh,0.1,7.8,[2])

    pwhole.buffer_ph_list_to_multiple_rows(buffertrishigh,buffertrislow,0.1,[7.5 + x/12.0 for x in range(12)],["A","D"])

    # Setup the peg gradients
    p1.push_gradient_list_y(peg400,[25,30,38,45])
    p2.push_gradient_list_y(peg400,[25,30,38,45])
    p3.push_gradient_list_y(peg400,[25,30,38,45])
    p4.push_gradient_list_y(peg400,[25,30,38,45])

#    t1 = component.Component("tb1",2.0,100000)
#    t2 = component.Component("tb2",2.0,10000)
#    p1.maketo100_alongx(t1,t2,0.1,30,80)

    # Water top up
    p1.fill_water(water)
    p2.fill_water(water)
    p3.fill_water(water)
    p4.fill_water(water)
    mp.printwellinfo()
    mp.printsolventlistsnapshot()
    mp.printpdfhuman("testmagic")
    mp.makefileforformulatrix("afterplatemod.dl.txt")


if __name__ == '__main__':
    main()

