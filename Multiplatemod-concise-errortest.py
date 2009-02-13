#!/usr/bin/env python
# encoding: utf-8
"""
Multiplatemod.py

Created by Hariharan Jayaram on 2009-01-28.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""



import plate
import masterplate
import component

def main():
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
	
	pwhole = plate.Plate("A1","H12",mp)
	pwhole.push_components_mapped_to_row(mp,[b1,b2,b3,b4,b1,b2,b3,b4],[100,100,100,100,100,100,100,100],["A",1,"C","D","E","F","G","H"])
	
	
	salt = component.Component("CaAc2",1000,100000)
	
	p.push_component_uniform_to_masterplate(mp,salt,25)
	p2.push_component_uniform_to_masterplate(mp,salt,50)
	p3.push_component_uniform_to_masterplate(mp,salt,100)
	p4.push_component_uniform_to_masterplate(mp,salt,150)
	
	water = component.Component("100.00% Water",1000,300000)
	pwhole.fill_water(mp,water)
	
	mp.printwellinfo()
	mp.makefileforformulatrix("CM610CaAcoptimize-concise-errortest.txt")
	

if __name__ == '__main__':
	main()

