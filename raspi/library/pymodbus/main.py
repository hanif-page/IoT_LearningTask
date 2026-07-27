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

# Great Source
# https://bisaioti.com/modbus-rtu-raspberry-pi-master-sensor-suhu/
# https://www.pymodbus.com/

from pymodbus.client import ModbusSerialClient
import time

print("Hello World")

# CHECK PORT: 
# ls /dev/ttyUSB*
port = "/dev/ttyUSB0"
client = ModbusSerialClient(port=port, timeout=2, baudrate=9600, bytesize=8, parity="N", stopbits=1)

if client.connect():
    print(f"Port {port} Connected!\n")
else:
    print(f"Port {port} Failed to Connect!")
    exit(1)

try:
    while True:
        # Read Temperature
        temperature = client.read_input_registers(address=1, count=1, device_id=1)
        if not temperature.isError():
            print(f"Temperature (raw data): {temperature.registers[0]}")
            print(f"Temperature (°C): {temperature.registers[0] / 10.0}") # assume that the raw data scaled by 10x
        else:
            print(f"Error reading Temperature: {temperature}")

        print() # space between the Temperature and Humidity data

        # Read Humidity
        humidity = client.read_input_registers(address=2, count=1, device_id=1)
        if not humidity.isError():
            print(f"Humidity (raw data): {humidity.registers[0]}")
            print(f"Humidity (%RH): {humidity.registers[0] / 10.0}")
        else:
            print(f"Error reading Humidity: {humidity}")

        print() # space

        # Still and Error! (all these 4 groups of lines)
        # deviceAddr = client.read_holding_registers(address=257, count=1, slave=1)
        # print(f"Device Address: {deviceAddr}")

        # baudRate = client.read_holding_registers(address=1, count=1, device_id=1)
        # print(f"Baud Rate: {baudRate}")

        # temperatureCorrection = client.read_input_registers(address=1, count=1, device_id=1)
        # print(f"Temperature Correction (Raw Data): {temperatureCorrection}")

        # humidityCorrection = client.read_input_registers(address=1, count=1, device_id=1)
        # print(f"Humidity Correction (Raw Data): {humidityCorrection}")

        # 5 second Interval!
        time.sleep(1) # 2 seconds sleep
        print("-------------------------")
except KeyboardInterrupt:
    print("Program Stopped By the User!")
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
    print("The sensor connection is closed!")
