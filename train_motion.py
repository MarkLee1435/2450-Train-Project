import numpy as np

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
   
   #constants
    air_density = 1
    pressure_atm = 101325
    drag_coefficient = 0.8
    rolling_coefficient = 0.03
    cf_static = 0.7
    wheel_radius = 0.02
    wheel_mass = 0.1
    density_material = 4500
    g = 9.81
    
    #ranges
    # tank_length = np.arange(0.2,0.3,0.01)
    # tank_radius = np.arange(0.05,0.2,0.01)
    # P_gauge = np.arange(70000,2000000,10)
    # gear_radius = np.arange(0.002,0.01,0.001)
    # piston_length = np.arange(0.1,0.5,0.01)
    # piston_radius = np.arange(0.02,0.04,0.001)
    
    tank_length = 0.2
    tank_radius = 0.05
    P_gauge = 125000
    gear_radius = 0.05
    piston_length = 0.1
    piston_radius = 0.04
    tank_density = 4500 
    
    #find area of tank
    frontal_area = np.pi * tank_radius**2;
    
    # Assign inputs to variables
    y, v = y0[0:2]
    
    if abs(y) > 0 and v < 0:
        return np.nan * np.ones(2)

    # Calculate forces
    
    # find total mass except wheel mass    
    tank_mass = ((np.pi * (tank_radius**2) * tank_length * tank_density))
    
    total_mass = train_mass + tank_mass
    
    Ap = np.pi * piston_radius**2;
   
    drag_force = 0.5 * air_density * frontal_area * density_material * drag_coefficient * v**2;
    
    rolling_friction = total_mass * gravity * rolling_coefficient;
            
    volume = np.pi * tank_radius**2 * tank_length;
	# Determine whether accelerating or decelerating
    x_transition = piston_length * wheel_radius/gear_radius;
    
    #find Ft    
    Ft = ((gear_radius * Ap) /wheel_radius) * ((P_gauge * volume)/(volume + Ap * (gear_radius/wheel_radius) * x_transition) - pressure_atm)
    
    # Calculate derivative estimates
    if y < x_transition: # accelerating
        a = (1/ (total_mass + wheel_mass)) * (Ft - drag_force - rolling_friction) 
    else: # decelerating
        a = (1/(total_mass)) * (-drag_force - rolling_friction)
        
    # Check for wheel slip
    Ft = ((gear_radius * Ap) /wheel_radius) * ((P_gauge * volume)/(volume + Ap * (gear_radius/wheel_radius) * x_transition) - pressure_atm) - (wheel_mass*a)    

    static_friction = cf_static*(total_mass + wheel_mass)/2*g;
    if (Ft) > static_friction:
        print('Ft = ', Ft)
        print('static friction =', static_friction)

        raise ValueError('Configuration results in wheel slippage')

    # Assemble output vector
    return np.array([v, a])
