# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

def Bisection(fun, a, b, tol, max_iters):
    
    if fun(a)*fun(b) > 0:
        print('a and b must be different')
        
    counter = 0
    
    c = (a + b)/2
    root = c;
    
    while counter < max_iters and abs(fun(c)) > tol:
      
        if fun(a)*fun(c) < 0:
            b = c
            
        else: 
            a = c
            
        
        c = (a+b)/2
        counter += 1
    
    root = c;
    
    plt.scatter(a, fun(a))
    plt.scatter(b, fun(b))
    plt.scatter(c, fun(c))
    plt.title('Bisection Method')
    plt.xlabel('a,b,c')
    plt.ylabel('F(a), F(b), F(c)')
    plt.show()
    plt.clf()
    
    return root



Cr = .03 
Cd = 1.21 
rho = 4.427e-5 #lb/in^3
A = 75 #in^2
Ft = 75 #lb
g = 386.09 #in/s^2
m =5.5 #lb

fun = lambda Vtr: Ft - ((1/2) * rho * A * Cd * (Vtr**2)) - Cr*m*g;


vtr = Bisection(fun, -1, 1000, 1e-3, 1000);


#create table of different root values given different params
#find optimal params by finding max vtr

x = PrettyTable(["Tank Pressure [P0]","Train Mass [m]","Piston Radius [rp]","Pinion Gear Radius [rg]","Veclocity of train [vtr]"])



x.add_row(["50 [psig]","1 [lbs]","1 [cm]","10 [cm]","177.67 [in/sec]"])
x.add_row(["50 [psig]","2 [lbs]","1 [cm]","10 [cm]","160.64 [in/sec]"])
x.add_row(["50 [psig]","4 [lbs]","1 [cm]","10 [cm]","119.47 [in/sec]"])
x.add_row(["50 [psig]","5.5 [lbs]","1 [cm]","10 [cm]","74.99 [in/sec]"])
x.add_row(["50 [psig]","6 [lbs]","1 [cm]","10 [cm]","52.34 [in/sec]"])

print(x)

print(vtr)