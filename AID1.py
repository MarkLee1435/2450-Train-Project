# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 16:44:31 2022

@author: mjlee
"""
import numpy as np
import sympy as sym
import math as m

def air_tank(p1,p0,v):
    x = p1*v*(np.log(p1/p0)+(p0/p1)-1)
    
    return x

def volume(r,h):
    v = m.pi*(r**2)*h
    return v

def integral(v,p0,p1):
    x1 = v*(np.log(p1/p0))
    return x1
    
h = 21.65 #in
r = 4.5 #in
p1 = 62 # psi
pressure_initial = 12.7798 #psi

v = volume(r,h)
print(v)
a= air_tank(p1,pressure_initial,v)
print(a)
x = integral(v,pressure_initial,p1)
print(x)

while pressure_initial != 62:
    for p0 in range(25):
        x = integral(v,pressure_initial,p1)
        Ep = x*.0625
        p1 -= 2
        print(Ep,'\n')
    
    
# deal with error prop


