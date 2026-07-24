# Virtual Environment: venv

# Why? Because the program only runs in the same Raspi. We are not planned to move the program to another OS. So I think that it's better to use just venv and isolating the project dependencies.

# venv guidelines: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

# How to setup .venv (run in the Terminal)
"""
python3 -m venv .venv # .venv is the name of the folder!

source .venv/bin/activate # activate the environment!

which python # check if the python comes from the .venv/bin folder!

# install any dependencies

# set all dependencies to the requirements.txt file
pip freeze > requirements.txt

deactivate # deactivate the environment
"""

from pymodbus.client import ModbusSerialClient

client = ModbusSerialClient(port=, timeout=, baudrate=, bytesize=, parity=, stopbits=)

client.connect()