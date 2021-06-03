# -*- coding: utf-8 -*-
import numpy as np

def encoder(s: str) -> [int]:
    return np.array([int(c) for i in s for c in "{0:07b}".format(ord(i))])
    
def mapper(s: [int]) -> [int]:
    return np.array(s*2 - 1)

def w(t, c_i, psi, T):
    """
    c_i is the sequence of codes, psi a function, T the time interval of the pulse train
    Returns the pulse train signal
    """
    return np.array(sum( [c_i[i]*psi(t - i*T, T) for i in range(len(c_i))] ))
    
def sample(w, T, T_min, T_max):
    """
    sample w every T time interval between T_min and T_max
    """
    if T_min >= T_max:
        raise ValueError(f'T_max ({T_max}) needs to be greater than T_min ({T_min})')
        
    t = np.linspace(T_min, T_max, T)
    return w(t)
