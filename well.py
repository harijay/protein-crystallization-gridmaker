#!/usr/bin/env python
# encoding: utf-8
"""
well.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import component
import componentlist
import plateliberror
class Well(object):

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
		voltoadd = (self.vol * finalconc)/(Component.stockconc)
		Component.deplete(voltoadd)
		self.wellcomponentdict[Component.name] = voltoadd
		self.deplete(voltoadd)
		
	def about(self):
		aboutstr = "WELL: %s%s \t" % (self.alpha , self.num)
		for i in self.wellcomponentdict:
			aboutstr = aboutstr + "Component %s : %3.3f " % (i,self.wellcomponentdict[i])
		return aboutstr
		
	def fillwithwater(self,Component):
		self.wellcomponentdict[Component.name] = self.volleft
		
def main():
	w = Well("A",1,2000)
	rack = componentlist.ComponentList()
	
	c1 = component.Component("peg400",50,100)
	rack.addcomponent(c1)
	
	c2 = component.Component("CaCl2",2000,100000)
	rack.addcomponent(c2)
	
	c = rack.getcomponent("CaCl2")
	
	w.addcomponent(c,200)
	x = w.about()
	print x

	print "Volume of %s left:%s" % (c.name,c.getmls()) 

if __name__ == '__main__':
	main()

