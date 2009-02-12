#!/usr/bin/env python
# encoding: utf-8
"""
example1.py

Created by Hariharan Jayaram on 2009-01-26.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""

import sys
import os
import plate,masterplate,component


def main():
	# A real world test plate made . With 4 different Calcium concentrations
	# Four different pHs and 6 different pegs
	# For CM610 optimization
	# Please also consult other examples. This example uses the most wordy syntax to make each setp very obvious. No Shortcuts here
	
	# First define the masterplate.Masterplate with volume in µl i.e 2000 for 2 ml
	mp = masterplate.Masterplate(2000)
	
	# Define each plate with the left corner well and right corner well . Feed the plate its containing master plate i.e
	
	p1 = plate.Plate("A1","D6",mp)
	p2 = plate.Plate("A7","D12",mp)
	p3 = plate.Plate("E1","H6",mp)
	p4 = plate.Plate("E7","H12",mp)
	
	# Define a component with concentration  units that you keep constant for this component. i.e 
	# if you use percent then you remember to use percent everytime you want to dispense this component
	
	peg400 = component.Component("peg400",60,130000)
	cacl = component.Component("CaCl",2, 100000)



	
	# Now we will lay down a peg gradient along the x axis 

	
	# Now lets define each buffer component
	
	b1 = component.Component("ph8p5Tris",1000,100000)
	b2 = component.Component("ph9.0Glycine",1000,100000)
	b3 = component.Component("ph9.2glycine",1000,100000)
	b4 = component.Component("ph9.5clycine",1000,100000)


	water = component.Component("100.00% Water",1000,300000)
	
	p1.push_gradient_list_x(mp,peg400,[28,30,32,34,36,38])
	p2.push_gradient_list_x(mp,peg400,[28,30,32,34,36,38])
	p3.push_gradient_list_x(mp,peg400,[28,30,32,34,36,38])
	p4.push_gradient_list_x(mp,peg400,[28,30,32,34,36,38])
	
	p1.constant_salt(mp,cacl,0.05)
	p2.constant_salt(mp,cacl,0.1)
	p3.constant_salt(mp,cacl,0.15)
	p4.constant_salt(mp,cacl,0.2)
	
	# Here we fill each sub plate with water : in example 3 you will see a shortcut way of doing this 
	
	p1.push_buffer_to_row_on_masterplate(mp,b1,100,"A")
	p1.push_buffer_to_row_on_masterplate(mp,b2,100,"B")
	p1.push_buffer_to_row_on_masterplate(mp,b3,100,"C")
	p1.push_buffer_to_row_on_masterplate(mp,b4,100,"D")
			

	p2.push_buffer_to_row_on_masterplate(mp,b1,100,"A")
	p2.push_buffer_to_row_on_masterplate(mp,b2,100,"B")
	p2.push_buffer_to_row_on_masterplate(mp,b3,100,"C")
	p2.push_buffer_to_row_on_masterplate(mp,b4,100,"D")
	
	p3.push_buffer_to_row_on_masterplate(mp,b1,100,"E")
	p3.push_buffer_to_row_on_masterplate(mp,b2,100,"F")
	p3.push_buffer_to_row_on_masterplate(mp,b3,100,"G")
	p3.push_buffer_to_row_on_masterplate(mp,b4,100,"H")
	
	p4.push_buffer_to_row_on_masterplate(mp,b1,100,"E")
	p4.push_buffer_to_row_on_masterplate(mp,b2,100,"F")
	p4.push_buffer_to_row_on_masterplate(mp,b3,100,"G")
	p4.push_buffer_to_row_on_masterplate(mp,b4,100,"H")
						
	p1.fill_water(mp,water)
	p2.fill_water(mp,water)
	p3.fill_water(mp,water)
	p4.fill_water(mp,water)
	
	# You can output the composition of each well to standard out with the masterplate.Masterplate.printwellinfo() method
	mp.printwellinfo()
	
	# And now to write the dispense list for the formulatrix robot
	
	mp.makefileforformulatrix("example12.dl.txt")

if __name__ == '__main__':
	
	main()

