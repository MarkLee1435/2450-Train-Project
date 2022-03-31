# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:44:43 2022

@author: mjlee
"""
import numpy as np
import matplotlib.pyplot as plt
        
def euler(odefun, tspan, y0):
    
    y = np.zeros((2,len(tspan)))
    y[:,0] = y0
    
    for i in range(1,tspan.shape[0]):
        h = tspan[i] - tspan[i-1]
        y[:,i] = y[:,i-1] + h*(odefun(tspan[i-1], y[:,i-1]))
        
    return y

def rk4(odefun, tspan, y0):
    
    
    n = len(tspan)
    y = np.zeros((n, len(y0)))
    y[0] = y0
    
    for i in range(n - 1):
        
        h = tspan[i+1] - tspan[i]
        k1 = odefun(tspan[i],y[i])
        k2 = odefun(tspan[i] + h / 2., y[i] + k1 * h / 2.)
        k3 = odefun(tspan[i] + h / 2., y[i] + k2 * h / 2.)
        k4 = odefun(tspan[i] + h, y[i] + k3 * h)
        y[i+1] = y[i] + (h / 6.) * (k1 + 2*k2 + 2*k3 + k4)
        
    return y.T
        
def train_motion(t,y,params):
    
    x,v = y[0], y[1]
    
    g = params[0]
    rho = params[1]
    m = params[2]
    A = params[3]
    Cd = params[4]
    Crr = params[5]
    L_s = params[6]
    r_w = params[7]
    r_g = params[8]
    m_w = params[9]
    u_s = params[10]
    p_g = params[11]
    r_p = params[12]
    
    Fd = (rho * Cd * A * v**2)/2
    
    Frr = m*g*Crr
    
    L_a = (L_s * r_w)/r_g
    
    if (x > L_a):
        dvdt = (1/m)*(-Fd - Frr)
    else:
        Fp = p_g *np.pi* (r_p**2)
        T = r_g * Fp
        dvdt = (1/(m+2*m_w)) * ((T/r_w) + (-Fd - Frr))
        
    if (-Fd-Frr) > (u_s * g * (m/2)):
        raise ValueError('The wheels will slip')

    dydt = [v,dvdt]
    
    return np.array(dydt)


g = 9.81
rho = 1
m = 10
A = 0.05
Cd = 0.4
Crr = 0.03
L_s = 0.1
r_w = 2.5/100
r_g = 1.0/100
m_w = 0.1
u_s = 0.7
p_g = 100*1000
r_p = 1/100

params = [g,rho,m,A,Cd,Crr,L_s, r_w, r_g, m_w, u_s, p_g, r_p]
y0 = np.array([0,0])
tspan = np.arange(0,11)

odefun = lambda t,y: train_motion(tspan,y,params)

y = rk4(odefun, tspan, y0)

plt.plot(tspan,y[1,:], label = 'Velocity')   
plt.plot(tspan,y[0,:], label = 'Position')
plt.title('Train Position / Velocity')
plt.xlabel('Time')
plt.ylabel('Position / Velocity')
plt.grid(True)
plt.legend()





