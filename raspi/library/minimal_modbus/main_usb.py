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

import minimalmodbus
import time
from datetime import datetime

# Function Code 
# check the xy md 02 function code datasheet!
# https://minimalmodbus.readthedocs.io/en/stable/modbusdetails.html?highlight=read_register

# Instrument function argument detail
# https://github.com/pyhys/minimalmodbus/blob/master/minimalmodbus.py

def connectToInstrument(baudRate, port, deviceAddress):
    try:
        instrument = minimalmodbus.Instrument(port=port, slaveaddress=deviceAddress)

        # default setup
        instrument.serial.bytesize = 8
        instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
        instrument.serial.stopbits = 1
        instrument.serial.timeout = 1

        instrument.serial.baudrate = baudRate

        return instrument
    except Exception as e:
        print(f"Error: {e}")

        print(f"Port {port} Failed to Connect!")

        exit(1)

def runMonitorDisplay(instrument):
    try:
        while True:

            strDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"== MONITOR DATA ({strDate}) ==\n")

            # Read Temperature
            temperature = instrument.read_register(registeraddress=1, number_of_decimals=1, functioncode=4)
            print(f"Temperature (°C): {temperature}")

            print() # space between the Temperature and Humidity data

            # Read Humidity
            humidity = instrument.read_register(registeraddress=2, number_of_decimals=1, functioncode=4)
            print(f"Humidity (%RH): {humidity}")

            print() # space

            # Read Keeping Registers
            deviceAddr = instrument.read_register(registeraddress=257, number_of_decimals=1, functioncode=3)
            print(f"Device Address (raw): {deviceAddr}")
            print(f"Device Address: {int(deviceAddr*10)}\n")

            baudRate = instrument.read_register(registeraddress=258, number_of_decimals=1, functioncode=3)
            print(f"Baud Rate (raw): {baudRate}")
            print(f"Baud Rate: {baudRate*10}\n")

            temperatureCorrection = instrument.read_register(registeraddress=259, number_of_decimals=1, functioncode=3)
            print(f"Temperature Correction (raw): {temperatureCorrection}")
            print(f"Temperature Correction (°C): {temperatureCorrection*10}\n")

            humidityCorrection = instrument.read_register(registeraddress=260, number_of_decimals=1, functioncode=3)
            print(f"Humidity Correction (raw): {humidityCorrection}")
            print(f"Humidity Correction (%RH): {humidityCorrection*10}")

            # instruction of how to exit from the loop
            print("\n[Press ctrl+C to Exit from the Loop]")

            time.sleep(2) # 2 seconds sleep
            print("--------------------------------------------------")
    except KeyboardInterrupt:
        print("\nData Monitoring Stopped!\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        runOptionDisplay(instrument)

def changeBaudRate(instrument, newBaudRate):
    # Change the Baud Rate
    instrument.write_register(registeraddress=258, value=newBaudRate, functioncode=6)
    # --> This will be changed after a while, but not instantly!

    # read the new register
    baudRate = instrument.read_register(registeraddress=258, number_of_decimals=1, functioncode=3) * 10

    if newBaudRate == baudRate:
        print(f"Successfully change baud rate to {baudRate}!")
        print(f"Please !\n")
    else:
        print(f"Failed to change the baud rate. Baud rate: {baudRate}\n")

    runOptionDisplay(instrument)

def runControlDisplay(instrument):
    print("== CONTROL ==\n")

    print("Please Pick the New Baud Rate:")
    print("1. 9600\n2. 14400\n3. 19200\n(please only input the number)\n")
    inp = int(input(": "))

    if inp == 1:
        changeBaudRate(instrument, 9600)
    elif inp == 2:
        changeBaudRate(instrument, 14400)
    elif inp == 3:
        changeBaudRate(instrument, 19200)
    else:
        print("Please input the Correct Option!")
        runControlDisplay(instrument)

def runOptionDisplay(instrument):
    print("Please Pick One:")
    print("1. Monitor\n2. Control\n3. Exit\n(please only input the number)\n")
    inp = int(input(": "))

    if inp == 1:
        runMonitorDisplay(instrument)
    elif inp == 2:
        runControlDisplay(instrument)
    else:
        instrument.serial.close()
        print("The sensor connection is closed!")

        print("Exiting Program...")
        exit(1)


def main(baudrate, port, deviceAddress):
    instrument = connectToInstrument(baudRate=baudrate, port=port, deviceAddress=deviceAddress)

    print("Welcome to IoT Learning Task System...")
    print("Sensor: XY-MD02\n")

    runOptionDisplay(instrument)

if __name__ == "__main__":
    baudrate = int(input("Please input initial baud rate: "))

    print()

    # CHECK PORT:
    # ls /dev/ttyUSB*
    port = "/dev/ttyUSB0"
    deviceAddress = 1

    main(baudrate=baudrate, port=port, deviceAddress=deviceAddress)