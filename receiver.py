import numpy as np

N0=105
assert N0 % 3 == 0
ENCODING = 'utf-8'

def load_signal(N0, filename='output.txt'):
    # Load the received signal
    out = np.loadtxt(filename)
    n = out.shape[0]
    if n % N0 !=0:
        raise ValueError("Transmitted signal has incorrect length")
    return (out, n)

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

def decode_utf8_8bits(N0, H_hat):
    """
    Decodes the signal under an utf-8 transmitter design optimized for 8bits utf-8:
    Takes the sign of the average over 2*N0/3 transmissions of the same bit
    """
    if N0 % 3 != 0:
        raise ValueError('Warning: N0 should be multiple of 3')
    N0_eff = 2*N0//3

    out, n = load_signal(N0)

    out_clean = [out[i] for i in range(len(out)) if i % 3 != H_hat]
    if len(out_clean) % N0_eff != 0:
        raise ValueError('Warning: length of out_clean should be multiple of N0_eff')

    averages = [sum(out_clean[k*N0_eff : (k+1)*N0_eff]) for k in range(n//N0)]

    # Map to -1, 0 or 1
    decoded_bits = np.sign(np.array(averages))

    # Map to binary
    decoded_bits = ((decoded_bits+1)/2).astype(int)

    decoded_ints = [int(''.join(decoded_bits[7*i:7*(i+1)].astype(str)), 2) for i in range(len(decoded_bits)//7)]
    decoded_bytes = bytes(decoded_ints)

    print(f"Decoded bytes:\n{decoded_bytes}", f"{len(decoded_bytes)} bytes")

    decoded_string = decoded_bytes.decode(ENCODING)

    return decoded_string

index, H_MAP = estimate_H()
print("Deleted index: {} (from the following estimate: {})\n".format(index, H_MAP))

decoded_string = decode_utf8_8bits(N0, index)
print("Decoded string using N0={}:".format(N0), decoded_string)

original_message = None
with open('message.txt', 'rb') as f:
    original_message = f.read().decode(ENCODING).strip()

if original_message:
    print("Original message was: '", original_message, "'", sep='')

    errors = dict()
    for i in range(len(original_message)):
        if original_message[i] != decoded_string[i]:
            errors[i] = {'original': original_message[i], 'decoded': decoded_string[i] }

    print(f"Total number of errors: {len(errors)}")
    for i,e in errors.items():
        print(f' - index {i}:')
        print('\texpected this: {0:08b}'.format(ord(e["original"])), end='')
        print(f' -> {e["original"].encode(ENCODING)} -> {e["original"]}')
        print('\tand got this : {0:08b}'.format(ord(e["decoded"])), end='')
        print(f' -> {e["decoded"].encode(ENCODING)} -> {e["decoded"]}')
