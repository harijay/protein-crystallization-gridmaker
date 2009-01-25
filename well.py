#!/usr/bin/env python
# encoding: utf-8
"""
well.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os

class well(object):
	components = []
	def __init__(self,alpha,num):
		self.alpha = alpha
		self.num = num
	def about(self):
		about = "WELL: %s%s" % (self.alpha , self.num)
		return about
def main():
	pass


if __name__ == '__main__':
	main()

