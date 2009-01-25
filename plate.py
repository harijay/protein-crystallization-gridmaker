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
	def __init__(self,gridstart,gridend):
		self.gridstart = gridstart
		self.gridend = gridend
		self.gridminnum = int(self.gridstart[1:])
		self.gridmaxnum = int(self.gridend[1:])
		self.gridminalpha = self.gridstart[0]
		self.gridmaxalpha = self.gridend[0]
		self.calcnumwells()
		
	def calcnumwells(self):
		numalongalpha = ord(self.gridmaxalpha)-ord(self.gridminalpha)+1
		numalongnum = self.gridmaxnum - self.gridminnum + 1
		return numalongalpha * numalongnum
	def calcgradientnums(self,start):

def main():
	p = plate("A1","D3")
	print "number of wells in plate" , p.calcnumwells()


if __name__ == '__main__':
	main()

