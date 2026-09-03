from package.mymodbus import MyModbusClient
import time
from datetime import datetime
from package.sensordata import SensorData # for this absolute import explanation, look at setup.py
from package.database import MySQLData

class MyModbusModule:
    def __init__(self, port: str, baudRate: int, deviceAddress: int):
        self.port = port
        self.baudRate = baudRate
        self.deviceAddress = deviceAddress

    def connectToClient(self) -> MyModbusClient:
        client = MyModbusClient(port=self.port, baudRate=self.baudRate)
        if client.connect():
            print(f"[Mymodbus][CONNECTION] Port {self.port} Connected!\n")

            return client
        else:
            print(f"[Mymodbus][CONNECTION] Port {self.port} Failed to Connect!")
            exit(1)

    def closeConnection(self, client: MyModbusClient) -> None:
        client.close()

    def changeBaudRate(self, client: MyModbusClient, newBaudRate: int) -> bool:
        # Change the Baud Rate
        newBaudRateStatus, newbaudrate = client.write_register(
            deviceaddress=1,
            functioncode=6,
            registeraddress=258,
            newvalue=newBaudRate
        )

        # read the new register
        baudRate = client.read_register(
            deviceaddress=1,
            functioncode=3,
            startingaddress=258, # temperature data
            quantity=1 # default value
        )

        if newBaudRateStatus:
            print(f"[Pymodbus][SYSTEM] Successfully change baud rate to {baudRate}!")
            return True
        else:
            print(f"[Pymodbus][SYSTEM] Failed to change the baud rate. Baud rate: {baudRate}\n")
            return False
    
    def getMonitoredData(self, client: MyModbusClient) -> dict:
        sensor = SensorData(filePathRelativeToDriver="raspi/no_library/data") # the sensor data class, takes the target file output path as an argument
        MySQLSensorData = MySQLData(databaseName="iot_task", tableName="mymodbus_data") # in terms of efficiency, this shouldn't be called every time!

        strDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"== MONITOR DATA ({strDate}) ==\n")

        # string to be stored in the database
        _date = datetime.now().strftime('%Y-%m-%d')
        _time = datetime.now().strftime('%H-%M-%S')

        # Read Temperature
        temperature = client.read_register(
            deviceaddress=1,
            functioncode=4,
            startingaddress=1, # temperature data
            quantity=1 # default value
        )
        _temperature = temperature / 10
        # print(temperature)
        if not (temperature == None):
            print(f"Temperature (raw data): {temperature}")
            print(f"Temperature (°C): {_temperature}") # assume that the raw data scaled by 10x
        else:
            print(f"Error reading Temperature: {temperature}")

        print() # space between the Temperature and Humidity data

        # Read Humidity
        humidity = client.read_register(
            deviceaddress=1,
            functioncode=4,
            startingaddress=2, # temperature data
            quantity=1 # default value
        )
        _humidity = humidity / 10.0
        if not (humidity == None):
            print(f"Humidity (raw data): {humidity}")
            print(f"Humidity (%RH): {_humidity}")
        else:
            print(f"Error reading Humidity: {humidity}")

        print() # space

        deviceAddr = client.read_register(
            deviceaddress=1,
            functioncode=3,
            startingaddress=257, # temperature data
            quantity=1 # default value
        )
        _deviceAddr = deviceAddr
        print(f"Device Address: {_deviceAddr}")

        baudRate = client.read_register(
            deviceaddress=1,
            functioncode=3,
            startingaddress=258, # temperature data
            quantity=1 # default value
        )
        _baudRate = baudRate
        print(f"Baud Rate: {_baudRate}")

        # [STILL WRONG]
        # both of this data still output 0, which I assume for now, it's a false output...?
        temperatureCorrection = client.read_register(
            deviceaddress=1,
            functioncode=3,
            startingaddress=259,
            quantity=1
        )
        _temperatureCorrection = temperatureCorrection
        print(f"Temperature Correction (Raw Data): {_temperatureCorrection}")

        humidityCorrection = client.read_register(
            deviceaddress=1,
            functioncode=3,
            startingaddress=260, # temperature data
            quantity=1 # default value
        )
        _humidityCorrection = humidityCorrection
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
                print("[Mymodbus][MySQL] Data successfully added!")

        # store it into 1 big CSV file! (just like a mariadb table)
        sensor.saveDataToBigCSV(libraryname="mymodbus")

        MySQLSensorData.closeConnection()

        # instruction of how to exit from the loop
        # print("\n[Press ctrl+C to Exit from the Loop]")
        # window.ui.stopAndSave_button.clicked.connect(lambda:)

        # time.sleep(2) # Set the 2 second sleep in the GUI!
        print("--------------------------------------------------")

        return newData # returning the data in form of Dictionary!

def connectToClient(port, baudRate):
    client = MyModbusClient(port=port, baudRate=baudRate) # the other value is set to default value
    if client.connect() != None:
        print(f"Port {port} Connected!\n")

        return client
    else:
        print(f"Port {port} Failed to Connect!")
        exit(1)

def runMonitorDisplay(client):
    sensor = SensorData(filePathRelativeToDriver="data") # the sensor data class, takes the target file output path as an argument
    MySQLSensorData = MySQLData(databaseName="iot_task", tableName="mymodbus_data") # in terms of efficiency, this shouldn't be called every time!

    try:

        while True:
            strDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"== MONITOR DATA ({strDate}) ==\n")

            # string to be stored in the database
            _date = datetime.now().strftime('%Y-%m-%d')
            _time = datetime.now().strftime('%H-%M-%S')

            # Read Temperature
            temperature = client.read_register(
                deviceaddress=1,
                functioncode=4,
                startingaddress=1, # temperature data
                quantity=1 # default value
            )
            _temperature = temperature / 10
            # print(temperature)
            if not (temperature == None):
                print(f"Temperature (raw data): {temperature}")
                print(f"Temperature (°C): {_temperature}") # assume that the raw data scaled by 10x
            else:
                print(f"Error reading Temperature: {temperature}")

            print() # space between the Temperature and Humidity data

            # Read Humidity
            humidity = client.read_register(
                deviceaddress=1,
                functioncode=4,
                startingaddress=2, # temperature data
                quantity=1 # default value
            )
            _humidity = humidity / 10.0
            if not (humidity == None):
                print(f"Humidity (raw data): {humidity}")
                print(f"Humidity (%RH): {_humidity}")
            else:
                print(f"Error reading Humidity: {humidity}")

            print() # space

            deviceAddr = client.read_register(
                deviceaddress=1,
                functioncode=3,
                startingaddress=257, # temperature data
                quantity=1 # default value
            )
            _deviceAddr = deviceAddr
            print(f"Device Address: {_deviceAddr}")

            baudRate = client.read_register(
                deviceaddress=1,
                functioncode=3,
                startingaddress=258, # temperature data
                quantity=1 # default value
            )
            _baudRate = baudRate
            print(f"Baud Rate: {_baudRate}")

            # [STILL WRONG]
            # both of this data still output 0, which I assume for now, it's a false output...?
            temperatureCorrection = client.read_register(
                deviceaddress=1,
                functioncode=3,
                startingaddress=259,
                quantity=1
            )
            _temperatureCorrection = temperatureCorrection
            print(f"Temperature Correction (Raw Data): {_temperatureCorrection}")

            humidityCorrection = client.read_register(
                deviceaddress=1,
                functioncode=3,
                startingaddress=260, # temperature data
                quantity=1 # default value
            )
            _humidityCorrection = humidityCorrection
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
    newBaudRateStatus, newbaudrate = client.write_register(
        deviceaddress=1,
        functioncode=6,
        registeraddress=258,
        newvalue=newBaudRate
    )

    # read the new register
    baudRate = client.read_register(
        deviceaddress=1,
        functioncode=3,
        startingaddress=258, # temperature data
        quantity=1 # default value
    )

    if newBaudRateStatus:
        print(f"Successfully change baud rate to: {newbaudrate}")
    else:
        print(f"Failed to change the baud rate. Current Baud Rate: {newBaudRate}")

    if baudRate == newBaudRate:
        print(f"Successfully change baud rate to: {baudRate}!")
    else:
        print(f"Failed to change the baud rate. Baud rate: {baudRate}\n")
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
