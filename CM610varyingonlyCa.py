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
	p = plate.Plate("A1","H12",mp)
	
	c = component.Component("CaAc2",2000,100000)
	p.gradient_along_x(mp,c,0,200)
	
	peg400 = component.Component("peg400",50,100000)
	p.gradient_along_y(mp,peg400,22,30)
	
	buff = component.Component("ph8.0", 1000,100000)
	p.constant_concentration(mp,buff,100)
	
	Water = component.Component("100.00% Water",100,100000)
	p.fill_water(mp,Water)
	
	mp.makefileforformulatrix("CM610GradienCaAc2AndPeg400ph8p0.dl.txt")
	
if __name__ == '__main__':
	main()

