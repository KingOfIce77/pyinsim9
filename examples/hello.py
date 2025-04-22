"""Example 1: Initialize InSim and send the message 'Hello, InSim!' to the chat."""

import pyinsim9 as pyinsim

# Initialize the InSim system
insim = pyinsim.insim('127.0.0.1', 29999, Admin='')

# Send message 'Hello, InSim!' to the game
insim.sendm('Hello, InSim!')

# Start pyinsim.
pyinsim.run()
