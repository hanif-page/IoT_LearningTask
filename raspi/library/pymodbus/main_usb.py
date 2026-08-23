# Great Source
# https://bisaioti.com/modbus-rtu-raspberry-pi-master-sensor-suhu/
# https://www.pymodbus.com/

from pymodbus.client import ModbusSerialClient
import time
from datetime import datetime
from package.sensordata import SensorData # for this absolute import explanation, look at setup.py
from package.database import MySQLData

class PyModbusModule:
    def __init__(self, port: str, baudRate: int, deviceAddress: int):
        self.port = port
        self.baudRate = baudRate
        self.deviceAddress = deviceAddress

    def connectToClient(self) -> ModbusSerialClient:
        client = ModbusSerialClient(port=self.port, timeout=2, baudrate=self.baudRate, bytesize=8, parity="N", stopbits=1)
        if client.connect():
            print(f"[Pymodbus][CONNECTION] Port {self.port} Connected!\n")

            return client
        else:
            print(f"[Pymodbus][CONNECTION] Port {self.port} Failed to Connect!")
            exit(1)

    def closeConnection(self, client: ModbusSerialClient) -> None:
        client.close()

    def changeBaudRate(self, client: ModbusSerialClient, newBaudRate: int) -> bool:
        # Change the Baud Rate
        client.write_register(address=258, value=newBaudRate, device_id=1)
        # --> This will be changed after a while, but not instantly!

        # read the new register
        baudRate = client.read_holding_registers(address=258, count=1, device_id=1)

        if baudRate.registers[0] == newBaudRate:
            print(f"[Pymodbus][SYSTEM] Successfully change baud rate to {baudRate.registers[0]}!")
            return True
        else:
            print(f"[Pymodbus][SYSTEM] Failed to change the baud rate. Baud rate: {baudRate.registers[0]}\n")
            return False
    
    def getMonitoredData(self, client: ModbusSerialClient) -> dict:
        sensor = SensorData(filePathRelativeToDriver="raspi/library/pymodbus/data") # the sensor data class, takes the target file output path as an argument
        MySQLSensorData = MySQLData(databaseName="iot_task", tableName="pymodbus_data") # in terms of efficiency, this shouldn't be called every time!

        strDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"== MONITOR DATA ({strDate}) ==\n")

        # string to be stored in the database
        _date = datetime.now().strftime('%Y-%m-%d')
        _time = datetime.now().strftime('%H-%M-%S')

        # Read Temperature
        temperature = client.read_input_registers(address=1, count=1, device_id=1)
        _temperature = temperature.registers[0] / 10.0
        # print(temperature)
        if not temperature.isError():
            print(f"Temperature (raw data): {temperature.registers[0]}")
            print(f"Temperature (°C): {_temperature}") # assume that the raw data scaled by 10x
        else:
            print(f"Error reading Temperature: {temperature}")

        print() # space between the Temperature and Humidity data

        # Read Humidity
        humidity = client.read_input_registers(address=2, count=1, device_id=1)
        _humidity = humidity.registers[0] / 10.0
        if not humidity.isError():
            print(f"Humidity (raw data): {humidity.registers[0]}")
            print(f"Humidity (%RH): {_humidity}")
        else:
            print(f"Error reading Humidity: {humidity}")

        print() # space

        deviceAddr = client.read_holding_registers(address=257, count=1, device_id=1)
        _deviceAddr = deviceAddr.registers[0]
        print(f"Device Address: {_deviceAddr}")

        baudRate = client.read_holding_registers(address=258, count=1, device_id=1)
        _baudRate = baudRate.registers[0]
        print(f"Baud Rate: {_baudRate}")

        # [STILL WRONG]
        # both of this data still output 0, which I assume for now, it's a false output...?
        temperatureCorrection = client.read_holding_registers(address=259, count=1, device_id=1)
        _temperatureCorrection = temperatureCorrection.registers[0]
        print(f"Temperature Correction (Raw Data): {_temperatureCorrection}")
        humidityCorrection = client.read_holding_registers(address=260, count=1, device_id=1)
        _humidityCorrection = humidityCorrection.registers[0]
        print(f"Humidity Correction (Raw Data): {_humidityCorrection}")

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
                print("[Pymodbus][MySQL] Data successfully added!")

        # store it into 1 big CSV file! (just like a mariadb table)
        sensor.saveDataToBigCSV(libraryname="pymodbus")

        MySQLSensorData.closeConnection()

        # instruction of how to exit from the loop
        # print("\n[Press ctrl+C to Exit from the Loop]")
        # window.ui.stopAndSave_button.clicked.connect(lambda:)

        # time.sleep(2) # Set the 2 second sleep in the GUI!
        print("--------------------------------------------------")

        return newData # returning the data in form of Dictionary!

def connectToClient(port, baudRate):
    client = ModbusSerialClient(port=port, timeout=2, baudrate=baudRate, bytesize=8, parity="N", stopbits=1)
    if client.connect():
        print(f"Port {port} Connected!\n")

        return client
    else:
        print(f"Port {port} Failed to Connect!")
        exit(1)

def runMonitorDisplay(client):
    sensor = SensorData(filePathRelativeToDriver="data") # the sensor data class, takes the target file output path as an argument
    MySQLSensorData = MySQLData(databaseName="iot_task", tableName="pymodbus_data") # in terms of efficiency, this shouldn't be called every time!

    try:

        while True:
            strDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"== MONITOR DATA ({strDate}) ==\n")

            # string to be stored in the database
            _date = datetime.now().strftime('%Y-%m-%d')
            _time = datetime.now().strftime('%H-%M-%S')

            # Read Temperature
            temperature = client.read_input_registers(address=1, count=1, device_id=1)
            _temperature = temperature.registers[0] / 10.0
            # print(temperature)
            if not temperature.isError():
                print(f"Temperature (raw data): {temperature.registers[0]}")
                print(f"Temperature (°C): {_temperature}") # assume that the raw data scaled by 10x
            else:
                print(f"Error reading Temperature: {temperature}")

            print() # space between the Temperature and Humidity data

            # Read Humidity
            humidity = client.read_input_registers(address=2, count=1, device_id=1)
            _humidity = humidity.registers[0] / 10.0
            if not humidity.isError():
                print(f"Humidity (raw data): {humidity.registers[0]}")
                print(f"Humidity (%RH): {_humidity}")
            else:
                print(f"Error reading Humidity: {humidity}")

            print() # space

            deviceAddr = client.read_holding_registers(address=257, count=1, device_id=1)
            _deviceAddr = deviceAddr.registers[0]
            print(f"Device Address: {_deviceAddr}")

            baudRate = client.read_holding_registers(address=258, count=1, device_id=1)
            _baudRate = baudRate.registers[0]
            print(f"Baud Rate: {_baudRate}")

            # [STILL WRONG]
            # both of this data still output 0, which I assume for now, it's a false output...?
            temperatureCorrection = client.read_holding_registers(address=259, count=1, device_id=1)
            _temperatureCorrection = temperatureCorrection.registers[0]
            print(f"Temperature Correction (Raw Data): {_temperatureCorrection}")
            humidityCorrection = client.read_holding_registers(address=260, count=1, device_id=1)
            _humidityCorrection = humidityCorrection.registers[0]
            print(f"Humidity Correction (Raw Data): {_humidityCorrection}")

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
                    print("Data successfully added!")

            # instruction of how to exit from the loop
            print("\n[Press ctrl+C to Exit from the Loop]")

            time.sleep(2) # 2 seconds sleep
            print("--------------------------------------------------")
    except KeyboardInterrupt:
        print("\nData Monitoring Stopped!\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sensor.saveDataToCsv()

        MySQLSensorData.closeConnection()

        runOptionDisplay(client)

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

def main(baudrate):
    client = connectToClient(port=port, baudRate=baudrate)

    print("Welcome to IoT Learning Task System...")
    print("Sensor: XY-MD02\n")

    runOptionDisplay(client)

if __name__ == "__main__":
    baudrate = int(input("Please input initial baudRate: "))

    print()

    main(baudrate)
