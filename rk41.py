
import numpy as np

def rk4(fun, h, tspan, x0, y0, Ls, slipCheck):
    yArr = np.zeros([len(tspan), 2])
    yArr[0,1] = y0
    yArr[0,0] = x0
    
    for i in range(len(tspan)-1):
        k1 = fun[2](yArr[i,1])
        k2 = fun[2](yArr[i,1] + k1 * (h/2))
        k3 = fun[2](yArr[i,1] + k2 * (h/2))
        k4 = fun[2](yArr[i,1] + k3 * h)
        
        yArr[i+1, 0] = yArr[i, 0] + h * (k1/6 + k2/3 + k3/3 + k4/6)
        
        if (fun[3](yArr[i+1,0]) > slipCheck) or (yArr[i+1, 0] > 12.5):
            return None
            
        if yArr[i,0] <= Ls:
            k1 = fun[0](yArr[i,0])
            k2 = fun[0](yArr[i,0] + k1 * (h/2))
            k3 = fun[0](yArr[i,0] + k2 * (h/2))
            k4 = fun[0](yArr[i,0] + k3 * h)    
         
            yArr[i+1, 1] = yArr[i, 1] + h * (k1/6 + k2/3 + k3/3 + k4/6)
            
        elif yArr[i,0] > Ls:
            k1 = fun[1](yArr[i,1])
            k2 = fun[1](yArr[i,1] + k1 * (h/2))
            k3 = fun[1](yArr[i,1] + k2 * (h/2))
            k4 = fun[1](yArr[i,1] + k3 * h)  
        
            yArr[i+1, 1] = yArr[i, 1] + h * (k1/6 + k2/3 + k3/3 + k4/6)
            
        if yArr[i+1,1] < 0 and yArr[i+1, 0] > 10:
            tFinish = tspan[i]
            data = np.column_stack((yArr, tspan))
            return data[:i], tFinish