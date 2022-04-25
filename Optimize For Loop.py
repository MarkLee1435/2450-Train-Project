# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 07:14:17 2022

@author: Owner
"""

from moving_train import t_at_finish
import numpy as np



'''State Physical Params'''
r_w = 0.02 #meters
t_opt = 1e6 #seconds

'''Make var_p array & var_p_opt'''
var_p = np.zeros([6,1])
var_p_opt = np.zeros([6,1])

'''Make parameters for the array'''
L_t = np.arange(0.2,0.30, 0.01) #meters
r_0 = np.arange(0.05, 0.2, 0.005) #meters
P0_gauge = np.arange(70000,200000,10000) #Pascals
r_g = np.arange(0.002,0.01,0.001) #meters
L_r = np.arange(0.1,0.5,0.1) #meters
r_p = np.arange(0.02,0.04,0.01) #meters

rho_t = [1400,1200,7700,8000,4500,8940,2700] #kg/m^3

'''Set Constraints'''
max_height = 0.23 #meters
max_width = 0.2 #meters
max_length = 1.5 #meters
max_gear = r_g/r_w 


'''For Loop to Brute Force optimize'''
    
for i in range(np.size(rho_t)):
    for j in range(np.size(L_t)):
        for k in range(np.size(r_0)):
            for l in range(np.size(P0_gauge)):
                for m in range(np.size(r_g)):
                    for n in range(np.size(L_r)):
                        for o in range(np.size(r_p)):
                            
                            #Material Density
                            rho_mat = rho_t[i]
                            
                            #Variable Params
                            var_p[0] = L_t[j]
                            var_p[1] = r_0[k]
                            var_p[2] = P0_gauge[l]
                            var_p[3] = r_g[m]
                            var_p[4] = L_r[n]
                            var_p[5] = r_p[o]
                            
                            #Find tie to finish with parameters
                            try:
                                t_finish = t_at_finish(var_p, rho_mat, return_only_time=True)
                            except:
                                import pdb;pdb.set_trace()
                            #Filter results that violate constraints
                            if (2*r_w + 2*r_0[k] < max_height) and (2*r_0[k] < max_width) and (L_r[n]+L_t[j] < max_length) and (r_g[m]/r_w < 1) and t_finish < t_opt:
                                
                                #Finish optimal
                                t_opt = t_finish   
                                print(t_opt)
                                #Optimal parameters
                                var_p_opt[0] = L_t[j]
                                var_p_opt[1] = r_0[k]
                                var_p_opt[2] = P0_gauge[l]
                                var_p_opt[3] = r_g[m]
                                var_p_opt[4] = L_r[n]
                                var_p_opt[5] = r_p[o]
                                
                                rho_mat_opt = rho_mat
print('a')
'''
xo = var_p_opt 
print("xo = ", xo)
res = optimize.minimize(objfun, xo, method='SLSQP', bounds=(db, tb))
print("Results of constrained optimization:")
print("Optimal d, t = %g, %g" % tuple(res.x))
print("Cost of optimized column = ", cost(res.x, P, E, L, rho, ni, nn))
res = optimize.minimize(objfun, xo, method='Nelder-Mead')
print("Results of unconstrained optimization:")
print("Optimal d, t = %g, %g" % tuple(res.x))
print("Cost of optimized column = ", cost(res.x, P, E, L, rho, ni, nn))

'''
print(var_p_opt)
print(t_opt)                                
                                
                                





                                
                                
                                




