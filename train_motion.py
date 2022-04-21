import numpy as np
import random
from rk41 import rk4


def train_motion(t, y0, p):
    gravity = p[0] #g
    air_density = p[1] #rho
    train_mass = p[2] #m
    frontal_area = p[3] #A
    drag_coefficient = p[4] #Cd
    rolling_coefficient = p[5] #Cr
    P_gauge = p[6] #P0gauge
    piston_radius = p[7] #rp
    gear_radius = p[8] #rg
    wheel_radius = p[9] #rw
    wheel_mass = p[10] #mw
    cf_static = p[11] #s
    piston_length = p[12]

   #plug in known values and ranges
    air_density = 1
    pressure_atm = 101325
    drag_coefficient = 0.8
    rolling_coefficient = 0.03
    cf_static = 0.7
    wheel_radius = 0.02
    wheel_mass = 0.1
    Pp = 1250
    
    #conditions for for loop
    N = 200
    final_time = 10.0
    tspan = np.linspace(0, final_time, N)
    
    for i in range(N):
        i += 1
        
        #values to be optimized
        tank_length =   np.random.rand(np.random.uniform(.2,.3),3)
        tank_radius =   np.random.rand(np.random.uniform(.05,.2),3)
        tank_density =  1400
        tankMat = tank_density
        P_gauge =       np.random.rand(np.random.uniform(70000,200000),3)
        gear_radius =   np.random.rand(np.random.uniform(.002,.01),3)
        piston_length = np.random.rand(np.random.uniform(.1,.5),3)
        piston_radius = np.random.rand(np.random.uniform(.02,.04),3)
        
        #find area of tank
        ri = tank_radius/1.15  #inner radius
        frontal_area = np.pi * tank_radius**2; 
        
        # Assign inputs to variables
        x0, v0 = y0[0:2]
        
        if abs(x0) > 0 and v0 < 0:
            return None
        
        # find total mass except wheel mass  
        
        Ap = np.pi * piston_radius**2
        
        piston_mass = Ap * piston_length * Pp
        tank_mass = (((np.pi * (tank_radius**2) * tank_length) - (np.pi * (ri**2) * tank_length)) * tank_density)
        total_mass = train_mass + tank_mass + piston_mass
       
        drag_force = 0.5 * air_density * frontal_area * drag_coefficient * v0**2
        print(air_density, frontal_area, drag_coefficient,v0,drag_force)
        
        rolling_friction = total_mass * gravity * rolling_coefficient
        volume = np.pi * tank_radius**2 * tank_length
        
    	# Determine whether accelerating or decelerating
        x_transition = piston_length * wheel_radius/gear_radius
        
        #find Ft    
        Ft = ((gear_radius * Ap) /wheel_radius) * (((P_gauge + pressure_atm) * volume)/(volume + (Ap * (gear_radius/wheel_radius) * x_transition)) - pressure_atm)
        '''
        if y < x_transition: # accelerating
            a = (1/ (total_mass + wheel_mass)) * (Ft - drag_force - rolling_friction) 
            print('a = ', a)
            
        else: # decelerating
            a = (1/(total_mass)) * (-drag_force - rolling_friction)
            print('a = ', a)
          '''
        # Calculate derivative estimates
        dvdt_acceleration = lambda x, v: (1/ (total_mass + wheel_mass)) * (Ft - drag_force - rolling_friction) 
        dvdt_deceleration = lambda v: (1/(total_mass)) * (-drag_force - rolling_friction)
        dxdt = lambda v: v
        Ft1 = lambda x: (1/ (total_mass + wheel_mass)) * ((gear_radius * Ap) /wheel_radius) * (((P_gauge + pressure_atm) * volume)/(volume + (Ap * (gear_radius/wheel_radius) * x)) - pressure_atm)
        
        static_friction = cf_static * ((total_mass + wheel_mass) / 2) * gravity
        
        # Check for wheel slip
        if (Ft1) > static_friction:
            print('Ft = ', Ft1)
            print('static friction', static_friction)
            raise ValueError('Configuration results in wheel slippage')

        # Assemble output vector
        trainMotion = np.array([dvdt_acceleration,dvdt_deceleration, dxdt, Ft1])
        
        Wt = 2 * tank_radius
        Ht = 2 * tank_radius + 2 * wheel_radius
        slipCheck = static_friction
        h = 3
        Ls = 2
        La =   Ls * wheel_radius/gear_radius
        best_time = 0
        
        if (Ht < .23) and (Wt < .2) and (gear_radius/wheel_radius < 1):
            if rk4(trainMotion,h,tspan,v0,x0,La,slipCheck) is not None and rk4(trainMotion, h, tspan, v0, x0, La, slipCheck)[1] < best_time:
                data = rk4(trainMotion,h,tspan,v0,x0,La,slipCheck)[0]
                best_time = rk4(trainMotion,h,tspan,v0,x0,La,slipCheck)[1]
                best_params = np.array([tank_radius, P_gauge, gear_radius, Ls, piston_radius])
                
                if tankMat == 1400:
                    best_tank_mat = 'PVC pipe'
                    
                elif tankMat == 1200:
                    best_tank_mat = 'Acrylic'
                    
                elif tankMat == 7700:
                    best_tank_mat = 'Galvanized Steel'
                    
                elif tankMat == 8000:
                    best_tank_mat = 'Stanless Steel'
                    
                elif tankMat == 4500:
                    best_tank_mat = 'Titanium'
                    
                elif tankMat == 8940:
                    best_tank_mat = 'Copper'
                    
                elif tankMat == 2700:
                    best_tank_mat = 'Alluminium'
                
            return best_tank_mat, data , best_time, best_params
