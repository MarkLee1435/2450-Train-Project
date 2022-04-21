import numpy as np

def rk4(odefun, tspan, y0):
    """ Performs the 4th-Order Runge-Kutta Method to solve a system of ordinary
    differential equations with an arbitrary number of equations
    """

    # Determine the number of items in the outputs
    tspan = np.asarray(tspan)
    num_steps = tspan.shape[0]
    y0 = np.asarray(y0)
    num_states = y0.shape[0]

    # Initialize the outputs
    t = tspan
    y = np.zeros((num_steps, num_states))

    # Assign the first row of outputs
    t[0] = tspan[0]
    y[0,:] = y0[:]

    # Start the loop
    for k in range(num_steps-1):

        # Calculate the slope
        h = tspan[k+1] - tspan[k]
        k1 = odefun(t[k], y[k,:])       
        k2 = odefun(t[k]+.5*h, y[k,:]+.5*k1*h)
        k3 = odefun(t[k]+.5*h, y[k,:]+.5*k2*h)
        k4 = odefun(t[k]+h, y[k,:]+k3*h)
        
        if np.any(np.isnan(np.array([k1,k2,k3,k4]))):
            """
            Checks for wheel slip
            """
            return np.array([np.inf]), np.ones(y.shape)*np.inf
        
        if np.any(np.isinf(np.array([k1,k2,k3,k4]))):
            """
            Checks for when train stops moving
            """
            return t[:k], y[:k,:]
        
        slope = (k1 + 2*k2 + 2*k3 + k4) / 6.
        
        # Calculate the next state
        y[k+1,:] = y[k,:] + slope * h


    return t, y
