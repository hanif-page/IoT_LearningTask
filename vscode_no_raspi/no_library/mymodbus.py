import serial
import sys
import struct
import time

from typing import Generic, Literal, TypeVar, cast
T = TypeVar("T", covariant=False)

import struct

# Good python class object name writing format!
# https://medium.com/better-programming/how-to-use-underscore-properly-in-python-37df5e05ba4c

# Minimal Modbus Source Code
# https://github.com/pyhys/minimalmodbus/blob/master/minimalmodbus.py

class CommunicationParams:

    def __init__(
        self,
        # general value, but still needed to be changed!
        host: str = "localhost", # this equals to the port value such as "/dev/ttyUSB0"
        timeout: int = 0,
        port: int = 0,

        # serial value (needed to be changed!)
        baudrate: int = -1,
        bytesize: int = -1,
        parity: str = "",
        stopbits: int = -1,
        deviceid: int = -1,
        handle_local_echo: bool = False # it just exist in the pymodbus code...
    ):
        self.host = host
        self.timeout = timeout
        self.port = port

        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.deviceid = deviceid
        self.handle_local_echo = handle_local_echo

class ModbusPDU:
    def __init__(
        self,
        deviceId: int = 0,
        transactionId: int = 0,
        address: int = 0,
        count: int = 0,
        bits: list[bool] | None = None,
        registers: list[int] | None = None,
        status: int = 1,
        functioncode: int = 4 # default, for the input register
    ) -> None:
        """Initialize the base data for a modbus request"""

        self.deviceId: int = deviceId
        if deviceId > 255:
            raise f"Invalid ID {deviceId}"

        self.transactionId: int = transactionId
        self.address: int = address
        self.bits: list[bool] = bits or []
        self.registers: list[int] = registers or []
        self.count: int = count or len(self.registers)
        self.status: int = status
        self.exception_code: int = 0
        # self.fut: asyncio.Future
        # self.retries: int = 0

    def verifyCount(self, max_count: int, count: int = -1) -> None:
        """Validate API supplied count"""

        if count == -1:
            count = self.count
        if not 1 <= count <= max_count:
            raise ValueError(f"1 <= count {count} <= {max_count} !")

    def verifyAddress(self, address: int = -1) -> None:
        """Validate API supplied address"""

        if address == -1:
            address = self.address
        if not 0 <= address <= 65535:
            raise ValueError(f"0 <= address {address} <= 65535 !")

        

class ReadRegisterRequest(ModbusPDU):

    """
    functioncode = 3 (holding register)
    functioncode = 4 (input register)
    """

    def encode(self) -> bytes:
        self.verifyAddress()
        self.verifyCount(125)
        return struct.pack(">HH", self.address, self.count)

    def decode(self, data: bytes) -> None:
        self.address, self.count = struct.unpack(">HH", data[:4])


class WriteRegister:

    """
    functioncode = 6 (edit baudrate value)
    """

    def __init__(
        self,

    ) -> None:
        return None

    def datastore_update(self):
        return True

    def setValues(self):
        return True

    def getValues(self):
        return True

class Client:
    def __init__(
            self, 
            port: str, # needs to be defined! 
            deviceId: int = 1, 
            baudRate: int = 9600,
            byteSize: int = 8,
            parity: str = "N",
            stopBits: int = 1,
            timeout: int = 3,
            # host = port (in this case)

    ) -> None:
        """Initialize the Modbus Serial Client!"""

        if "serial" not in sys.modules:
            raise RuntimeError(
                "Serial client requires pyserial"
                'Please install with "pip install pyserial" and try again!'
            )

        self.comm_params = CommunicationParams(
            host=port,
            baudrate=baudRate,
            bytesize=byteSize,
            parity=parity,
            stopbits=stopBits,
            handle_local_echo=False, # in pymodbus, its default is False
            timeout=timeout,
            deviceid=deviceId # current default value!
        )
        self.comm_params.host = port

        self.socket: serial.Serial 

        # _[variable name] --> A temporary variable!
        self._t0 = float(1 + byteSize + stopBits) / baudRate

        # Check every 4 bytes / 2 registers if the reading is ready
        self._recv_interval = self._t0 * 4

        # Set a minimum of 1ms for high baudrates
        self._recv_interval = max(self._recv_interval, 0.001)

        self.inter_byte_timeout: float = 0 # default value

        if baudRate <= 19200:
            self.inter_byte_timeout = 1.5 * self._t0

    def execute(self, no_response_expected: bool, request) -> T:
        _ = no_response_expected, request
        return cast(T, None)

    def connect(self) -> bool:

        """Connect to the modbus serial server!"""

        # if self.socket:
            # return True 

        try:
            # self.socket = serial.serial_for_url(
            #     url=self.comm_params.host, # example: "/dev/ttyUSB0"
            #     timeout=self.comm_params.timeout,
            #     bytesize=self.comm_params.bytesize,
            #     stopbits=self.comm_params.stopbits,
            #     baudrate=self.comm_params.baudrate,
            #     parity=self.comm_params.parity,
            #     exclusive=True # it's defined in the pymodbus code...
            # )

            self.socket = serial.Serial("/dev/ttyUSB0", self.comm_params.baudrate)

            # self.socket.inter_byte_timeout = self.inter_byte_timeout

        except Exception as e:
            print(f"Error: {e}")
            self.close()

        return self.socket is not None

    def close(self):
        """Close the socket connection!"""

        if self.socket:
            self.socket.close()

        self.socket = None

    def get_crc_ccitt_16(self, data):
        # crc 16 references: https://www.askpython.com/python/examples/crc-16-bit-manual-calculation

        crc = 0xFFFF
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1

                crc &= 0xFFFF

        return crc >> 8, crc & 0xFF # 0: High Byte, 1: Low Byte

    def split_hi_li(self, data: int) -> int:

        return data >> 8, data & 0xFF   

    def merge_hi_li(self, hi, li):

        # for splitting, it;s
        # hi = data >> 8, li & 0xFF

        # this process basically the reverse process of the top data 
        return (hi << 8) | li

    def write_with_confirm(self, ser, data, expected=b'OK', timeout=2):
        """Write data and wait for a confirmation response."""
        ser.reset_input_buffer()
        ser.write(data)
        ser.flush()

        response = b''
        deadline = time.time() + timeout
        while time.time() < deadline:
            if ser.in_waiting:
                response += ser.read(ser.in_waiting)
                if expected in response:
                    return True, response
            time.sleep(0.01)
        return False, response

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

        crc_hi, crc_li = self.get_crc_ccitt_16(data=dataPack)

        # add the crc_hi and crc_li into the end of the datapack
        dataPack.extend([crc_hi, crc_li])

        print(f"dataPack: {dataPack}")

        # dataPack ready to be sent by serial.write(dataPack)
        # self.socket.write(dataPack)
        # self.socket.write(b"\x01\x04\x00\x01\x00\x01\xe5\xa7") # hard code trial

        # Debugging the Process!
        ok, resp = self.write_with_confirm(ser=self.socket, data=dataPack)
        print(f"Confirmed: {ok}")

        print(f"Number: {self.socket.in_waiting}")

        # RECEIVING DATA AS A RESPONSE
        numOfIncomingData = self.socket.in_waiting
        if numOfIncomingData > 0:
            print("Data Exist")

        else:
            print("Data Not Exist")
            """
            
            data = self.socket.read(numOfIncomingData)

            print(f"Data: {data}")

            # check the crc
            original_crc = self.merge_hi_li(data[-2], data[-1])
            generated_crc = self.get_crc_ccitt_16(data=original_crc)

            # Why -4 and -3 index? Because the pattern is fixed (the value high and low data is stored literally before the crc_hi part)
            mainData = self.merge_hi_li(data[-4], data[-3])

            return mainData

            if original_crc == generated_crc:
                return mainData / 10 # because originally, the given data is still 10x of the original data
            else:
                print(f"CRC Error: CRC Does Not Match!")
                return None
            """

        """
        numOfIncomingData = serial.in_waiting
        if numOfIncomingData > 0:
            data = serial.read(numOfIncomingData)
        
            print(f"Data: {data}")

            # check the crc
            original_crc = self.merge_hi_li(data[-2], data[-1])
            generated_crc = self.get_crc_ccitt_16(data=original_crc)

            # Why -4 and -3 index? Because the pattern is fixed (the value high and low data is stored literally before the crc_hi part)
            mainData = self.merge_hi_li(data[-4], data[-3])

            if original_crc == generated_crc:
                return data / 10 # because originally, the given data is still 10x of the original data
            else:
                print(f"CRC Error: CRC Does Not Match!")
                return None
        """




    def write_register(
            self,
            registeraddress: int,
            value: int,
            functioncode: int = 6
    ):
        # determine the argument of this function first!

        # DIFFERENT: The return value status, it could be nothing or any Error. So this needs to be plan for the function structure

        return True

def connectToClient(port):
    client = Client(port=port)
    if client.connect():
        print(f"Port {port} Connected!\n")

        return client
    else:
        print(f"Port {port} Failed to Connect!")
        exit(1)

def get_crc_ccitt_16(data):
    # crc 16 references: https://www.askpython.com/python/examples/crc-16-bit-manual-calculation

    crc = 0xFFFF
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1

            crc &= 0xFFFF

    return crc >> 8, crc & 0xFF # 0: High Byte, 1: Low Byte

def split_hi_li(data: int) -> int:

    return data >> 8, data & 0xFF 

def read_register_v2( 
            deviceaddress: int,
            functioncode: int,
            startingaddress: int,
            quantity: int
    ):
        startingaddressHi, startingaddressLi = split_hi_li(data=startingaddress)
        quantityHi, quantityLi = split_hi_li(data=quantity)
        print(f"{deviceaddress:#X}\n{functioncode:#X}")
        print(f"{startingaddressHi:#X} + {startingaddressLi:#X}\n{quantityHi:#X} + {quantityLi:#X}")

        dataPack = bytearray([deviceaddress, functioncode, startingaddressHi, startingaddressLi, quantityHi, quantityLi])

        crc_hi, crc_li = get_crc_ccitt_16(data=dataPack)

        dataPack.extend([crc_hi, crc_li])

        print(dataPack)

        # accessing the last byte, which is the crc_li
        print(f"{dataPack[7]:#X}")

        # later, to get the dataPack size, use serial.in_waiting property

def main() -> None:
    port = "/dev/ttyUSB0"

    client = connectToClient(port=port)

    # print(client.socket.wi)

    temperature = client.read_register(
        deviceaddress=0x01,
        functioncode=0x04,
        startingaddress=0x01, # temperature data
        quantity=0x01 # default value
    )

    print(f"Temperature: {temperature}")

    # Good Source
    # https://www.wevolver.com/article/modbus-rtu-a-comprehensive-guide-to-understanding-and-implementing-the-protocol

    # TEST THE CRC FIRST
    # data = b'Hello, World!'
    # crc_16 = client.get_crc_ccitt_16(data)

    # print(f"CRC Hi: 0x{crc_16[0]:02X}, CRC Li: 0x{crc_16[1]:02X}")

# NEXT: TRY TO RUN IT IN THE RASPI!
if __name__ == "__main__":
    main()
