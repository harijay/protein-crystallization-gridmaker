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
	
	peg400 = component.Component("peg400",50,100000)
	
	# Now we will lay down a peg gradient along the x axis 
	p.gradient_along_x(peg400,18,25)
	p2.gradient_along_x(peg400,18,25)
	p3.gradient_along_x(peg400,18,25)
	p4.gradient_along_x(peg400,18,25)
	
	
	# Now lets define each buffer component
	
	b1 = component.Component("ph7p6",1000,100000)
	b2 = component.Component("ph8p0",1000,100000)
	b3 = component.Component("ph8p2",1000,100000)
	b4 = component.Component("ph8p4",1000,100000)

	# Now we use the rather wordy push_buffer_to_row_on_masterplate method to populate with buffer for each row
	# In example3 you will see the shortcut methods for the same procedure. Also the push_component_to_column_on_masterplate(self,masterplate,Component,finalconc,columnnum) from the 
	# plate.Plate class will do the same except for the column instead of row 
	
	p.push_buffer_to_row_on_masterplate(b1,100,"A")
	p.push_buffer_to_row_on_masterplate(b2,100,"B")
	p.push_buffer_to_row_on_masterplate(b3,100,"C")
	p.push_buffer_to_row_on_masterplate(b4,100,"D")
	
	p2.push_buffer_to_row_on_masterplate(b1,100,"A")
	p2.push_buffer_to_row_on_masterplate(b2,100,"B")
	p2.push_buffer_to_row_on_masterplate(b3,100,"C")
	p2.push_buffer_to_row_on_masterplate(b4,100,"D")
	
	p3.push_buffer_to_row_on_masterplate(b1,100,"E")
	p3.push_buffer_to_row_on_masterplate(b2,100,"F")
	p3.push_buffer_to_row_on_masterplate(b3,100,"G")
	p3.push_buffer_to_row_on_masterplate(b4,100,"H")
	
	p4.push_buffer_to_row_on_masterplate(b1,100,"E")
	p4.push_buffer_to_row_on_masterplate(b2,100,"F")
	p4.push_buffer_to_row_on_masterplate(b3,100,"G")
	p4.push_buffer_to_row_on_masterplate(b4,100,"H")
	
	salt = component.Component("CaAc2",1000,100000)
	
	# Finally we add a constant salt additive to the entire sub plate. Plate 1 has 25 mM , plate 2 , 50 mM , plate 3 , 100 mM , and plate 4 ,150 mM
	# This method is also called plate.Plate.constant_salt(self,masterplate,Component,finalconc):
	# so you could very well say p.constant_salt(salt,25)
	
	p.push_component_uniform_to_masterplate(salt,25)
	p2.push_component_uniform_to_masterplate(salt,50)
	p3.push_component_uniform_to_masterplate(salt,100)
	p4.push_component_uniform_to_masterplate(salt,150)
	
	# Finally we define the water component : Here the concentration is arbitrary! The platelib just fills water to the final volume of the well ( 2000 µl)
	
	water = component.Component("100.00% Water",1000,300000)
	
	# Here we fill each sub plate with water : in example 3 you will see a shortcut way of doing this 
	
	p.fill_water(water)
	p2.fill_water(water)
	p3.fill_water(water)
	p4.fill_water(water)
	# You can output the composition of each well to standard out with the masterplate.Masterplate.printwellinfo() method
#	mp.printwellinfo()
	
	# And now to write the dispense list for the formulatrix robot
	
	mp.makefileforformulatrix("example1.dl.txt")
	mp.printpdf("example1")
if __name__ == '__main__':
	
	main()

