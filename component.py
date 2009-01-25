#!/usr/bin/env python
# encoding: utf-8
"""
component.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import plateliberror

class Component(object):
	
	def __init__(self,name,stockconc,totalvol):
		self.vol = totalvol
		self.name = name
		self.stockconc = stockconc
		
	def deplete(self,volused):
		self.vol = self.vol - volused
		if self.vol <= 0:
			raise plateliberror.PlatelibException("Used up component %s" % self.name)
	def getmls(self):
		return self.vol/1000.0		
def main():
	pass


if __name__ == '__main__':
	main()

