#!/usr/bin/env python
# encoding: utf-8
"""
componentlist.py

Created by Hariharan Jayaram on 2009-01-25.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""


class ComponentList(object):
	# A factory which holds all the components . I am not yet using this appropriately.
	# Need to read up on the Factory pattern or something 
	componentfactory = {}
	def __init__(self):
		ComponentList.componentfactory = {}
	def insertcomponent(self,Component):
		self.componentfactory[Component.name] = Component
	def getcomponent(self,componentname):
		return self.componentfactory[componentname]
	
	def listcontents(self):
		for i in ComponentList.componentfactory:
			print ComponentList.componentfactory[i].name,ComponentList.componentfactory[i].vol, ComponentList.componentfactory[i].stockconc

def main():
	rack = ComponentList()
	c1 = component.Component("peg400",50,100)
	rack.insertcomponent(c1)
	c2 = component.Component("CaCl2",2000,10)
	rack.insertcomponent(c2)
	rack.listcontents()


if __name__ == '__main__':
	main()

