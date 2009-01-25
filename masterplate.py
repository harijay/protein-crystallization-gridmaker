#!/usr/bin/env python
# encoding: utf-8
"""
masterplate.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import well

class Masterplate(object):
	alphas = ["A", "B", "C" , "D", "E" , "F", "G", "H"]
	nums = [1,2,3,4,5,6,7,8,9,10,11,12]
	ordered_keys = []
	welldict = {}
	
	def __init__(self):
		for a in self.alphas:
			for i in self.nums:
				key = "%s" % a + "%s" % i
				self.ordered_keys.append(key)
				self.welldict[key] = well.well(a,i)
				
	def getwell(self,alpha,num):
		key = "%s" % alpha + "%s" % num
		return self.welldict[key]
		
	def printwellinfo(self):
		for k in self.ordered_keys :
			print self.welldict[k].about()
			
def main():
	sys.path.append("/Users/hari")
	import gridder
	from gridder import masterplate
	testplate = masterplate.Masterplate()
	testplate.printwellinfo()
	pass


if __name__ == '__main__':
	main()

