import numpy as np
import matplotlib.pyplot as plt
from rk4 import rk4
from scipy.optimize import minimize 
from train_motion import train_motion

def interactive_plots(b):
    if b:
        plt.ion()
        plt.show()
    else:
        plt.ioff()

def plot_results(t, y, l_track, l_runout, filename=None, title=None,
                 interactive=False):
   
    x, v = y[:,0], y[:,1]
    
    plt.clf()
    plt.cla()
    fig, ax1 = plt.subplots()

    # Plot the race
    ax1.plot(t, x, 'b-')

    L = l_track + l_runout
    ax1.set_ylim(0, None)
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
        
def train_motion_wrapper(const_p, var_p, rho_materials, t_final=20, n=200, return_only_time=True):
    
    tspan = np.linspace(0, t_final, n)
    
    odefun = lambda t, y: train_motion(t, y, const_p, var_p, material_density=8000)
    
    t, y = rk4(odefun, tspan, np.array([0.,0.]))
    
    if return_only_time is True:
        if y[:,0].max() > 12.5 and y[:,0].max() < 10:
            
            return np.inf()
        
        return t[-1]
    
    return t, y

def main():

    const_p = np.array([1.0, 101324.0, 0.8, 0.03, 0.7, 0.02, 0.1])
    var_p = np.array([0.25, 0.115, 115000.0, 0.005, 0.3, 0.032])
    rho_t = {'PVC':1400, 'acrylic':1200, 'galvanized_steel':7700, 'stainless_steel':8000,
          'titanium':4500, 'copper':8940, 'aluminium':2700}

    
    wrap_of_wrapper = lambda var_params: train_motion_wrapper(const_p, var_params, rho_t, return_only_time=False)
    
    #print(wrap_of_wrapper(var_p, True), 'yay')
    #print(wrap_of_wrapper(var_p, False), 'boo')
    
    t , y = wrap_of_wrapper(var_p)
    
    plot_results(t, y, l_track = 10, l_runout = 2.5)
    '''
   
    Lt = (.2,.3)        # m
    ro = (0.05, 0.2)    # m
    P0 = (70000,200000)  # Pa
    rg = (0.002,0.01)   # m
    Ls = (0.1,0.5)      # m         
    rp = (0.02, 0.05)   # m
    
    rho_air = 1.0
    P_atm = 101324.0
    C_d = 0.8
    C_r = 0.03
    mu_s = 0.7
    r_w = 0.02
    m_w = 0.1
    
    t , y = wrap_of_wrapper(var_p, False)
    
    plot_results(t, y, l_track = 10, l_runout = 2.5)
    bounds = (Lt, ro, P0, rg, Ls, rp)
    var_p = np.array([Lt, ro, P0, rg, Ls, rp])
    const_p = np.array([rho_air, P_atm,C_d, C_r, mu_s, r_w, m_w])
    keys = rho_t.keys()
    times = []
    x0 = var_p
    
    for key in keys:
        
        const_p = np.array([rho_air, P_atm,C_d, C_r, mu_s, r_w, m_w])
        
        drive = wrap_of_wrapper() 
        
        res = minimize(drive, x0, bounds = bounds, method='Nelder-Mead')
        
        times.append(drive(res.x))
        
        print('the outputs of minization are:\n', x0, times, file = open)
        '''
print(main())
