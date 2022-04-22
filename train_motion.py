# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 13:37:21 2022

@author: Owner
"""

import numpy as np

def train_motion(t, y0, const_p, var_p, material_density = 1200):
    
    rho_air = const_p[0]
    P_atm = const_p[1]
    C_d = const_p[2]
    C_r = const_p[3]
    mu_s = const_p[4]
    r_w = const_p[5]
    m_w = const_p[6]

    L_t = var_p[0]
    r_0 = var_p[1]
    rho_t = material_density
    P_0gauge = var_p[2]
    r_g = var_p[3]
    L_r = var_p[4]
    r_p = var_p[5]
    
    #find area of tank
    ri = r_0/1.15  #inner radius
    
    L_p = 1.5 * L_r
    frontal_area = np.pi * r_0**2; 
    
    #print(ri,L_p, frontal_area)
    # Assign inputs to variables
    x, v = y0[0], y0[1]
    
    if abs(x) > 0 and v < 0:
        
        return np.array([np.inf, np.inf])
    
    # find total mass except wheel mass  
    
    Ap = np.pi * r_p**2
    
    piston_mass = Ap * L_p * 1250
    
    tank_mass = (((np.pi * (r_0**2) * L_t) - (np.pi * (ri**2) * L_t)) * rho_t)
    
    total_mass = tank_mass + piston_mass + (2*m_w)
    
    drag_force = 0.5 * rho_air * frontal_area * C_d * v**2
    
    rolling_friction = total_mass * 9.81 * C_r
    
    V0 =  np.pi * (r_p**2) 
    
    #print(Ap, piston_mass, tank_mass, total_mass, drag_force, rolling_friction, V0)
    
    # Determine whether accelerating or decelerating
    x_transition = L_p * r_w/r_g
    
    #find Ft    
    Ft = ((r_g * Ap) /r_w) * ((((P_0gauge + P_atm) * V0)/(V0 + (Ap * (r_g/r_w) * x_transition))) - P_atm)
    
    # Calculate derivative estimates
    dvdt_acceleration = lambda x, v: (1/ total_mass) * (Ft - drag_force - rolling_friction) 
    dvdt_deceleration = lambda v: (1/(total_mass)) * (-drag_force - rolling_friction)
 
    static_friction = mu_s * (total_mass / 2) * 9.81
    
    if x < x_transition:
        dvdt = dvdt_acceleration(x, v)
    else:
        dvdt = dvdt_deceleration(v)
        
    # Check for wheel slip
    if Ft > static_friction:
        print('Ft = ', Ft, 'static friction', static_friction)
        print('Configuration results in wheel slippage')
        return np.array([np.nan, np.nan])
 
        
    return np.array([v, dvdt])