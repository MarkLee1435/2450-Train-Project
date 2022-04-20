import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from train_motion import train_motion
from rk4 import rk4

def main():
    p = np.zeros(14)
    p[0] = 9.81  # gravity
    p[1] = 1.0  # air density
    p[2] = 10 # train mass
    p[3] = 0.05  # frontal area
    p[4] = 0.8  # drag coefficient
    p[5] = 0.03  # rolling coefficient
    p[6] = 100000; # gauge pressure (Pa)
    p[7] = 0.01; # radius of piston (m)
    p[8] = 0.01; # radius of gear (m)
    p[9] = 0.025; # radius of wheel (m)
    p[10] = 0.1; # mass of wheel (kg)
    p[11] = 0.7; # coefficient of static friction (between wheel and track)
    p[12] = 0.1; # piston stroke length (m)
    
    odefun = lambda t,y: train_motion(t, y, p)

    # Initial values
    y0 = np.array([0, 0], dtype=float)

    N = 2000
    final_time = 20.0
    tspan = np.linspace(0, final_time, N)

    # Call 4th order Runge-Kutta method
    t_rk, y_rk = rk4(odefun, tspan, y0)
    
    x_rk = y_rk[:,0]
    v_rk = y_rk[:,1]

    plt.figure(1)
    plt.plot(t_rk, v_rk,label='4th-Order Runge-Kutta')
    plt.title('Simulation of a Moving Train')
    plt.ylabel('Velocity (m/s)')
    plt.xlabel('Time (seconds)')

    plt.title('Simulation of a Moving Train')
    plt.ylabel('Position (m)')
    plt.xlabel('Time (seconds)')
    

    plt.show()
    #
    #plt.figure(2)
    #plt.plot(t_rk,y_rk[:,1],t_rk2,y_rk2[:,1],t_rk3,y_rk3[:,1],t_rk4,y_rk4[:,1])
    plt.tight_layout()
    #plt.savefig("moving_train_result.pdf")
    plt.clf()
    

if __name__ == '__main__':
    main()
