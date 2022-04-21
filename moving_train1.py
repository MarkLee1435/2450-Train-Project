import numpy as np
import matplotlib.pyplot as plt
from rk4 import rk4
from train_motion import train_motion

def interactive_plots(b):
    if b:
        plt.ion()
        plt.show()
    else:
        plt.ioff()

def plot_results(t, x, v, l_track, l_runout, filename=None, title=None,
                 interactive=False):

    plt.clf()
    plt.cla()
    fig, ax1 = plt.subplots()

    # Plot the race
    ax1.plot(t, x, 'b-')

    L = l_track + l_runout
    ax1.set_ylim(0, L+.05*L)
    ax1.set_xlim(0, np.amax(t))
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Distance (m)', color='b')
    ax1.tick_params('y', colors='b')

    # Plot the velocity
    ax2 = ax1.twinx()
    ax2.plot(t, v, 'r-.')
    ax2.set_ylim(0, None)
    ax2.set_ylabel('Velocity (m/s)', color='r')
    ax2.tick_params('y', colors='r')

    # plot the time the track crossed the finish
    t_finish = np.interp(l_track, x, t)
    ax1.plot([t_finish, t_finish], [0, l_track], 'k--', lw=.5)
    ax1.plot([0, t_finish], [l_track, l_track], 'k--', lw=.5)
    ax1.plot([t_finish], [l_track], 'k.', ms=12)
    ax1.plot([0, t[-1]], [L, L], 'k--', lw=.5)
    textstr = r'$t_f={0:.5f}$ (s)'.format(t_finish)
    ax1.text(t_finish+.01*t_finish, l_track-.01*l_track,
             textstr, fontsize=10, verticalalignment='top')

    fig.tight_layout()
    if title is not None:
        plt.suptitle(title)
        plt.subplots_adjust(top=0.925)

    if interactive:
        plt.draw()
        plt.pause(.001)
    elif filename is None:
        plt.show()
    else:
        plt.savefig(filename, transparent=True)

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

    # Initial values
    N = 200
    final_time = 10.0
    
    tspan = np.linspace(0, final_time, N)
    y0 = np.array([0, 0], dtype = float)
    odefun = lambda t,y: train_motion(tspan, y0, p)
    
    t, y = rk4(odefun, tspan, y0)
    
    v = y[:,1]
    x = y[:,0]
    
    plot_results(t, x, v, l_track = 12, l_runout = 15)

print(main())
