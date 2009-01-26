#!/usr/bin/env python
# encoding: utf-8
"""
MakeRealPlate.py

Created by Hariharan Jayaram on 2009-01-26.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import plate,masterplate,component


def main():
	mp = masterplate.Masterplate(2000)
	p = plate.Plate("A1","H12",mp)
	peg400 = component.Component("peg400",50,100000)
	
	b1 = component.Component("ph7p0",1000,100000)
	b2 = component.Component("ph7p2",1000,100000)
	b3 = component.Component("ph7p4",1000,100000)
	b4 = component.Component("ph7p6",1000,100000)
	b5 = component.Component("ph7p8",1000,100000)
	b6 = component.Component("ph8p0",1000,100000)
	b7 = component.Component("ph8p2",1000,100000)
	b8 = component.Component("ph8p4",1000,100000)
	
	p.push_buffer_to_row_on_masterplate(mp,b1,100,"A")
	p.push_buffer_to_row_on_masterplate(mp,b2,100,"B")
	p.push_buffer_to_row_on_masterplate(mp,b3,100,"C")
	p.push_buffer_to_row_on_masterplate(mp,b4,100,"D")
	p.push_buffer_to_row_on_masterplate(mp,b5,100,"E")
	p.push_buffer_to_row_on_masterplate(mp,b6,100,"F")
	p.push_buffer_to_row_on_masterplate(mp,b7,100,"G")
	p.push_buffer_to_row_on_masterplate(mp,b8,100,"H")
	
	p.push_gradient_start_stop_x(mp,peg400,20,32)
	water = component.Component("water",1000,300000)
	p.fill_water(mp,water)
	
	mp.printwellinfo()
	mp.makefileforformulatrix()

if __name__ == '__main__':
	
	main()

