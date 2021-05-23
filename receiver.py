import numpy as np

N0=102
assert N0 % 3 == 0
ENDIANNESS = 'big'

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

def load_signal(N0, filename='output.txt'):
    # Load the received signal
    out = np.loadtxt(filename)
    n = out.shape[0]
    if n % N0 !=0:
        return "Transmitted signal has incorrect length"
    return out

def decode_ascii(N0, H_hat):
    """
    Decodes the signal under ascii transmitter design:
    Take the sign of the average over 2*N0/3 transmissions of the same bit
    """
    out = load_signal(N0)
    n = out.shape[0]

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
    decoded_string = ''.join([x.to_bytes(1,ENDIANNESS).decode('ascii') for x in decoded_ints])

    return decoded_string

def decode_utf8(N0, H_hat):
    """
    Decodes the signal under utf-8 transmitter design:
    Takes the sign of the average over 2*N0/3 transmissios of the same bit
    """
    if N0 % 3 != 0:
        raise ValueError('Warning: N0 should be multiple of 3')
    N0_eff = 2*N0//3

    out = load_signal(N0)
    n = out.shape[0]

    out_clean = [out[i] for i in range(len(out)) if i % 3 != H_hat]
    if len(out_clean) % N0_eff != 0:
        raise ValueError('Warning: length of out_clean should be multiple of N0_eff')

    averages = [sum(out_clean[k*N0_eff : (k+1)*N0_eff]) for k in range(n//N0)]
    
    # Map to -1, 0 or 1
    decoded_bits = np.sign(np.array(averages))
    
    # Map to binary
    decoded_bits = ((decoded_bits+1)/2).astype(int)
    decoded_ints = [int(''.join(decoded_bits[8*i:8*(i+1)].astype(str)), 2) for i in range(len(decoded_bits)//8)]
    decoded_bytes = bytes(decoded_ints)

    print(len(decoded_bits)//8, 'bytes')

    print(decoded_ints)
    print(decoded_bytes)

    decoded_string = decoded_bytes.decode('utf-8')

    return decoded_string

index, H_MAP = estimate_H()
print("H_MAP = {} \nRemember: noise has std dev = 10".format(H_MAP))

decoded_string = decode_utf8(N0, index)
print("Decoded string using N0={}:".format(N0), decoded_string)

original_message = None
with open('message.txt', 'rb') as f:
    original_message = f.read().decode('utf-8').strip()

if original_message:
    print("Original message was: '", original_message, "'", sep='')

    errors = dict()
    for i in range(len(original_message)):
        if original_message[i] != decoded_string[i]:
            errors[i] = {'original': original_message[i], 'decoded': decoded_string[i] }

    print(f"Total number of errors: {len(errors)}")
    for i,e in errors.items():
        print(f' - index {i}:')
        print(f'\texpected this: {bin(ord(e["original"]))} -> {e["original"].encode("utf-8")} -> {e["original"]}')
        print(f'\tand got this : {bin(ord(e["decoded"]))} -> {e["decoded"].encode("utf-8")} -> {e["decoded"]}')