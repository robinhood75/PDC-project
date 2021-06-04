# PDC Project
_Author: Julien Biefer & Arthur Mellinger_   
_Date: june 4th 2021_

## How to run

We provided two additionnal scripts:
  * _transmitter.py_: will, in the current configuration, generate a 8 bits utf-8 80 chars sequence and will save it to _message.txt_ file. It will also encode the message so that it can be sent to the client. If you do not want to generate a random message, you can simply comment line 38 of the file and the server will take the message provided in the _message.txt_ file
  * _receiver.py_: will handle the client output and attempt to recover the message and compare the received values with the transmitted one.

Moreover, we modified the client so that input.txt and output.txt are defaults for the _input\_file_ and _output\_file_ arguments respectively. If _srv\_hostname_ and _srv\_port_ are not provided, client will simulate the server response (remove the need to connect through EPFL VPN) using the provided code for the server part.

An example of run would be:

```bash
python3 transmitter.py  # To generate and encode a message
client.py --input_file input.txt --output_file output.txt --srv_hostname iscsrv72.epfl.ch --srv_port 80
python3 receiver.py # To decode the message
```

To make a simple test quickly. First ensure the _test.sh_ script has the correct permission with `chmod u+x test.sh` and then execute:

```bash
./test.sh
```

The script will create a random message, the transmitter will prepare it, the client will connect to the server and the receiver will attempt to decode the message.