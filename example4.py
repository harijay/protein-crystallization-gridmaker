#!/usr/bin/env python
# encoding: utf-8
"""
example3.py

Created by Hariharan Jayaram on 2009-01-28.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""


import plate
import masterplate
import component

def main():
	# Create the plate with volume of 2 mls or 2000 microlitre : volume should be in microlitres ( eg 2000 µl)
	mp = masterplate.Masterplate(2000)

	# Split plate into 4 subplates. For each subplate plate you need the first ( left corner) and last ( right corner)
	p = plate.Plate("A1","D6",mp)
	p2 = plate.Plate("A7","D12",mp)
	p3 = plate.Plate("E1","H6",mp)
	p4 = plate.Plate("E7","H12",mp)
	# Define the first component 
	# Define a component with concentration  units that you keep constant for this component. i.e 
	# if you use percent then you remember to use percent everytime you want to dispense this component
	peg400 = component.Component("peg400",50,100000)
	
	# Now define the gradients along x ( i.e the numeral axes )
	
	p.gradient_along_x(mp,peg400,18,25)
	p2.gradient_along_x(mp,peg400,18,25)
	p3.gradient_along_x(mp,peg400,18,25)
	p4.gradient_along_x(mp,peg400,18,25)
	
	# Define the four buffers that will be added along the alphabet axes 
	b1 = component.Component("ph7p6",1000,100000)
	b2 = component.Component("ph8p0",1000,100000)
	b3 = component.Component("ph8p2",1000,100000)
	b4 = component.Component("ph8p4",1000,100000)
	
	# Now these buffers will be the same for an entire row across the plates we could do this as done below or as given in example 1
	# define a plate that corresponds to the whole 96 wells
	pwhole = plate.Plate("A1","H12",mp)
	
	# Use this to add the components using the plate methods push_components_mapped_to_row, Note that the pattern is specified according to the order 
	pwhole.push_components_mapped_to_row(mp,[b1,b2,b3,b4,b1,b2,b3,b4],[100,100,100,100,100,100,100,100],["A","B","C","D","E","F","G","H"])
	
	
	# We want each quadrant ( i.e plate p , p2 , p3 and p4 ) to have a constant concentration of Calcium Chloride
	# We use the method Plate.constant_concentration(self,masterplate,Component,finalconc):
	salt = component.Component("CaAc2",1000,100000)
	
	p.constant_concentration(mp,salt,25)
	p2.constant_concentration(mp,salt,50)
	p3.constant_concentration(mp,salt,100)
	p4.constant_concentration(mp,salt,150)
	
	# Now its time to fill the rest with water calling the fill_water method. We can do it for whole plate using pwhole defined from ( A1 to H12)
	# The water concentration is arbitratrily assigned to a value. Has no implications on dispensed volume
	water = component.Component("100.00% Water",1000,300000)
	pwhole.fill_water(mp,water)
	# You can output the composition of each well to stdout using the printwellinfo() method of masterplate.Masterplate class
	mp.printwellinfo()
	
	# The makefilefor formulatrix outputs the final dispense list
	mp.makefileforformulatrix("example4.dl.txt")
	

if __name__ == '__main__':
	main()

