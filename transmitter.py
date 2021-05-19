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
    str_to_int = [int.from_bytes(b,"big") for b in str_to_bytes]
    str_to_binary= ["{0:b}".format(x) for x in str_to_int]
    for i, bitstr in enumerate(str_to_binary):
        if len(bitstr) < 8:
            str_to_binary[i] = (8-len(bitstr))*'0' + bitstr

    # Duplicate each sequence of 8 bits N0 times
    str_to_binary = [bitstr*N0 for bitstr in str_to_binary]
    input = ''.join(str_to_binary)
    input = list(map(int,input))
    input = [2*x-1 for x in input]

    print("Length of the transmitted sequence: {}".format(len(input)))

    # Fill input.txt
    if write:
        f = open("input.txt", "w+")
        for bit in input:
            f.write(str(bit)+" ")
        f.close()

s = "hello, my name is Arthur"
N0=2
transmitter_ascii(s, N0)
