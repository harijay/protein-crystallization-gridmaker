#!/usr/bin/env python
# encoding: utf-8
"""
plateliberror.py

Created by Hariharan Jayaram on 2009-01-25.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""


class PlatelibException(Exception):
	# An error class 
	def __init__(self,message):
		self.message = message
	def __str__(self):
		return repr(self.message)
		
def main():
	try:
		p =PlatelibException("Wrong input")
		raise p
	except PlatelibException, message:
		print "Error caught in test case:%s" % message.message



if __name__ == '__main__':
	main()

