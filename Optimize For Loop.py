# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 13:37:22 2022

@author: Bfelts

Variable Optimization

"""
from moving_train import main
from train_motion import *

import numpy as np

#Initial Values
t_opt = 1e6

#Constants
wheel_radius = .02 #meters

#Define ranges for physical parameters 
tank_length = np.arange(0.2,0.301,.01) #meters
tank_radius = np.arange(0.05,0.201,.01) #meters
trainMat_rho = 1400 #kg/m^3 for PVC
tank_P0 = np.arange(70000,201000,1000) #Pa
gear_radius = np.arange(.002,.011,.001) #m
piston_strokeLength = np.arange(.1,.6,.1)
piston_radius = np.arange(.02,.05,.01)

#Design constraints
maxTrain_height = .23 #meters
maxTrain_width = .2 #meters
maxTrain_length = 1.5 #meters
travel_distance = 12.5 #meters

#Some Equations
piston_length = 1.5 * piston_strokeLength

#For loops to optimize conditions
for i in range(np.size(tank_length)):
    for j in range(np.size(tank_radius)):
        for k in range(np.size(tank_P0)):
            for l in range(np.size(gear_radius)):
                for m in range(np.size(piston_strokeLength)):
                    for n in range(np.size(piston_radius)):
                        
                        #Intermidate equations
                        piston_length = 1.5 * piston_strokeLength[m]
                        train_height = 2*tank_radius[j] + 2*wheel_radius
                        train_width = 2*tank_radius[j]
                        train_length = piston_length + tank_length[i]
                        
                        #Call train_motion to determine t@10 meters & our final horizontal distance
                        t,xfinal = train_motion(tank_length[i], tank_radius[j], tank_P0[k], gear_radius[l], piston_strokeLength[m], piston_radius[n])
                        
                        #Check design Constraints 
                        #Wheel slippage is being used within train_motion 
                        #If slippage is detected xfinal = 100 m and will not pass final check
                        if train_height < maxTrain_height:
                            if train_width < maxTrain_width:
                                if train_length < maxTrain_length:
                                    if (gear_radius)/(wheel_radius) < 1:
                                        if 10<=xfinal<=12.5:
                                            if t_opt > t:
                                                t_opt = t
                                                tank_L_opt = tank_length[i]
                                                tank_r_opt = tank_radius[j]
                                                tank_P0_opt = tank_P0[k]
                                                gear_r_opt = gear_radius[l]
                                                piston_stroke_opt = piston_strokeLength[m]
                                                piston_r_opt = piston_radius[n]

opt_params = [tank_L_opt, tank_r_opt, tank_P0_opt, gear_r_opt, piston_stroke_opt, piston_r_opt]
# Plot distance traveled and train velocity versus time
                                                                                             
a = main(opt_params) 
print(a)                                        
                                              
                                                
                                        
                        
                        




         

