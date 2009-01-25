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
class Plate(object):
	gridstart = None
	gridend = None
	numwells = None
	numalongalpha = None
	numalongnum = None
	xgradientlist = None
	
	def __init__(self,gridstart,gridend):
		self.gridstart = gridstart
		self.gridend = gridend
		self.gridminnum = int(self.gridstart[1:])
		self.gridmaxnum = int(self.gridend[1:])
		self.gridminalpha = self.gridstart[0]
		self.gridmaxalpha = self.gridend[0]
		self.calcnumwells()
		self.xgradientlist = []
		self.ygradientlist = []
		
	def calcnumwells(self):
		self.numalongalpha = ord(self.gridmaxalpha)-ord(self.gridminalpha)+1
		self.numalongnum = self.gridmaxnum - self.gridminnum + 1
		return self.numalongalpha * self.numalongnum
		
	def calcgradientalongnum(self,start,end):
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
		# Specify the pergentages of peg required for the wells 
		if len(list) < self.numalongnum:
			raise plateliberror.PlatelibException("Too few inputs in gradient along x list")
		else:
			self.xgradientlist = list
		return self.xgradientlist
	
	def calcgradientalongalpha(self,start,end):
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
		# Specify the pergentages of peg required for the wells 
		if len(list) < self.numalongnum:
			raise plateliberror.PlatelibException("Too few inputs in gradient along x list")
		else:
			self.ygradientlist = list
		return self.ygradientlist
		
	def pushtomasterplate(self):
		# Sets the well components in masterplate.platedict()
		pass
def main():
	p = Plate("A1","D6")
	print "number of wells in plate" , p.calcnumwells()
	x=p.calcgradientalongnum(20,26)
	print x
	pasdfaf = Plate("A1","D6")
	x=pasdfaf.calcgradientalongnum(20,26)
	print x
	psdfvd = Plate("A1","D3")
	x=psdfvd.calcgradientalongnum(20,50)
	print x
	x = psdfvd.specifygradientalongnum([20,22,24,26,28,30])
	print x
	p = Plate("A1","D6")
	x=p.calcgradientalongalpha(22,30)
	for item in x:
		print item
if __name__ == '__main__':
	main()

