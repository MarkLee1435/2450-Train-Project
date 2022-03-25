# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 11:22:20 2022

@author: mjlee
"""

def Newton_Raphson(fun,fund,c0,tol = .000001,maxiter = 100000):
    i = 0
    while i<maxiter:
        i += 1
        root = c0-(fun)/(fund)
        c0 = root
        if i>1:
            err = (root-c0)/root
            if abs(err) < tol:
                    
                return root