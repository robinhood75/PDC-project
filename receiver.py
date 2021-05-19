import numpy as np

# This can be run from the terminal

N0=90

def estimate_H():
    """
    Estimate H by outputing min average y**2 among i=0,1,2
    Works independantly of the transmitter design
    """
    out = np.loadtxt("output.txt")
    n = out.shape[0]
    n_eff = n-n%3
    MAP = np.zeros(3)
    for i, y in enumerate(out[:n_eff]):
        MAP[i%3] += y**2
    MAP /= n_eff/3
    return np.argmin(MAP), MAP

index, H_MAP = estimate_H()
print("H_MAP = {} \nRemember: noise has std dev = 10".format(H_MAP))

def bin_to_dec(lst):
    """
    Input: np.array of bits
    Output: associated decimal
    """
    lst = np.flip(lst)
    dec = 0
    for k, bit in enumerate(lst):
        dec += bit*2**k
    return dec.item()

def decode_ascii(N0, H_hat):
    """
    Decodes the signal under ascii transmitter design:
    Take the sign of the average over 2*N0/3 transmissions of the same bit
    """
    # Load the received signal
    out = np.loadtxt("output.txt")
    n = out.shape[0]
    if n%N0 !=0:
        return "Transmitted signal has incorrect length"

    # Drop the useless data
    out_clean = []
    for i, y in enumerate(out):
        if i%3 != H_hat: out_clean.append(y)
    if N0%3 != 0:
        return "WARNING: N0 should be multiple of 3"
    N0_eff = int(2*N0/3)

    # Make a prediction for the n/N0 original bits
    averages = [sum(out_clean[k*N0_eff:(k+1)*N0_eff]) for k in range(int(n/N0))]
    decoded_bits = np.sign(np.array(averages))
    decoded_bits = (decoded_bits+1)/2
    decoded_bits = decoded_bits.astype(int)
    
    # Retreive the original string
    decoded_ints = [bin_to_dec(decoded_bits[8*k:8*(k+1)])%128 for k in range(int(len(decoded_bits)/8))] # %ideally %128 to be discarded
    decoded_string = ''.join([x.to_bytes(1,'big').decode('ascii') for x in decoded_ints])

    return decoded_string

decoded_string = decode_ascii(N0, index)
print("decoded string using N0={}:".format(N0), decoded_string)
        
