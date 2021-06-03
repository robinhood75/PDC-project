from utf8_generator import get_8bit_unicode

# WARNING: N0 should be multiple of 3
N0=105
NB_CHARS = 80
ENCODING = 'utf-8'

assert N0 % 3 == 0

def generate_message_and_save(NB_CHARS, filename = 'message.txt'):
    s = get_8bit_unicode(NB_CHARS)

    print(f"Generated: {len(s.encode(ENCODING))} bytes")
    print(s.encode(ENCODING))
    
    with open(filename, 'wb') as f:
        for i in s:
            f.write(i.encode(ENCODING))
        f.write('\n'.encode(ENCODING))

def transmitter_utf8_8bits(s, N0, write=True):
    # Since utf-8 on 8 bits, the MSB will always be 0 so it can be omitted.
    # We pad on 7 instead of 8 bits
    str_to_bin_format = ["{0:07b}".format(ord(i)) for i in s]
    
    # Map 0 to -1
    str_to_bin = [2*int(i)-1 for x in str_to_bin_format for i in x]
    
    # Duplicates each element N0 times
    to_be_transmitted = [str(x) for x in str_to_bin for i in range(N0)]

    print(f"Length of the encoded sequence: {len(to_be_transmitted)}")

    with open('input.txt', 'w') as f:
        # Add spaces and print to file
        f.write(' '.join(to_be_transmitted) + ' ')

generate_message_and_save(NB_CHARS)

with open('message.txt', 'rb') as f:
    message = f.read().decode(ENCODING).strip()

transmitter_utf8_8bits(message, N0)