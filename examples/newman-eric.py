#!/usr/bin/env python
# encoding: utf-8
"""
example2.py

Created by Hariharan Jayaram on 2009-01-28.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

from gridder import component, plate, masterplate

def main():
# Create the plate in this case each well will have 2000 ml 
	mp = masterplate.Masterplate(2000)
	p = plate.Plate("A1","H12",mp)

# Define a component with concentration  units that you keep constant for this component. i.e 
# if you use percent then you remember to use percent everytime you want to dispense this component
	nabr = component.Component("NaBr1M",1000,100000)
	peg300 = component.Component("peg300",60,300000)
	acid = component.Component("newmanpH4",1.0,100000)
	base = component.Component("newmanph10",1.0,100000)
	
# Gradient along X dispensed a gradient of component along x ( i.e along number axis  on 96 well plate)
	p.gradient_along_y(peg300,35,43)
	p.constant_salt(nabr,100)
	
# Now we will use a Tribuffer as described by Newman J et al 
# Say we want to do a pH from 4 to 10 along the x axis we do
	p.maketo100_alongx(acid,base,0.1,100,0)
	
	Water = component.Component("100.00% Water",100,100000)
	p.fill_water(Water)
	
# The makefileforformulatrix method of masterplate.Masterplate Class writes the dispense list
	mp.makefileforformulatrix("ericNabr100_newman.dl.txt")
	
if __name__ == '__main__':
	main()

