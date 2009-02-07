#!/usr/bin/env python
# encoding: utf-8
"""
well.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""

import sys
import os
import component
import componentlist
import plateliberror
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
		
	def deplete(self,vol):
		self.volleft = self.volleft - vol
		if self.volleft < 0:
			raise plateliberror.PlatelibException("Well volume exceeded")
				
	def addcomponent(self,Component,finalconc):
		key = Component.name
		if key not in Well.wellcomponentlist.componentfactory:
			Well.wellcomponentlist.addcomponent(Component)
		voltoadd = (self.vol * finalconc)/(Component.stockconc)
#		print "Adding %s of\t%s to well %s,%s get a conc of\t%s" % (voltoadd,Component.name,self.alpha,self.num,finalconc)
		Component.deplete(voltoadd)
		self.wellcomponentdict[Component.name] = voltoadd
		self.deplete(voltoadd)

	def calctotalvol(self):
		total = 0
		for i in self.wellcomponentdict:
			total = total + self.wellcomponentdict[i] 
		return total
		
	def about(self):
		aboutstr = "WELL: %s%s \t" % (self.alpha , self.num)
		total = self.calctotalvol()
		for i in self.wellcomponentdict:
			aboutstr = aboutstr + "Component %s : %3.3f " % (i,self.wellcomponentdict[i]) +  "Total:%s" % total 
		return aboutstr
	
		
	def fillwithwater(self,Component):
		key = Component.name
		newname = "100.00 % Water"
		if key != "100.00 % Water":
			Component.name = newname
			
		if key not in Well.wellcomponentlist.componentfactory:
			Well.wellcomponentlist.addcomponent(Component)
		self.wellcomponentdict[Component.name] = self.volleft
	
		
	def getmastercomponentlist(self):
		return Well.wellcomponentlist
			
def main():
	w = Well("A",1,2000)
	rack = w.getmastercomponentlist()
	c1 = component.Component("peg400",50,100)
	rack.addcomponent(c1)
	
	c2 = component.Component("CaCl2",2000,100000)
	rack.addcomponent(c2)
	
	c = rack.getcomponent("CaCl2")
	
	w.addcomponent(c,200)
	x = w.about()
	print x

	print "Volume of %s left:%s" % (c.name,c.getmls()) 
	rack.listcontents()
if __name__ == '__main__':
	main()

