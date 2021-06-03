## Getting started
Instructions to type in the terminal:

```bash
python3 transmitter.py  # To generate a random message
client.py --input_file input.txt --output_file output.txt --srv_hostname iscsrv72.epfl.ch --srv_port 80
python3 receiver.py # To decode the message
```

To make a simple test quickly. First ensure the _test.sh_ script has the correct permission with `chmod u+x test.sh` and then execute:

```bash
./test.sh
```

The script will create a random message, the transmitter will prepare it, the client will connect to the server and the receiver will attempt to decode the message.