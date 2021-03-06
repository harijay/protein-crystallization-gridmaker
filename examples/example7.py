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
	c = component.Component("CaAc2",2000,100000)
	
# Gradient along X dispensed a gradient of component along x ( i.e along number axis  on 96 well plate)
	p.gradient_along_x(c,0,200)
	
	peg400 = component.Component("peg400",50,100000)
# Gradient along Y dispensed a gradient of component along y ( i.e along alphabet axis)
	p.gradient_along_y(peg400,22,30)
	
# Now we will use a Tribuffer as described by Newman J et al 
	t1 = component.Component("tribfferpH4",1.0,100000)
	t2 = component.Component("tribufferpH10",1.0,100000)

# Say we want to do a pH from 4.5 to 7 along the x axis we look at the table and figure 10 to  55 percent of component 2 should cover it 
# We need to report for component1 so that goes from 10 to 45
	p.maketo100_alongx(t1,t2,0.1,90,45)
	
	Water = component.Component("100.00% Water",100,100000)
	p.fill_water(Water)
# The makefileforformulatrix method of masterplate.Masterplate Class writes the dispense list
	mp.makefileforformulatrix("example7_newman.dl.txt")
	
if __name__ == '__main__':
	main()

