#!/usr/bin/env python
# encoding: utf-8
"""
well.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""

import plateliberror, component, componentlist

class Well(object):
    # A well class that modifies itself by adding components and reports to the
    # Componentlist when any component is added
    # well.about is a tostring() method
    wellcomponentlist = componentlist.ComponentList()
    def __init__(self,alpha,num,vol):
        self.alpha = alpha
        self.num = num
        self.components = []
        self.vol = vol
        self.wellcomponentdict = {}
        self.volleft = vol
        self.component_name_object_map = {}

    def deplete(self,vol,Component):
        """Deplete removes the available volume from the Well total volume."""
        self.volleft = self.volleft - vol
        if "100.00 % Water" in self.wellcomponentdict.keys():
            raise plateliberror.PlatelibException("Well volume exceeded when trying to add component to Well: %s%s. But you have already Added water.Please Add water last to prevent this\n" % (self.alpha,self.num))
        if round(self.volleft) < 0:
            raise plateliberror.PlatelibException("""Well volume exceeded when trying to add component %s to Well: %s%s. Increase concentration of stock for any component and retry""" %(Component.name,self.alpha,self.num))

    def addcomponent(self,Component,finalconc):
        key = Component.name
        if key not in Well.wellcomponentlist.componentfactory:
            Well.wellcomponentlist.insertcomponent(Component)
        if key in self.wellcomponentdict:
            #If a component has already been added to well . Then repeating additing will mess up concentration intended
            inconsistent_conc_warning = plateliberror.PlatelibException("Component %s already dispensed into Well:%s,%s: Inconsistent concentrations will result from Repeat DISPENSE.Please check plate configuration or combine both additions into one" % (Component.name,self.alpha,self.num))
            raise inconsistent_conc_warning
        voltoadd = (self.vol * finalconc)/(Component.stockconc)
        #		print "Adding %s of\t%s to well %s,%s get a conc of\t%s" % (voltoadd,Component.name,self.alpha,self.num,finalconc)
        Component.deplete(voltoadd)
        self.wellcomponentdict[Component.name] = voltoadd
        self.deplete(voltoadd,Component)
        self.components.append(Component.name)
        self.component_name_object_map[Component.name] = Component

    def calctotalvol(self):
        total = 0
        for i in self.wellcomponentdict:
            total = total + self.wellcomponentdict[i]
        return total

    def about(self):
        aboutstr = "WELL:%s%s\t" % (self.alpha , self.num)
        total = self.calctotalvol()
        for i in self.wellcomponentdict:
            aboutstr = aboutstr + "Component %s : %3.3f " % (i,self.wellcomponentdict[i]) +  "Total:%s" % total
        return aboutstr


    def fillwithwater(self,Component):
        key = Component.name
        newname = "100.00 % Water"
        if key != "100.00 % Water":
            Component.name = newname
        if self.volleft == 0:
            # If the well is already full Do nothing
            pass
        else:
            if key not in Well.wellcomponentlist.componentfactory:
                Well.wellcomponentlist.insertcomponent(Component)
            self.wellcomponentdict[Component.name] = self.volleft
            self.component_name_object_map[Component.name] = Component
            # Fixed Bug when other components were added after Water : and self.volleft was not calling deplete to
            # update self.volleft
            # Alternative approach call self.deplete(self.volleft)
            self.volleft = 0


    def getmastercomponentlist(self):
        return Well.wellcomponentlist

def main():
    w = Well("A",1,2000)
    rack = w.getmastercomponentlist()
    c1 = component.Component("peg400",50,100)
    rack.insertcomponent(c1)

    c2 = component.Component("CaCl2",2000,100000)
    rack.insertcomponent(c2)

    c = rack.getcomponent("CaCl2")

    w.addcomponent(c,200)

    c3 = component.Component("LowCaCl2",5,1000000)
    w.addcomponent(c3,45)
    x = w.about()
    print x

    print "Volume of %s left:%s" % (c.name,c.getmls())
    rack.listcontents()

if __name__ == '__main__':
    main()

