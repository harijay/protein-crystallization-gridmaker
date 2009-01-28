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
	c = component.Component("CaAc2",2000,100000)
	
# Gradient along X dispensed a gradient of component along x ( i.e along number axis  on 96 well plate)
	p.gradient_along_x(mp,c,0,200)
	
	peg400 = component.Component("peg400",50,100000)
# Gradient along Y dispensed a gradient of component along y ( i.e along alphabet axis)
	p.gradient_along_y(mp,peg400,22,30)
	

	buff = component.Component("ph8.0", 1000,100000)
# Constant for the well uses constant_concentration
	p.constant_concentration(mp,buff,100)
	
	Water = component.Component("100.00% Water",100,100000)
	p.fill_water(mp,Water)
# The makefileforformulatrix method of masterplate.Masterplate Class writes the dispense list
	mp.makefileforformulatrix("example2.dl.txt")
	
if __name__ == '__main__':
	main()

