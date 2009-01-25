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
class plate(object):
	gridstart = None
	gridend = None
	numwells = None
	numalongalpha = None
	numalongnum = None
	
	def __init__(self,gridstart,gridend):
		self.gridstart = gridstart
		self.gridend = gridend
		self.gridminnum = int(self.gridstart[1:])
		self.gridmaxnum = int(self.gridend[1:])
		self.gridminalpha = self.gridstart[0]
		self.gridmaxalpha = self.gridend[0]
		self.calcnumwells()
		
	def calcnumwells(self):
		self.numalongalpha = ord(self.gridmaxalpha)-ord(self.gridminalpha)+1
		self.numalongnum = self.gridmaxnum - self.gridminnum + 1
		return self.numalongalpha * self.numalongnum
		
	def calcgradientalongnum(self,start,end):
		xgradientlist = []
		xgradientlist.append(start)
		wellstofill = self.numalongnum 
		step = float(end-start)/wellstofill
		i = start
		while len(xgradientlist) < (self.numalongnum-1):
			i = i + step
			xgradientlist.append(i)
			xgradientlist.append(end)
		print xgradientlist
		
	def setgradientalongnum(self,list):
		if len(list) < self.numalongnum:
			raise plateliberror.PlatelibException("Too few inputs in gradient along x list")
		else:
			self.xgradientlist = list
		print self.xgradientlist

def main():
	p = plate("A1","D6")
	print "number of wells in plate" , p.calcnumwells()
	p.calcgradientalongnum(20,26)
	
	pasdfaf = plate("A1","D6")
	pasdfaf.calcgradientalongnum(20,26)

	psdfvd = plate("A1","D6")
	psdfvd.calcgradientalongnum(20,26)
	psdfvd.setgradientalongnum([20,22,24,26,28,30])

if __name__ == '__main__':
	main()

