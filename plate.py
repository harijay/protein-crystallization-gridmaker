#!/usr/bin/env python
# encoding: utf-8
"""
plate.py

Created by Hariharan Jayaram on 2009-01-25.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import plateliberror
import masterplate
import component

class Plate(object):
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
		if len(list) < self.numalongnum:
			raise plateliberror.PlatelibException("Too few inputs in gradient along x list")
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
	
	def pushtomasterplate(self,masterplate,Component,start,end,gradientdirection):
		# Sets the well components in masterplate.platedict()
		
		if gradientdirection == "alongalpha":
			self.calcgradientalongalpha(start,end)
			for x in self.alphas:
				for y in self.nums:
					welltofill = masterplate.getwell(x,y).addcomponent(Component,float(self.ygradientlist[self.alphas.index(str(x))]))
		if gradientdirection == "alongnum":
			self.calcgradientalongnum(start,end)
			for x in self.alphas:
				for y in self.nums:
					welltofill = masterplate.getwell(x,y).addcomponent(Component,float(self.xgradientlist[self.nums.index(y)]))
		if gradientdirection == "constant":
			self.specifyconstantalongalpha(start)
			self.specifyconstantalongnum(start)
			for x in self.alphas:
				for y in self.nums:
					welltofill = masterplate.getwell(x,y).addcomponent(Component,float(self.ygradientlist[self.alphas.index(str(x))]))
	
	def pushtomasterlisttoplate(self,masterplate,Component,gradientlist,gradientdirection):
		if gradientdirection == "alongalpha":
			self.specifygradientalongalpha(gradientlist)
			for x in self.alphas:
				for y in self.nums:
					welltofill = masterplate.getwell(x,y).addcomponent(Component,float(self.ygradientlist[self.alphas.index(str(x))]))
					
		if gradientdirection == "alongnum":
			self.specifygradientalongnum(gradientlist)
			for x in self.alphas:
				for y in self.nums:
					welltofill = masterplate.getwell(x,y).addcomponent(Component,float(self.xgradientlist[self.nums.index(y)]))
			
					
def main():
	peg = component.Component("peg400",60,100000)
	salt1 = component.Component("CaCl2",2000,100000)
	salt2 = component.Component("NH42SO4",1000,100000)
	salt3 = component.Component("CaAc2",1000,100000)
	salt4 = component.Component("MgCl2",1000,100000)
	water = component.Component("water",100,100000)
	ph4p5 = component.Component("ph4.5",1000,100000)
	ph5p5 = component.Component("ph5.5",1000,100000)
	ph6p5 = component.Component("ph6.5",1000,100000)
	ph7p5 = component.Component("ph7.5",1000,100000)
	ph8p5 = component.Component("ph8.5",1000,100000)
	ph9p5 = component.Component("ph9.5",1000,100000)
	
	mp = masterplate.Masterplate(2000)
#	p = Plate("A1","D6",mp)
#	print "number of wells in plate" , p.calcnumwells()
#	x=p.calcgradientalongnum(20,26)
#	print x
	p = Plate("A1","D6",mp)
#	x=p.calcgradientalongnum(20,26)
#	print x
	p.pushtomasterplate(mp,salt1,200,200,"constant")
#	p2 = Plate("A1","D6",mp)
	p.pushtomasterplate(mp,peg,20,35,"alongalpha")
	p.pushtomasterplate(mp,peg,100,100,"gradientxlist")
	p.pushtomasterlisttoplate(mp,ph4p5,[100,0,0,0,0,0],"alongnum")
	p.pushtomasterlisttoplate(mp,ph5p5,[0,100,0,0,0,0],"alongnum")
	p.pushtomasterlisttoplate(mp,ph6p5,[0,0,100,0,0,0],"alongnum")
	p.pushtomasterlisttoplate(mp,ph7p5,[0,0,0,100,0,0],"alongnum")
	p.pushtomasterlisttoplate(mp,ph8p5,[0,0,0,0,100,0],"alongnum")
	p.pushtomasterlisttoplate(mp,ph9p5,[0,0,0,0,0,100],"alongnum")
#	p.pushtomasterplate(mp,salt1,200,200,"constant")
	
	p2 = Plate("A7","D12",mp)
	p2.pushtomasterplate(mp,peg,20,35,"alongalpha")
	p2.pushtomasterplate(mp,peg,100,100,"gradientxlist")
	p2.pushtomasterlisttoplate(mp,ph4p5,[100,0,0,0,0,0],"alongnum")
	p2.pushtomasterlisttoplate(mp,ph5p5,[0,100,0,0,0,0],"alongnum")
	p2.pushtomasterlisttoplate(mp,ph6p5,[0,0,100,0,0,0],"alongnum")
	p2.pushtomasterlisttoplate(mp,ph7p5,[0,0,0,100,0,0],"alongnum")
	p2.pushtomasterlisttoplate(mp,ph8p5,[0,0,0,0,100,0],"alongnum")
	p2.pushtomasterlisttoplate(mp,ph9p5,[0,0,0,0,0,100],"alongnum")
	# x=p.specifyconstantalongalpha(36)
	# 	psdfvd = Plate("A1","D3",mp)
	# 	x=psdfvd.calcgradientalongnum(20,50)
	# 	print x
	# 	x = psdfvd.specifygradientalongnum([20,22,24,26,28,30])
	# 	print x
	# 	p = Plate("A1","D6",mp)
	# 	x=p.calcgradientalongalpha(22,30)
	# 	for item in x:
	# 		print item
#	p = Plate("A6","D12",mp)
#	p.pushtomasterplate(mp,peg,20,26,"alongalpha")
#	p.pushtomasterplate(mp,salt2,200,200,"alongalpha")
	mp.printwellinfo()
	# 	
	# 	for i in x:
	# 		print i
	# 		
	
if __name__ == '__main__':
	main()

