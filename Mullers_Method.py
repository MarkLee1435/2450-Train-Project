# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 11:22:18 2022

@author: mjlee
"""
import math as m
def Mullers_Method(fun,x0,x1,x2,tol = .000001,maxiter = 100000):
    i = 0
    while i< maxiter:
        i += 1
        h0 = x1-x0
        h1 = x2-x1
        g0 = (fun(x1)-fun(x0))/h0
        g1 = (fun(x2)-fun(x1))/h1
        a = (g1-g0)/(h1+h0)
        b = a * h1 + g1
        c = fun(x2)
        D = m.sqrt(b**2-4*a*c)
        if b < 0 :
            D = -D
        ci = x2 +(-2*c)/(b+D)
        if i>1:
            err = (ci-x2)/ci
            if abs(err) < tol:
                return ci
        x0 = x1
        x1 = x2
        x2 = ci