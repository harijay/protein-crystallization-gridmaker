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
import buffercomponent

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
	
	p.gradient_along_x(peg400,18,25)
	p2.gradient_along_x(peg400,18,25)
	p3.gradient_along_x(peg400,18,25)
	p4.gradient_along_x(peg400,18,25)
	
	# Define the buffer components  that will be mixed to get the pH gradients along the alphabet axes 
	# Buffer components that are used for mixing can be defined as follows after importing the buffercomponent.SimpleBuffer
	# buffer = buffercomponent.SimpleBuffer(name,stockconc,totalvol,ph,pka)
	
	b1 = buffercomponent.SimpleBuffer("ph7p5",1,100000,7.5,8.03)
	b2 = buffercomponent.SimpleBuffer("ph8.5",1,100000,8.5,8.03)
	
	# Now we will setup the same gradient as we did before as specified gradient 7.6 , 8.0 ,8.2 , 8.4
	# The methods for buffers are
	# ph_gradient_alongx(masterplate,buffer1,buffer2,finalconc,startph,stopph)
	# ph_gradient_alongy(masterplate,buffer1,buffer2,finalconc,startph,stopph)
	# ph_list_alongx(masterplate,buffer1,buffer2,finalconc,phlist)
	# ph_list_alongy(masterplate,buffer1,buffer2,finalconc,phlist)
	# Note that Buffer stock conc is specified in molar i.e 1 so the final conc is also in molar 0.1
	p.ph_list_alongy(b1,b2,0.1,[7.6,8.0,8.2,8.4])
	p2.ph_list_alongy(b1,b2,0.1,[7.6,8.0,8.2,8.4])
	p3.ph_list_alongy(b1,b2,0.1,[7.6,8.0,8.2,8.4])
	p4.ph_list_alongy(b1,b2,0.1,[7.6,8.0,8.2,8.4])
	
	
	
	# We want each quadrant ( i.e plate p , p2 , p3 and p4 ) to have a constant concentration of Calcium Chloride
	# We use the method Plate.constant_concentration(self,masterplate,Component,finalconc):
	salt = component.Component("CaAc2",1000,100000)
	
	p.constant_concentration(salt,25)
	p2.constant_concentration(salt,50)
	p3.constant_concentration(salt,100)
	p4.constant_concentration(salt,150)
	
	# Now its time to fill the rest with water calling the fill_water method. We can do it for whole plate using pwhole defined from ( A1 to H12)
	# The water concentration is arbitratrily assigned to a value. Has no implications on dispensed volume
	# We will define pwhole for the water filling step since it has to take place for whole plate
	
	pwhole = plate.Plate("A1","H12",mp)
	water = component.Component("100.00% Water",1000,300000)
	
	pwhole.fill_water(water)
	# You can output the composition of each well to stdout using the printwellinfo() method of masterplate.Masterplate class
	mp.printwellinfo()
	
	# The makefilefor formulatrix outputs the final dispense list
	mp.makefileforformulatrix("example5.dl.txt")
	

if __name__ == '__main__':
	main()

