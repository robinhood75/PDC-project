from utf8_generator import (get_random_unicode, get_8bit_unicode)
from scipy.stats import entropy
from numpy import flip
from math import log

N0=117 # WARNING: N0 should be multiple of 3
assert N0 % 3 == 0
NB_CHARS = 80
ENDIANNESS = 'big'

def bin_to_dec(lst):
    """
    Input: np.array of bits
    Output: associated decimal
    """
    lst = flip(lst)
    dec = 0
    for k, bit in enumerate(lst):
        dec += bit*2**k
    return dec.item()

def transmitter_ascii(s, N0, write=True):
    """
    Inputs:
    str = string of ascii characters
    N0 = design parameter
    Output:
    Goal: fills input.txt with X
    """
    # Convert the string to sequence of 8 bits strings
    str_to_bytes = [bytes(c.encode()) for c in s]
    str_to_int = [int.from_bytes(b,ENDIANNESS) for b in str_to_bytes]
    str_to_binary= ["{0:b}".format(x) for x in str_to_int]
    for i, bitstr in enumerate(str_to_binary):
        if len(bitstr) < 8:
            str_to_binary[i] = (8-len(bitstr))*'0' + bitstr
    str_to_binary = ''.join(str_to_binary)

    # Replicate each bit N0 times
    input = ''.join([bit*N0 for bit in str_to_binary])
    input = list(map(int,input))
    input = [2*x-1 for x in input]

    print("Length of the transmitted sequence: {}".format(len(input)))

    # Fill input.txt
    if write:
        f = open("input.txt", "w+")
        for bit in input:
            f.write(str(bit)+" ")
        f.close() 

def transmitter_utf8(s, N0, write=True):
    """
    Inputs:
    str = string of ascii characters
    N0 = design parameter
    Output:
    Goal: fills input.txt with X
    """
    # Convert the string to sequence of 8 bits strings
    str_to_bytes = [bytes(c.encode('utf-8')) for c in s]
    str_to_int = [int.from_bytes(b,ENDIANNESS) for b in str_to_bytes]
    str_to_binary= ["{0:b}".format(x) for x in str_to_int]
    for i, bitstr in enumerate(str_to_binary):
        if len(bitstr) < 8:
            str_to_binary[i] = (8-len(bitstr))*'0' + bitstr
    str_to_binary = ''.join(str_to_binary)

    # Replicate each bit N0 times
    input = ''.join([bit*N0 for bit in str_to_binary])
    input = list(map(int,input))
    input = [2*x-1 for x in input]

    print("Length of the transmitted sequence: {}".format(len(input)))

    # Fill input.txt
    with open("input.txt", "w") as f:
        for bit in input:
            f.write(str(bit)+" ")

def transmitter_utf8_8bits(s, N0, write=True, compute_entropy=False):
    # Since utf-8 on 8 bits, the MSB will always be 0 so it can be omitted.
    # We pad on 7 instead of 8 bits
    str_to_bin_format = ["{0:07b}".format(ord(i)) for i in s]

    # Compute entropy to see if Huffman is meaningful
    if compute_entropy:
        _to_int = list(map(int,''.join(str_to_bin_format)))
        _entropy = compute_entropy(_to_int)
        print("Entropy of transmitted signal over blocks of 7 bits: {}\n".format(round(_entropy,4)))
    
    # Map 0 to -1
    str_to_bin = [2*int(i)-1 for x in str_to_bin_format for i in x]
    
    # Duplicates each element N0 times
    to_be_transmitted = [str(x) for x in str_to_bin for i in range(N0)]

    print(f"Length of the transmitted sequence: {len(to_be_transmitted)}")

    with open('input.txt', 'w') as f:
        # Add spaces and print to file
        f.write(' '.join(to_be_transmitted) + ' ')

def transmitter_utf8_improved(s, N0, code_e=True):
    # We take advantages of the high number of spaces by encoding them to '1'
    to_transmit = []
    
    if code_e:
        for ch in s:
            if ch == "e":
                to_transmit.append('10')
            elif ch == " ":
                to_transmit.append('11')
            else:
                b = bytes(ch.encode())
                x = int.from_bytes(b,ENDIANNESS)
                bitstr = "{0:b}".format(x)
                if len(bitstr) < 8:
                    bitstr = (8-len(bitstr))*'0' + bitstr
                to_transmit.append(bitstr)
        to_transmit = ''.join(to_transmit)
        
    else:
        for ch in s:
            if ch == " ":
                to_transmit.append('1')
            else:
                b = bytes(ch.encode())
                x = int.from_bytes(b,ENDIANNESS)
                bitstr = "{0:b}".format(x)
                if len(bitstr) < 8:
                    bitstr = (8-len(bitstr))*'0' + bitstr
                to_transmit.append(bitstr)
        to_transmit = ''.join(to_transmit)

    # Map 0 to -1
    str_to_bin = [2*int(i)-1 for i in to_transmit]

    # Duplicates each element the right number of times
    to_be_transmitted = [str(x) for x in str_to_bin for i in range(N0)]

    print(f"Length of the transmitted sequence: {len(to_be_transmitted)}")

    with open('input.txt', 'w') as f:
        # Add spaces and print to file
        f.write(' '.join(to_be_transmitted) + ' ')


def compute_entropy(bin_seq, nb_bits=7):
    """
    Compute the entropy of the distribution of packets of nb_bits
    """
    N = len(bin_seq)
    counter = [0]*2**nb_bits
    for i in range(int(N/nb_bits)):
        seq_nb_bits = bin_seq[nb_bits*i:nb_bits*(i+1)]
        counter[bin_to_dec(seq_nb_bits)] += 1
    distrib = [p/N for p in counter]
    return entropy(distrib)/log(2**nb_bits)

s = "Here is another sentence of rougly 80 characters. Or maybe a little bit less? No.."
#s=" "
#s = get_random_unicode(10)
#s = get_8bit_unicode(NB_CHARS)

print(s.encode('utf-8'), f"{len(s.encode('utf-8'))} bytes")

with open('message.txt', 'wb') as f:
    for i in s:
        f.write(i.encode('utf-8'))
    f.write('\n'.encode('utf-8'))

transmitter_utf8_improved(s, N0, code_e=True)
