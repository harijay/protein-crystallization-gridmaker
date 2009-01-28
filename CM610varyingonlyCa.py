#!/usr/bin/env python
# encoding: utf-8
"""
Multiplate-mapped-columntest.py

Created by Hariharan Jayaram on 2009-01-28.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import masterplate,plate,component

def main():
	mp = masterplate.Masterplate(2000)
	p = plate.Plate("A1""H12",mp)
	c = component.Component("CaAc2",2000,100000)
	p.gradient_along_x(mp,c,0,200)
	
	peg400 = component.Component("peg400",50,100000)
	p.constant_concentration(mp,peg400,32):
	
	b = component.Component("ph8.0", 1000,100000)
	p.constant_concentration(mp,b,100)
	
	mp.writefileforforumulatrix("CM610GradientonlyCaAc2")
if __name__ == '__main__':
	main()

