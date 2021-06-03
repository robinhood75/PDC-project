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
    
    if filter == 'moving average':
        # pad with 0s on the right and on the left to keep the same size
        avged_y = np.zeros(len(y))
        padded_y = np.pad(np.array(y), (m//2,m//2))
        for k in range(avged_y.size):
            avged_y[k] = np.sum(padded_y[k:k+m])/m
        return avged_y

def get_charac(signal, psi, T_min, T_max, T, removed_index):
    """
    Performs w_hat dot psi_j for every j to recover the bits
    """
    bits = [0]*7
    N0 = 3*signal.shape[0]//2
    dt = (T_max-T_min)/N0
    
    grid = []
    for i in range(N0):
        if i%3 != removed_index:
            grid.append(T_min + i*dt)
            
    for k in range(7):
        psi_k = np.array([psi(t - k*T, T) for t in grid])
        dot_product = signal.dot(psi_k)
        bits[k] = (np.sign(dot_product)+1)/2

    bits = np.array(bits)
    decoded_ints = [int(bits.dot(np.flip(np.array([2**k for k in range(7)]))))]
    decoded_bytes = bytes(decoded_ints)
    
    return decoded_bytes.decode('utf-8'), bits
