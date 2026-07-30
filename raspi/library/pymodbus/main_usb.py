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
from datetime import datetime
# from sshkeyboard import listen_keyboard

def connectToClient(port, baudRate):
    client = ModbusSerialClient(port=port, timeout=2, baudrate=baudRate, bytesize=8, parity="N", stopbits=1)
    if client.connect():
        print(f"Port {port} Connected!\n")

        return client
    else:
        print(f"Port {port} Failed to Connect!")
        exit(1)

def runMonitorDisplay(client):
    try:
        while True:

            strDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"== MONITOR DATA ({strDate}) ==\n")

            # Read Temperature
            temperature = client.read_input_registers(address=1, count=1, device_id=1)
            # print(temperature)
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

            deviceAddr = client.read_holding_registers(address=257, count=1, device_id=1)
            print(f"Device Address: {deviceAddr.registers[0]}")

            baudRate = client.read_holding_registers(address=258, count=1, device_id=1)
            print(f"Baud Rate: {baudRate.registers[0]}")

            # [STILL WRONG]
            # both of this data still output 0, which I assume for now, it's a false output...?
            temperatureCorrection = client.read_holding_registers(address=259, count=1, device_id=1)
            print(f"Temperature Correction (Raw Data): {temperatureCorrection.registers[0]}")
            humidityCorrection = client.read_holding_registers(address=260, count=1, device_id=1)
            print(f"Humidity Correction (Raw Data): {humidityCorrection.registers[0]}")

            # instruction of how to exit from the loop
            print("\n[Press ctrl+C to Exit from the Loop]")

            # 5 second Interval!
            time.sleep(2) # 2 seconds sleep
            print("--------------------------------------------------")
    except KeyboardInterrupt:
        print("\nData Monitoring Stopped!\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        runOptionDisplay(client)

# [STILL WRONG] 
# --> Because the accepted baudrate to connect is still default (9600), even tho the holding register have changed to any other than 9600 (either 14400 or 19200)
def changeBaudRate(client, newBaudRate):
    # Change the Baud Rate
    client.write_register(address=258, value=newBaudRate, device_id=1)
    # --> This will be changed after a while, but not instantly!

    # read the new register
    baudRate = client.read_holding_registers(address=258, count=1, device_id=1)

    if baudRate.registers[0] == newBaudRate:
        print(f"Successfully change baud rate to {baudRate.registers[0]}!")
        print(f"Please !\n")
    else:
        print(f"Failed to change the baud rate. Baud rate: {baudRate.registers[0]}\n")
    runOptionDisplay(client)

def runControlDisplay(client):
    print("== CONTROL ==\n")

    print("Please Pick the New Baud Rate:")
    print("1. 9600\n2. 14400\n3. 19200\n(please only input the number)\n")
    inp = int(input(": "))

    if inp == 1:
        changeBaudRate(client, 9600)
    elif inp == 2:
        changeBaudRate(client, 14400)
    elif inp == 3:
        changeBaudRate(client, 19200)
    else:
        print("Please input the Correct Option!")
        runControlDisplay(client)

def runOptionDisplay(client):
    print("Please Pick One:")
    print("1. Monitor\n2. Control\n3. Exit\n(please only input the number)\n")
    inp = int(input(": "))

    if inp == 1:
        runMonitorDisplay(client)
    elif inp == 2:
        runControlDisplay(client)
    else:
        client.close()
        print("The sensor connection is closed!")

        print("Exiting Program...")
        exit(1)

# CHECK PORT: 
# ls /dev/ttyUSB*
port = "/dev/ttyUSB0"
# baudRate = 9600
# baudRate = 14400

def main(baudrate):
    client = connectToClient(port=port, baudRate=baudrate)

    print("Welcome to IoT Learning Task System...")
    print("Sensor: XY-MD02\n")

    runOptionDisplay(client)

if __name__ == "__main__":
    baudrate = int(input("Please input initial baudRate: "))

    print()

    main(baudrate)
