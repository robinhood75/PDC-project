from utf8_generator import (get_random_unicode, get_8bit_unicode)
from scipy.stats import entropy
from numpy import flip
from math import log

N0=3 # WARNING: N0 should be multiple of 3
assert N0 % 3 == 0
NB_CHARS = 2
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

def transmitter_utf8_8bits(s, N0, write=True):
    # Since utf-8 on 8 bits, the MSB will always be 0 so it can be omitted.
    # We pad on 7 instead of 8 bits
    str_to_bin_format = ["{0:07b}".format(ord(i)) for i in s]
    
    # Map 0 to -1
    str_to_bin = [2*int(i)-1 for x in str_to_bin_format for i in x]
    
    # Duplicates each element N0 times
    to_be_transmitted = [str(x) for x in str_to_bin for i in range(N0)]

    print(f"Length of the transmitted sequence: {len(to_be_transmitted)}")

    with open('input.txt', 'w') as f:
        # Add spaces and print to file
        f.write(' '.join(to_be_transmitted) + ' ')

dic = {
    "e": '1000',
    " ": '1001',
    "t": '1010',
    "a": '1011',
    "o": '1100',
    "i": '1101',
    "n": '1110',
    "s": '1111'
    }

def transmitter_with_dic(s, N0, dic):
    to_transmit = []

    for ch in s:
        if ch in dic:
            to_transmit.append(dic[ch])
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

def transmitter_utf8_8bits_adapted(s, N0_4, N0_3, write=True):
    """
    Idea: split each 7 bytes words into two parts of 4 and 3 bytes
    Input:
        N0_4: Number of times we duplicate each bit of each 4-bit elements
        N0_3: Number of times we duplicate each bit of each 3-bit elements
    """

    # Convert to int
    char_to_int = [ord(i) for i in s]
    #print(char_to_int)

    # Split each 7 bit-int into two 4-bit and 3-bit ints
    splitted_int = [(i >> 3, i % 2**3) for i in char_to_int]
    #print(splitted_int)

    # Binary signal in [-1,1]^{16} and [-1,1]^{8}
    converted_int = [(['-1']*(15-i4) + ['1'] + ['-1']*(i4), ['-1']*(7-i3) + ['1'] + ['-1']*(i3)) for i4,i3 in splitted_int]
    #for e in converted_int:
    #    print(e)

    #print('Duplication:')
    duplicated = [[x for x in i4 for i in range(N0_4)] + [x for x in i3 for i in range(N0_3)] for i4, i3 in converted_int]

    to_be_transmitted = []
    for d in duplicated:
        to_be_transmitted += d
    #print(to_be_transmitted)
    
    print(f"Length of the transmitted sequence: {len(to_be_transmitted)}")
    
    with open('input.txt', 'w') as f:
        # Add spaces and print to file
        f.write(' '.join(to_be_transmitted) + ' ')
    
#s = "Probably one more 80 characters sentence that's clearly waaaaaaay longer than this"
#s = get_random_unicode(10)
s = get_8bit_unicode(NB_CHARS)

print(s.encode('utf-8'), f"{len(s.encode('utf-8'))} bytes")

with open('message.txt', 'wb') as f:
    for i in s:
        f.write(i.encode('utf-8'))
    f.write('\n'.encode('utf-8'))

transmitter_utf8_8bits_adapted(s, N0, N0)
