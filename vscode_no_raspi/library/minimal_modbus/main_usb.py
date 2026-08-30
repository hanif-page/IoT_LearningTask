import minimalmodbus
import time
from datetime import datetime
from package.sensordata import SensorData # for this absolute import explanation, look at setup.py
from package.database import MySQLData

# Regarding the sudo problem in running "python3 main_usb.py"
# STEPS:
# sudo usermod -a -G dialout $USER # setting up the super user
# newgrp dialout # refresh directly!

# Function Code 
# check the xy md 02 function code datasheet!
# https://minimalmodbus.readthedocs.io/en/stable/modbusdetails.html?highlight=read_register

# Instrument function argument detail
# https://github.com/pyhys/minimalmodbus/blob/master/minimalmodbus.py

# NOTE: in this code, client = instrument (the correct term here is instrument, but I just simplify it so that it match with the term used in the Pymodbus program!)
class MinimalModbusModule:
    def __init__(self, port: str, baudRate: int, deviceAddress: int):
        self.port = port
        self.baudRate = baudRate
        self.deviceAddress = deviceAddress

    def connectToClient(self) -> minimalmodbus.Instrument:
        try:
            client = minimalmodbus.Instrument(port=self.port, slaveaddress=self.deviceAddress)

            # default setup
            client.serial.bytesize = 8
            client.serial.parity = minimalmodbus.serial.PARITY_NONE
            client.serial.stopbits = 1
            client.serial.timeout = 1

            client.serial.baudrate = self.baudRate

            print(f"[Minimalmodbus][CONNECTION] Port {self.port} Connected!\n")

            return client
        except Exception as e:
            print(f"[Minimalmodbus][CONNECTION] Port {self.port} Failed to Connect!")
            print(f"[Minimalmodbus] Error: {e}")

            exit(1)

    def closeConnection(self, client: minimalmodbus.Instrument) -> None:
        client.serial.close()

    def changeBaudRate(self, client: minimalmodbus.Instrument, newBaudRate: int) -> bool:
        # Change the Baud Rate
        client.write_register(registeraddress=258, value=newBaudRate, functioncode=6)
        # --> This will be changed after a while, but not instantly!

        # read the new register
        baudRate = client.read_register(registeraddress=258, number_of_decimals=1, functioncode=3) * 10

        if newBaudRate == baudRate:
            print(f"[Minimalmodbus][SYSTEM] Successfully change baud rate to {baudRate}!")
            return True
        else:
            print(f"[Minimalmodbus][SYSTEM] Failed to change the baud rate. Baud rate: {baudRate}\n")
            return False

    def getMonitoredData(self, client: minimalmodbus.Instrument) -> dict:
        sensor = SensorData(filePathRelativeToDriver="raspi/library/minimal_modbus/data") # the sensor data class, takes the target file output path as an argument
        MySQLSensorData = MySQLData(databaseName="iot_task", tableName="minimalmodbus_data") # in terms of efficiency, this shouldn't be called every time!

        strDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"== MONITOR DATA ({strDate}) ==\n")

            # string to be stored in the database
        _date = datetime.now().strftime('%Y-%m-%d')
        _time = datetime.now().strftime('%H-%M-%S')

        # Read Temperature
        temperature = client.read_register(registeraddress=1, number_of_decimals=1, functioncode=4)
        _temperature = temperature
        print(f"Temperature (°C): {_temperature}")

        print() # space between the Temperature and Humidity data

        # Read Humidity
        humidity = client.read_register(registeraddress=2, number_of_decimals=1, functioncode=4)
        _humidity = humidity
        print(f"Humidity (%RH): {_humidity}")

        print() # space

        # Read Keeping Registers
        deviceAddr = client.read_register(registeraddress=257, number_of_decimals=1, functioncode=3)
        _deviceAddr = int(deviceAddr*10)
        print(f"Device Address (raw): {deviceAddr}")
        print(f"Device Address: {_deviceAddr}\n")

        baudRate = client.read_register(registeraddress=258, number_of_decimals=1, functioncode=3)
        _baudRate = baudRate*10
        print(f"Baud Rate (raw): {baudRate}")
        print(f"Baud Rate: {_baudRate}\n")

        temperatureCorrection = client.read_register(registeraddress=259, number_of_decimals=1, functioncode=3)
        _temperatureCorrection = temperatureCorrection*10
        print(f"Temperature Correction (raw): {temperatureCorrection}")
        print(f"Temperature Correction (°C): {_temperatureCorrection}\n")

        humidityCorrection = client.read_register(registeraddress=260, number_of_decimals=1, functioncode=3)
        _humidityCorrection = humidityCorrection*10
        print(f"Humidity Correction (raw): {humidityCorrection}")
        print(f"Humidity Correction (%RH): {_humidityCorrection}")

        print()

        # create the sensor data from the SensorData class
        newData = sensor.createData(
            date=_date, 
            time=_time,
            temperature=_temperature,
            humidity=_humidity,
            deviceAddress=_deviceAddr,
            baudRate=_baudRate,
            temperatureCorrection=_temperatureCorrection,
            humidityCorrection=_humidityCorrection
        )
        sensor.addData(newData)

        # MySQL Data Saving process
        if MySQLSensorData.connectToMySQL():
            if MySQLSensorData.addData(
                date=_date,
                time=_time,
                temperature=_temperature,
                humidity=_humidity,
                deviceAddress=_deviceAddr,
                baudRate=_baudRate,
                temperatureCorrection=_temperatureCorrection,
                humidityCorrection=_humidityCorrection
            ):
                print("[Minimalmodbus][MySQL] Data successfully added!")

        # store it into 1 big CSV file! (just like a mariadb table)
        sensor.saveDataToBigCSV(libraryname="minimalmodbus")

        MySQLSensorData.closeConnection()
        print("--------------------------------------------------")

        return newData # returning the data in form of Dictionary

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
    # sensor = SensorData(filePathRelativeToDriver="data") # the sensor data class, takes the target file output path as an argument
    # MySQLSensorData = MySQLData(databaseName="iot_task", tableName="minimalmodbus_data") # in terms of efficiency, this shouldn't be called every time!

    try:
        while True:

            strDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"== MONITOR DATA ({strDate}) ==\n")

             # string to be stored in the database
            _date = datetime.now().strftime('%Y-%m-%d')
            _time = datetime.now().strftime('%H-%M-%S')

            # Read Temperature
            temperature = instrument.read_register(registeraddress=1, number_of_decimals=1, functioncode=4)
            _temperature = temperature
            print(f"Temperature (°C): {_temperature}")

            print() # space between the Temperature and Humidity data

            # Read Humidity
            humidity = instrument.read_register(registeraddress=2, number_of_decimals=1, functioncode=4)
            _humidity = humidity
            print(f"Humidity (%RH): {_humidity}")

            print() # space

            # Read Keeping Registers
            deviceAddr = instrument.read_register(registeraddress=257, number_of_decimals=1, functioncode=3)
            _deviceAddr = int(deviceAddr*10)
            print(f"Device Address (raw): {deviceAddr}")
            print(f"Device Address: {_deviceAddr}\n")

            baudRate = instrument.read_register(registeraddress=258, number_of_decimals=1, functioncode=3)
            _baudRate = baudRate*10
            print(f"Baud Rate (raw): {baudRate}")
            print(f"Baud Rate: {_baudRate}\n")

            temperatureCorrection = instrument.read_register(registeraddress=259, number_of_decimals=1, functioncode=3)
            _temperatureCorrection = temperatureCorrection*10
            print(f"Temperature Correction (raw): {temperatureCorrection}")
            print(f"Temperature Correction (°C): {_temperatureCorrection}\n")

            humidityCorrection = instrument.read_register(registeraddress=260, number_of_decimals=1, functioncode=3)
            _humidityCorrection = humidityCorrection*10
            print(f"Humidity Correction (raw): {humidityCorrection}")
            print(f"Humidity Correction (%RH): {_humidityCorrection}")

            # create the sensor data from the SensorData class
            # newData = sensor.createData(
            #     date=_date, 
            #     time=_time,
            #     temperature=_temperature,
            #     humidity=_humidity,
            #     deviceAddress=_deviceAddr,
            #     baudRate=_baudRate,
            #     temperatureCorrection=_temperatureCorrection,
            #     humidityCorrection=_humidityCorrection
            # )
            # sensor.addData(newData)

            # MySQL Data Saving process
            # if MySQLSensorData.connectToMySQL():
            #     if MySQLSensorData.addData(
            #         date=_date,
            #         time=_time,
            #         temperature=_temperature,
            #         humidity=_humidity,
            #         deviceAddress=_deviceAddr,
            #         baudRate=_baudRate,
            #         temperatureCorrection=_temperatureCorrection,
            #         humidityCorrection=_humidityCorrection
            #     ):
            #         print("Data successfully added!")

            # instruction of how to exit from the loop
            print("\n[Press ctrl+C to Exit from the Loop]")

            time.sleep(2) # 2 seconds sleep
            print("--------------------------------------------------")
    except KeyboardInterrupt:
        print("\nData Monitoring Stopped!\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # sensor.saveDataToCsv()

        # MySQLSensorData.closeConnection()

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