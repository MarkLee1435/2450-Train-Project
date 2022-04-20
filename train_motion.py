import numpy as np
import random as rd

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
    
    for i in range(10):
        i += 1
        
        #values to be optimized
        #tank_length = rd.random.rand(rd.random.uniform(.2,.3),3)
        tank_length = .2
        tank_radius = 0.05
        tank_density = 9000 
        P_gauge = 70000
        gear_radius = 0.05
        piston_length = 0.1
        piston_radius = 0.04
        
        #find area of tank
        ri = tank_radius/1.15  #inner radius
        
        frontal_area = np.pi * tank_radius**2; 
        
        # Assign inputs to variables
        y, v = y0[0:2]
        
        if abs(y) > 0 and v < 0:
            return None
        
        # find total mass except wheel mass  
        
        Ap = np.pi * piston_radius**2
        
        piston_mass = Ap * piston_length * Pp
        
        tank_mass = (((np.pi * (tank_radius**2) * tank_length) - (np.pi * (ri**2) * tank_length)) * tank_density)
        
        total_mass = train_mass + tank_mass + piston_mass
       
        drag_force = 0.5 * air_density * frontal_area * drag_coefficient * v**2
    
        print(air_density, frontal_area, drag_coefficient,v,drag_force)
        
        rolling_friction = total_mass * gravity * rolling_coefficient
                
        volume = np.pi * tank_radius**2 * tank_length
        
    	# Determine whether accelerating or decelerating
        x_transition = piston_length * wheel_radius/gear_radius
        
        #find Ft    
        Ft = ((gear_radius * Ap) /wheel_radius) * (((P_gauge + pressure_atm) * volume)/(volume + (Ap * (gear_radius/wheel_radius) * x_transition)) - pressure_atm)
        
        # Calculate derivative estimates
        '''
        if y < x_transition: # accelerating
            a = (1/ (total_mass + wheel_mass)) * (Ft - drag_force - rolling_friction) 
            print('a = ', a)
            
        else: # decelerating
            a = (1/(total_mass)) * (-drag_force - rolling_friction)
            print('a = ', a)
          '''
          
        dvdt_acceleration = lambda x, v: (1/ (total_mass + wheel_mass)) * (Ft - drag_force - rolling_friction) 
        dvdt_deceleration = lambda v: (1/(total_mass)) * (-drag_force - rolling_friction)
        dxdt = lambda v: v
        Ft1 = lambda x: (1/ (total_mass + wheel_mass)) * ((gear_radius * Ap) /wheel_radius) * (((P_gauge + pressure_atm) * volume)/(volume + (Ap * (gear_radius/wheel_radius) * x)) - pressure_atm)
        
        # Assemble output vector
        trainMotion = np.array([dvdt_acceleration,dvdt_deceleration, dxdt, Ft1])
        
        static_friction = cf_static * ((total_mass + wheel_mass) / 2) * gravity
        
        # Check for wheel slip
        if (Ft) > static_friction:
            print('Ft = ', Ft)
            print('static friction', static_friction)
            raise ValueError('Configuration results in wheel slippage')

        return trainMotion
