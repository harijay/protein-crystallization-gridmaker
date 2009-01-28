#!/usr/bin/env python
# encoding: utf-8
"""
MakeRealPlate.py

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
	mp = masterplate.Masterplate(2000)
	p = plate.Plate("A1","D6",mp)
	p2 = plate.Plate("A7","D12",mp)
	p3 = plate.Plate("E1","H6",mp)
	p4 = plate.Plate("E7","H12",mp)
	

	peg400 = component.Component("peg400",50,100000)
	
	p.push_gradient_start_stop_x(mp,peg400,18,25)
	p2.push_gradient_start_stop_x(mp,peg400,18,25)
	p3.push_gradient_start_stop_x(mp,peg400,18,25)
	p4.push_gradient_start_stop_x(mp,peg400,18,25)
	
	
	b1 = component.Component("ph7p6",1000,100000)
	b2 = component.Component("ph8p0",1000,100000)
	b3 = component.Component("ph8p2",1000,100000)
	b4 = component.Component("ph8p4",1000,100000)

	
	p.push_buffer_to_row_on_masterplate(mp,b1,100,"A")
	p.push_buffer_to_row_on_masterplate(mp,b2,100,"B")
	p.push_buffer_to_row_on_masterplate(mp,b3,100,"C")
	p.push_buffer_to_row_on_masterplate(mp,b4,100,"D")
	
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
	
	salt = component.Component("CaAc2",1000,100000)
	
	p.push_component_uniform_to_masterplate(mp,salt,25)
	p2.push_component_uniform_to_masterplate(mp,salt,50)
	p3.push_component_uniform_to_masterplate(mp,salt,100)
	p4.push_component_uniform_to_masterplate(mp,salt,150)
	
	water = component.Component("100.00% Water",1000,300000)
	p.fill_water(mp,water)
	p2.fill_water(mp,water)
	p3.fill_water(mp,water)
	p4.fill_water(mp,water)
	
	mp.printwellinfo()
	mp.makefileforformulatrix("CM610CaAcoptimize.txt")

if __name__ == '__main__':
	
	main()

