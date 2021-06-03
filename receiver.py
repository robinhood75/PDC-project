# -*- coding: utf-8 -*-
import numpy as np

def remove_index(out):
    """
    remove deleted index
    """
    n = out.shape[0]
    n_eff = n-n%3
    estim = np.zeros(3)
    for i, y in enumerate(out[:n_eff]):
        estim[i%3] += y**2
    estim /= n_eff/3
    H_hat = np.argmin(estim)
    
    out_clean = []
    for i, y in enumerate(out):
        if i%3 != H_hat:
            out_clean.append(y)
            
    return out_clean, H_hat

def remove_noise(y, m, filter='moving average'):
    """
    Filter the noisy signal to remove noise
    Parameters:
        y: signal to filter
        m: window size
    """
    # Careful: filter reduces size of y, pad y with 0s to keep same size
    
    if filter == 'moving average':
        # Moving average taken from: https://stackoverflow.com/a/14314054
        ret = np.cumsum(y, dtype=float)
        ret[m:] = ret[m:] - ret[:-m]
        return ret[m - 1:] / m

def get_charac(w_hat, psi, T_min, T_max, T):
    """
    Performs w_hat dot psi_j for every j to recover the bits
    """
    bits = [0]*7
    N0_eff = 2*(T_max-T_min)/T//3
    for k in range(7):
        signal = np.array(w_hat[k*N0:(k+1)*N0])
        dot_product = signal.dot(np.array([psi(j*T) for j in range(N0_eff//7)]))
        bits[k] = (np.sign(dot_product)+1)/2
        
    decoded_ints = [int(''.join(bits[7*i:7*(i+1)].astype(str)), 2) for i in range(len(bits)//7)]
    decoded_bytes = bytes(decoded_ints)
    
    return decoded_bits.decode('utf-8')