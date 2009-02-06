#!/usr/bin/env python
# encoding: utf-8
"""
example2.py

Created by Hariharan Jayaram on 2009-01-28.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import masterplate,plate,component

def main():
# Create the plate in this case each well will have 2000 ml 
	mp = masterplate.Masterplate(2000)
	p = plate.Plate("A1","H12",mp)

# Define a component with concentration  units that you keep constant for this component. i.e 
# if you use percent then you remember to use percent everytime you want to dispense this component
	c = component.Component("CaBr",2000,100000)
	buffer = component.Component("TrispH8.2",1000,100000)
	peg400 = component.Component("peg400",50,150000)
	water = component.Component("100.0% Water",100,1000000)
	p.constant_salt(mp,buffer,100)
	p.gradient_along_x(mp,peg400,31,33)
	p.gradient_along_y(mp,c,100,200)
	p.fill_water(mp,water)
	mp.makefileforformulatrix("bromide_cyf143r_constantph.dl.txt")
	
if __name__ == '__main__':
	main()

