from utf8_generator import get_random_unicode

N0=102 # WARNING: N0 should be multiple of 3
assert N0 % 3 == 0
ENDIANNESS = 'big'

def transmitter_ascii(s, N0, write=True):
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
    if write:
        f = open("input.txt", "w+")
        for bit in input:
            f.write(str(bit)+" ")
        f.close()

s = get_random_unicode(10) #"hello, my name is Arthur, and I'm 22. I know, this is kind of old."

print(len(s.encode('utf-8')), 'bytes')
print(s.encode('utf-8'))

with open('message.txt', 'wb') as f:
    for i in s:
        f.write(i.encode('utf-8'))
    f.write('\n'.encode('utf-8'))

transmitter_ascii(s, N0)
