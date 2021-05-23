#!/bin/bash
# Enable error reporting
set -e

PY=python3
if [[ `pwd` == *"arthu"* ]]; then
   echo 'Welcome back Arthur!'
   PY=python
fi

# Create random input.txt and encode it
$PY transmitter.py

# Pass signal through channel
$PY client.py

# Decode received signal
$PY receiver.py
