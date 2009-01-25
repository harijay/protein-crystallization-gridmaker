#!/usr/bin/env python
# encoding: utf-8
"""
plate.py

Created by Hariharan Jayaram on 2009-01-25.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
class plate(object):
	gridstart = None
	gridend = None
	numwells = None
	numalongalpha = None
	numalongnum = None
	xgradientlist = []
	
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
		
	def calcgradientnalongnum(self,start,end):
		self.xgradientlist.append(start)
		wellstofill = self.numalongnum 
		step = float(end-start)/wellstofill
		i = start
		while len(self.xgradientlist) < (self.numalongnum-1):
			i = i + step
			self.xgradientlist.append(i)
		self.xgradientlist.append(end)
		print self.xgradientlist
	def setgradientalongnum(self,list):
		if len(list) < self.numalongnum:
			raise 

def main():
	p = plate("A1","D6")
	print "number of wells in plate" , p.calcnumwells()
	p.calcgradientnalongnum(22,30)

if __name__ == '__main__':
	main()

