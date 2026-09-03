import serial
import time

# Good python class object name writing format!
# https://medium.com/better-programming/how-to-use-underscore-properly-in-python-37df5e05ba4c

# Minimal Modbus Source Code
# https://github.com/pyhys/minimalmodbus/blob/master/minimalmodbus.py

class MyModbusClient:
    def __init__(
            self, 
            port: str, # needs to be defined! 
            deviceId: int = 1, 
            baudRate: int = 9600,
            byteSize: int = 8,
            parity: str = "N",
            stopBits: int = 1,
            timeout: int = 2,
            # host = port (in this case)

    ) -> None:
        """Initialize the Modbus Serial Client!"""

        self.socket : serial.Serial 

        self.port = port
        self.deviceId = deviceId 
        self.baudRate = baudRate 
        self.byteSize = byteSize 
        self.parity = parity
        self.stopBits = stopBits 
        self.timeout = timeout

    def connect(self) -> bool:

        """Connect to the modbus serial server!"""
        try:

            self.socket = serial.Serial(
                port=self.port,
                baudrate=self.baudRate,
                bytesize=self.byteSize,
                parity=self.parity,
                stopbits=self.stopBits,
                timeout=self.timeout
            )

        except Exception as e:
            print(f"Error: {e}")
            self.close()

        return self.socket is not None

    def close(self):
        """Close the socket connection!"""

        if self.socket:
            self.socket.close()

        self.socket = None

    # https://www.pyserial.com/docs/modbus-rtu#crc-16-reference
    def modbus_crc16(self, data: bytes):
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc >> 8, crc & 0xFF # 0: High Byte, 1: Low Byte

    def split_hi_li(self, data: int) -> int:

        return data >> 8, data & 0xFF   

    def merge_hi_li(self, hi, li):

        # for splitting, it's
        # hi = data >> 8, li & 0xFF

        # this process basically the reverse process of the top data 
        return (hi << 8) | li

    def read_register(
            self,
            deviceaddress: bytes,
            functioncode: bytes,
            startingaddress : bytes,
            quantity: bytes
    ):
        # WRITING DATA
        startingaddressHi, startingaddressLi = self.split_hi_li(data=startingaddress)
        quantityHi, quantityLi = self.split_hi_li(data=quantity)

        dataPack = bytearray([deviceaddress, functioncode, startingaddressHi, startingaddressLi, quantityHi, quantityLi])

        crc_high, crc_low = self.modbus_crc16(data=dataPack)

        # add the crc_hi and crc_li into the end of the datapack
        # UNORDINARY THING FROM THE DATASHEET: THE CRC POSITION MUST BE POSITIONED WITH LOW FIRST, EVEN THO IN THE DATASHEET, IT'S WRITTEN HIGH FIRST....
        dataPack.extend([crc_low, crc_high])

        # Debugging the Process!
        bytesWritten = self.socket.write(dataPack)

        # MANDATORY, IT SOLVE THE NO DATA PROBLEM!
        time.sleep(0.1)

        # RECEIVING DATA AS A RESPONSE
        numOfIncomingData = self.socket.in_waiting
        if numOfIncomingData > 0:
            # There exist a data
            data = self.socket.read(numOfIncomingData)

            # check the crc
            original_crc = self.merge_hi_li(data[-2], data[-1])
            crc_high, crc_low = self.modbus_crc16(data=data[:-2]) # :-2 means that access all the data other than the last 2 index value!
            generated_crc = self.merge_hi_li(crc_low, crc_high)

            # Why -4 and -3 index? Because the pattern is fixed (the value high and low data is stored literally before the crc_hi part)
            mainData = self.merge_hi_li(data[-4], data[-3])

            if original_crc == generated_crc:
                return mainData # this mainData needs to be divided by 10 first before getting used! (for Temperature and Humidity data)
            else:
                print(f"CRC Error: CRC Does Not Match!")
                return None
        else:
            print("Data Not Exist")

    def write_register(
                self,
                deviceaddress: bytes,
                functioncode: bytes,
                registeraddress : bytes,
                newvalue: int,
    ):
        # WRITING DATA
        registeraddressHi, registeraddressLi = self.split_hi_li(data=registeraddress)
        newvalueHi, newvalueLi = self.split_hi_li(data=newvalue)

        dataPack = bytearray([deviceaddress, functioncode, registeraddressHi, registeraddressLi, newvalueHi, newvalueLi])

        crc_high, crc_low = self.modbus_crc16(data=dataPack)

        # UNORDINARY THING FROM THE DATASHEET: THE CRC POSITION MUST BE POSITIONED WITH LOW FIRST, EVEN THO IN THE DATASHEET, IT'S WRITTEN HIGH FIRST....
        dataPack.extend([crc_low, crc_high])

        # Debugging the Process!
        bytesWritten = self.socket.write(dataPack)

        # MANDATORY, AND FOR WRITE REGISTER, IT TOOK MORE TIME TO ACTUALLY RETURN THE RESULT CORRECTLY!
        time.sleep(0.2)

        # RECEIVING DATA AS A RESPONSE
        numOfIncomingData = self.socket.in_waiting
        if numOfIncomingData > 0:
            # There exist a data
            data = self.socket.read(numOfIncomingData)

            # check the crc
            original_crc = self.merge_hi_li(data[-2], data[-1])
            crc_high, crc_low = self.modbus_crc16(data=data[:-2]) # :-2 means that access all the data other than the last 2 index value!
            generated_crc = self.merge_hi_li(crc_low, crc_high)

            # Why -4 and -3 index? Because the pattern is fixed (the value high and low data is stored literally before the crc_hi part)
            mainData = self.merge_hi_li(data[-4], data[-3])

            if original_crc == generated_crc:
                return True, mainData # this mainData needs to be divided by 10 first before getting used! (for Temperature and Humidity data)
            else:
                print(f"CRC Error: CRC Does Not Match!")
                return False, None
        else:
            print("Data Not Exist")
            return False, None

def connectToClient(port):
    client = MyModbusClient(port=port)
    if client.connect() != None:
        print(f"Port {port} Connected!\n")

        return client
    else:
        print(f"Port {port} Failed to Connect!")
        exit(1)

# testing code
def main() -> None:
    port = "/dev/ttyUSB0"

    client = connectToClient(port=port)

    temperature = client.read_register(
        deviceaddress=1,
        functioncode=4,
        startingaddress=1, # temperature data
        quantity=1 # default value
    )

    humidity = client.read_register(
        deviceaddress=1,
        functioncode=4,
        startingaddress=2, # temperature data
        quantity=1 # default value
    )

    deviceAddress = client.read_register(
        deviceaddress=1,
        functioncode=3,
        startingaddress=257, # temperature data
        quantity=1 # default value
    )

    baudRate = client.read_register(
        deviceaddress=1,
        functioncode=3,
        startingaddress=258, # temperature data
        quantity=1 # default value
    )

    temperatureCorrection = client.read_register(
        deviceaddress=1,
        functioncode=3,
        startingaddress=259, # temperature data
        quantity=1 # default value
    )

    humidityCorrection = client.read_register(
        deviceaddress=1,
        functioncode=3,
        startingaddress=260, # temperature data
        quantity=1 # default value
    )

    print(f"Temperature: {temperature/10}")
    print(f"Humidity: {humidity/10}")
    print(f"Device Address: {deviceAddress}")
    print(f"Baud Rate: {baudRate}")
    print(f"Temperature Correction: {temperatureCorrection}")
    print(f"Humidity Correction: {humidityCorrection}")

    newBaudRateStatus, newBaudRate = client.write_register(
        deviceaddress=1,
        functioncode=6,
        registeraddress=258,
        newvalue=9600
    )
    if newBaudRateStatus:
        print(f"New Baud Rate: {newBaudRate}")

if __name__ == "__main__":
    main()
