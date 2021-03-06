#!/usr/bin/env python
# encoding: utf-8
"""
component.py

Created by Hariharan Jayaram on 2009-01-24.
Copyright (c) 2009 __SciForward LLC__. All rights reserved.
"""

import plateliberror, component

class SimpleBuffer(component.Component):
	 
    def __init__(self, name, stockconc, totalvol, ph, pka,dispensed=True):
        self.name = name.strip()
        self.stockconc = stockconc
        self.vol = totalvol
        self.ph = ph
        self.pka = pka
        self.molratio = self.mol_ratio()
        self.get_conc_acid()
        self.get_conc_base()
        self.dispensed = dispensed
        if abs(self.ph - self.pka) > 2.5:
            buffer_error = plateliberror.PlatelibException("ARE YOU sure your Buffers are made correctly. pH > 2.5 units of pKa. Use methods maketo100_alongx OR maketo100_listx to vary volumes of one component against the other")
            raise buffer_error

		
    def mol_ratio(self):
        self.molratio = 10 ** (self.ph - self.pka)
        return self.molratio
		
    def get_conc_acid(self):
        self.conc_acid = (self.stockconc) / (1 + self.molratio)
        return self.conc_acid
		
    def get_conc_base(self):
        self.conc_base = self.molratio * self.conc_acid
        return self.conc_base
	
    def volumes_given_counter(self, bufferb, bufferfinal):
        if bufferfinal.ph < min(self.ph, bufferb.ph) or  bufferfinal.ph > max(self.ph, bufferb.ph):
            phexceeded_range_error = plateliberror.PlatelibException("pH Exceeded range- buffers should bracket ph %s" % bufferfinal.ph)
            raise phexceeded_range_error
        molratio_net = bufferfinal.molratio
        vself = None
        try:
            vself = (molratio_net * bufferb.conc_acid - bufferb.conc_base) / (self.conc_base - bufferb.conc_base - molratio_net * self.conc_acid + molratio_net * bufferb.conc_acid)
        except ZeroDivisionError:
            vself = 0
        vother = 1 - vself
        bufferfinal.conc = (vself * self.stockconc + vother * bufferb.stockconc) / (vself + vother)
        return (vself, vother)
		
def main():
    b = SimpleBuffer("trishigh", 1.0, 100000, 8.5, 8.06)
    b2 = SimpleBuffer("trislow", 0.8, 100000, 7.5, 8.06)

    bfinal = SimpleBuffer("bfinal", 1.0, 200000, 7.2, 8.06)
    print b.volumes_given_counter(b2, bfinal)
    print bfinal.conc

if __name__ == "__main__":
	main()

