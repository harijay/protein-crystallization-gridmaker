#!/usr/bin/env python
# encoding: utf-8
"""
component.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""

import plateliberror

class Component(object):
	# A component is specified by its name ( eg "peg400") , a stock concentration in the same 
	# units that the final concentration is going to be specified in the well for eg 1000 ( or 1 ) 
	# and well concentration 200 ( or 0.2) denotes a component stock of 1000 mM and final conc of 
	# 200 mM or you could also use 1 in which case final conc will be 0.2 
	def __init__(self,name,stockconc,totalvol,dispensed=True):
		self.vol = totalvol
		self.name = name.strip()
		self.stockconc = stockconc
		self.dispensed = dispensed

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

