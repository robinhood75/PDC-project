# ############################################################################
# client.py
# =========
# Author : Sepand KASHANI [sepand.kashani@epfl.ch]
# ############################################################################

"""
Black-box channel simulator. (client)

Instructions
------------
python3 client.py --input_file=[FILENAME] --output_file=[FILENAME] --srv_hostname=[HOSTNAME] --srv_port=[PORT]
"""

import argparse
import pathlib
import socket

import numpy as np

import channel_helper as ch

def parse_args():
    parser = argparse.ArgumentParser(description="COM-302 black-box channel simulator. (client)",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog="To promote efficient communication schemes, transmissions are limited to 1 Mega-sample.")

    parser.add_argument('--input_file', type=str, required=False, default='input.txt',
                        help='.txt file containing (N_sample,) rows of float samples.')
    parser.add_argument('--output_file', type=str, required=False, default='output.txt',
                        help='.txt file to which channel output is saved.')
    parser.add_argument('--srv_hostname', type=str, required=False,
                        help='Server IP address.')
    parser.add_argument('--srv_port', type=int, required=False,
                        help='Server port.')

    args = parser.parse_args()

    args.input_file = pathlib.Path(args.input_file).resolve(strict=True)
    if not (args.input_file.is_file() and
            (args.input_file.suffix == '.txt')):
        raise ValueError('Parameter[input_file] is not a .txt file.')

    args.output_file = pathlib.Path(args.output_file).resolve(strict=False)
    if not (args.output_file.suffix == '.txt'):
        raise ValueError('Parameter[output_file] is not a .txt file.')

    if (args.srv_hostname and not args.srv_port) or (not args.srv_hostname and args.srv_port):
        raise ValueError('Server hostname and port has to be defined.')

    return args

if __name__ == '__main__':
    version_cl = b'dUN'  # Always length-3 alphanumeric

    args = parse_args()
    tx_p_signal = np.loadtxt(args.input_file)

    N_sample = tx_p_signal.size
    if not ((tx_p_signal.shape == (N_sample,)) and
            np.issubdtype(tx_p_signal.dtype, np.floating)):
        raise ValueError('Parameter[input_file] must contain a real-valued sequence.')

    if N_sample > 60000:
        raise ValueError(('Parameter[input_file] contains more than 32,000 samples. '
                          'Design a more efficient communication system.'))

    if args.srv_hostname:
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock_cl:
            sock_cl.connect((args.srv_hostname, args.srv_port))

            tx_header = b'0' + version_cl
            ch.send_msg(sock_cl, tx_header, tx_p_signal)

            rx_header, rx_data = ch.recv_msg(sock_cl)
            if rx_header[:1] == b'0':  # Data
                np.savetxt(args.output_file, rx_data)
            elif rx_header[:1] == b'1':  # Rate limit
                raise Exception(rx_data.tobytes())
            elif rx_header[:1] == b'2':  # Outdated version of client.py
                raise Exception(rx_data.tobytes())
            else:  # Unknown header
                err_msg = f'Unknown header: {rx_header}'
                raise Exception(err_msg)
    else:
        chanInput = np.clip(tx_p_signal,-1,1)
        
        # Erase index
        erasedIndex = np.random.randint(3)
        chanInput[erasedIndex:len(chanInput):3] = 0

        # Add noise
        chanOutput = chanInput + np.sqrt(10)*np.random.randn(len(chanInput))

        # Save file
        np.savetxt(args.output_file, chanOutput)
