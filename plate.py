#!/usr/bin/env python
# encoding: utf-8
"""
plate.py

Created by Hariharan Jayaram on 2009-01-25.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""

import sys
import os
import plateliberror
import masterplate
import component

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
		self.gridstart = gridstart
		self.gridend = gridend
		self.gridminnum = int(self.gridstart[1:])
		self.gridmaxnum = int(self.gridend[1:])
		self.gridminalpha = self.gridstart[0]
		self.gridmaxalpha = self.gridend[0]		
		self.alphas = masterplate.alphas[masterplate.alphas.index(self.gridminalpha):(masterplate.alphas.index(self.gridmaxalpha)+1)]
		self.nums = masterplate.nums[masterplate.nums.index(self.gridminnum):(masterplate.nums.index(self.gridmaxnum)+1)]
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
		step = float(end-start)/wellstofill
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
		step = float(end-start)/wellstofill
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

	def pushtomasterplate(self,masterplate,Component,start,end,gradientdirection):
		# Sets the well components in masterplate.platedict()
		
		if gradientdirection == "alongalpha":
			self.calcgradientalongalpha(start,end)
			for y in self.alphas:
				for x in self.nums:
					welltofill = masterplate.getwell(y,x).addcomponent(Component,float(self.ygradientlist[self.alphas.index(str(y))]))
		if gradientdirection == "alongnum":
			self.calcgradientalongnum(start,end)
			for y in self.alphas:
				for x in self.nums:
					welltofill = masterplate.getwell(y,x).addcomponent(Component,float(self.xgradientlist[self.nums.index(x)]))
		if gradientdirection == "constant":
			self.specifyconstantalongalpha(start)
			self.specifyconstantalongnum(start)
			for y in self.alphas:
				for x in self.nums:
					welltofill = masterplate.getwell(y,x).addcomponent(Component,float(self.ygradientlist[self.alphas.index(str(y))]))
	
	def pushlisttomasterplate(self,masterplate,Component,gradientlist,gradientdirection):
		if gradientdirection == "alongalpha":
			self.specifygradientalongalpha(gradientlist)
			for y in self.alphas:
				for x in self.nums:
					welltofill = masterplate.getwell(y,x).addcomponent(Component,float(self.ygradientlist[self.alphas.index(str(y))]))
					
		if gradientdirection == "alongnum":
			self.specifygradientalongnum(gradientlist)
			for y in self.alphas:
				for x in self.nums:
					welltofill = masterplate.getwell(y,x).addcomponent(Component,float(self.xgradientlist[self.nums.index(x)]))

#  REFINED methods to fill components 
	def push_component_to_row_on_masterplate(self,masterplate,Component,finalconc,rowalpha):
		rowalpha = rowalpha[0]
		if rowalpha not in self.alphas:
			raise plateliberror.PlatelibExtension("Specified plate alphabet index not in sub plate")
		self.specifyconstantalongnum(finalconc)
		for x in self.nums:
			welltofill = masterplate.getwell(rowalpha,x).addcomponent(Component,float(self.xgradientlist[self.nums.index(x)]))
		
	def push_component_uniform_to_masterplate(self,masterplate,Component,finalconc):
		self.pushtomasterplate(masterplate,Component,finalconc,finalconc,"constant")				

	def push_component_to_column_on_masterplate(self,masterplate,Component,finalconc,columnnum):
		if columnnum not in self.nums:
			raise plateliberror.PlatelibExtension("Specified column number not in sub plate")
		self.specifyconstantalongalpha(finalconc)
		for y in self.alphas:
			welltofill = masterplate.getwell(y,columnnum).addcomponent(Component,float(self.ygradientlist[self.alphas.index(y)])) 
	
	def push_buffer_to_column_on_masterplate(self,masterplate,Component,finalconc,columnnum):
		self.push_component_to_column_on_masterplate(masterplate,Component,finalconc,columnnum)

	
	def push_buffer_to_row_on_masterplate(self,masterplate,Component,finalconc,rowalpha):
		self.push_component_to_row_on_masterplate(masterplate,Component,finalconc,rowalpha)
	
	def push_gradient_start_stop_x(self,masterplate,Component,start,stop):
		self.pushtomasterplate(masterplate,Component,start,stop,"alongnum")
	
	def push_gradient_start_stop_y(self,masterplate,Component,start,stop):
		self.pushtomasterplate(masterplate,Component,start,stop,"alongalpha")
	
	def push_gradient_list_x(self,masterplate,Component,gradientlist):
		self.pushlisttomasterplate(masterplate,Component,gradientlist,"alongnum")
	
	def push_gradient_list_y(self,masterplate,Component,gradientlist):
		self.pushlisttomasterplate(masterplate,Component,gradientlist,"alongalpha")

	def fill_water(self,masterplate,Water):
		for y in self.alphas:
			for x in self.nums:
				welllist = masterplate.getwell(y,x).fillwithwater(Water)

def main():
	peg400 = component.Component("peg400",60,500000)
	salt1 = component.Component("NH42SO4",1000,100000)
	salt2 = component.Component("CaCl2",2000,100000)
	salt3 = component.Component("CaAc2",1000,100000)
	salt4 = component.Component("MgCl2",2000,100000)
	water = component.Component("water",100,100000)
	ph4p5 = component.Component("ph4.5",1000,100000)
	ph5p5 = component.Component("ph5.5",1000,100000)
	ph6p5 = component.Component("ph6.5",1000,100000)
	ph7p5 = component.Component("ph7.5",1000,100000)
	ph8p5 = component.Component("ph8.5",1000,100000)
	ph9p5 = component.Component("ph9.5",1000,100000)
	water = component.Component("water",100,100000)
	mp = masterplate.Masterplate(2000)
	p1 = Plate("A1","D6",mp)
	p2 = Plate("A7","D12",mp)
	p3 = Plate("E1","H6",mp)
	p4 = Plate("E7","H12",mp)
	
	# Fill the salts :
	p1.push_component_uniform_to_masterplate(mp,salt1,100)
	p2.push_component_uniform_to_masterplate(mp,salt2,200)
	p3.push_component_uniform_to_masterplate(mp,salt3,100)
	p4.push_component_uniform_to_masterplate(mp,salt4,200)
	
	# Fill the buffers :
	p1.push_buffer_to_column_on_masterplate(mp,ph4p5,100,1)
	p2.push_buffer_to_column_on_masterplate(mp,ph4p5,100,7)
	p3.push_buffer_to_column_on_masterplate(mp,ph4p5,100,1)
	p4.push_buffer_to_column_on_masterplate(mp,ph4p5,100,7)

	p1.push_buffer_to_column_on_masterplate(mp,ph5p5,100,2)
	p2.push_buffer_to_column_on_masterplate(mp,ph5p5,100,8)
	p3.push_buffer_to_column_on_masterplate(mp,ph5p5,100,2)
	p4.push_buffer_to_column_on_masterplate(mp,ph5p5,100,8)
	
	p1.push_buffer_to_column_on_masterplate(mp,ph6p5,100,3)
	p2.push_buffer_to_column_on_masterplate(mp,ph6p5,100,9)
	p3.push_buffer_to_column_on_masterplate(mp,ph6p5,100,3)
	p4.push_buffer_to_column_on_masterplate(mp,ph6p5,100,9)
	
	p1.push_buffer_to_column_on_masterplate(mp,ph7p5,100,4)
	p2.push_buffer_to_column_on_masterplate(mp,ph7p5,100,10)
	p3.push_buffer_to_column_on_masterplate(mp,ph7p5,100,4)
	p4.push_buffer_to_column_on_masterplate(mp,ph7p5,100,10)
	
	p1.push_buffer_to_column_on_masterplate(mp,ph8p5,100,5)
	p2.push_buffer_to_column_on_masterplate(mp,ph8p5,100,11)
	p3.push_buffer_to_column_on_masterplate(mp,ph8p5,100,5)
	p4.push_buffer_to_column_on_masterplate(mp,ph8p5,100,11)
	
	p1.push_buffer_to_column_on_masterplate(mp,ph9p5,100,6)
	p2.push_buffer_to_column_on_masterplate(mp,ph9p5,100,12)
	p3.push_buffer_to_column_on_masterplate(mp,ph9p5,100,6)
	p4.push_buffer_to_column_on_masterplate(mp,ph9p5,100,12)
		
	# Setup the peg gradients
	p1.push_gradient_list_y(mp,peg400,[25,30,38,45])
	p2.push_gradient_list_y(mp,peg400,[25,30,38,45])
	p3.push_gradient_list_y(mp,peg400,[25,30,38,45])
	p4.push_gradient_list_y(mp,peg400,[25,30,38,45])
	
	# Water top up 
	p1.fill_water(mp,water)
	p2.fill_water(mp,water)
	p3.fill_water(mp,water)
	p4.fill_water(mp,water)
	mp.printwellinfo()
	mp.printsolventlistsnapshot()
	mp.makefileforformulatrix()
	
	
if __name__ == '__main__':
	main()

