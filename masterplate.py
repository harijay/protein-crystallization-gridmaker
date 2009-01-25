#!/usr/bin/env python
# encoding: utf-8
"""
masterplate.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
sys.path.append("/Users/hari/gridder")
from gridder import well
class masterplate(object):
	alphas = ["A", "B", "C" , "D", "E" , "F", "G", "H"]
	nums = [1,2,3,4,5,6,7,8,9,10,11,12]
	welldict = {}
	
	def __init__(self):
		for i in range(12):
			for a in alphas:
				key = "%s" % a + "%s" % self.nums[i]
				welldict[key] = well(alpha=a, num = i)
				
	def getwell(self,alpha,num):
		key = "%s" % alpha + "%s" % num
		return self.welldict[key]
		
def main():
	pass


if __name__ == '__main__':
	main()

