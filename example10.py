#!/usr/bin/env python
# encoding: utf-8
"""
example1.py

Created by Hariharan Jayaram on 2009-01-26.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""


import plate
import masterplate
import component


def main():
	# A real world test plate made . With 4 different Calcium concentrations
	# Four different pHs and 6 different pegs
	# For CM610 optimization
	# Please also consult other examples. This example uses the most wordy syntax to make each setp very obvious. No Shortcuts here
	
	# First define the masterplate.Masterplate with volume in µl i.e 2000 for 2 ml
	mp = masterplate.Masterplate(2000)
	
	# Define each plate with the left corner well and right corner well . Feed the plate its containing master plate i.e
	
	p = plate.Plate("A1","D6",mp)
	p2 = plate.Plate("A7","D12",mp)
	p3 = plate.Plate("E1","H6",mp)
	p4 = plate.Plate("E7","H12",mp)
	
	# Define a component with concentration  units that you keep constant for this component. i.e 
	# if you use percent then you remember to use percent everytime you want to dispense this component
	
	ammso = component.Component("AMS04",3, 100000)
	sodcl = component.Component("NaCl",4,100000)
	amformate = component.Component("AMFormate",6, 100000)
	sodformate = component.Component("SodFormate",8,100000)


	
	# Now we will lay down a peg gradient along the x axis 

	
	# Now lets define each buffer component
	
	b1 = component.Component("ph4p5",1000,100000)
	b2 = component.Component("ph5p5",1000,100000)
	b3 = component.Component("ph6p5",1000,100000)
	b4 = component.Component("ph7p5",1000,100000)
	b5 = component.Component("ph8p5",1000,100000)
	b6 = component.Component("ph9p5",1000,100000)

	water = component.Component("100.00% Water",1000,300000)
	
	p.push_gradient_list_y(ammso,[1.8,2.1,2.4,2.7])
	p2.push_gradient_list_y(sodcl,[2.7,3,3.3,3.6])
	p3.push_gradient_list_y(amformate,[3,3.9,4.8,5.4])
	p4.push_gradient_list_y(sodformate,[4,5,6,7])
	
	# Here we fill each sub plate with water : in example 3 you will see a shortcut way of doing this 
	
	p.push_buffer_to_column_on_masterplate(b1,100,1)
	p.push_buffer_to_column_on_masterplate(b2,100,2)
	p.push_buffer_to_column_on_masterplate(b3,100,3)
	p.push_buffer_to_column_on_masterplate(b4,100,4)
	p.push_buffer_to_column_on_masterplate(b5,100,5)
	p.push_buffer_to_column_on_masterplate(b6,100,6)
			
	p2.push_buffer_to_column_on_masterplate(b1,100,7)
	p2.push_buffer_to_column_on_masterplate(b2,100,8)
	p2.push_buffer_to_column_on_masterplate(b3,100,9)
	p2.push_buffer_to_column_on_masterplate(b4,100,10)
	p2.push_buffer_to_column_on_masterplate(b5,100,11)
	p2.push_buffer_to_column_on_masterplate(b6,100,12)
	
	p3.push_buffer_to_column_on_masterplate(b1,100,1)
	p3.push_buffer_to_column_on_masterplate(b2,100,2)
	p3.push_buffer_to_column_on_masterplate(b3,100,3)
	p3.push_buffer_to_column_on_masterplate(b4,100,4)
	p3.push_buffer_to_column_on_masterplate(b5,100,5)
	p3.push_buffer_to_column_on_masterplate(b6,100,6)
	
	p4.push_buffer_to_column_on_masterplate(b1,100,7)
	p4.push_buffer_to_column_on_masterplate(b2,100,8)
	p4.push_buffer_to_column_on_masterplate(b3,100,9)
	p4.push_buffer_to_column_on_masterplate(b4,100,10)
	p4.push_buffer_to_column_on_masterplate(b5,100,11)
	p4.push_buffer_to_column_on_masterplate(b6,100,12)

						
	p.fill_water(water)
	p2.fill_water(water)
	p3.fill_water(water)
	p4.fill_water(water)
	
	# You can output the composition of each well to standard out with the masterplate.Masterplate.printwellinfo() method
	mp.printwellinfo()
	
	# And now to write the dispense list for the formulatrix robot
	
	mp.makefileforformulatrix("example10.dl.txt")

if __name__ == '__main__':
	
	main()

