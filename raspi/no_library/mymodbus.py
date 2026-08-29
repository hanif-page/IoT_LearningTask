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

        self.socket: serial.Serial | None = None 

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

        if self.socket:
            return True 

        try:
            self.socket = serial.serial_for_url(
                url=self.comm_params.host, # example: "/dev/ttyUSB0"
                timeout=self.comm_params.timeout,
                bytesize=self.comm_params.bytesize,
                stopbits=self.comm_params.stopbits,
                baudrate=self.comm_params.baudrate,
                parity=self.comm_params.parity,
                exclusive=True # it's defined in the pymodbus code...
            )

            self.socket.inter_byte_timeout = self.inter_byte_timeout

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

        return [crc >> 8, crc & 0x0FF] # 0: High Byte, 1: Low Byte

    def read_register(
            self,
            registeraddress: int,
            count: int = 1,
            functioncode: int = 4, # default for input register. The user needs to change the functioncode to 3 if they want to read the holding register!
            no_response_expected: bool = False,
            deviceId: int = 1
    ):

        # print(f"deviceaddress: {hex(registeraddress)}, functioncode: {hex(functioncode)}, ")
        
        # try to read the temperature data
        # self.socket.write(bytearray([0x01, 0x04, 0x00, 0x01, 0x00, 0x01, 0x60, 0x0A]))

        

        # time.sleep(0.1)

        waiting = self.socket.in_waiting
        if waiting > 0:
            data = self.socket.read(waiting)
            print(f"Data: {data}")

            print(f"Drained {len(data)} bytes from buffer!")

        # Clear input buffer
        self.socket.reset_input_buffer()

        # Clear output buffer (discard unsent data)
        self.socket.reset_output_buffer()

        # determine the argument of this function first!
        # return self.execute(
        #     no_response_expected,
        #     ReadRegisterRequest(address=registeraddress, count=count, deviceId=deviceId, functioncode=functioncode)
        # ) 

    def write_register(
            self,
            registeraddress: int,
            value: int,
            functioncode: int = 6
    ):
        # determine the argument of this function first!

        return True

def connectToClient(port):
    client = Client(port=port)
    if client.connect():
        print(f"Port {port} Connected!\n")

        return client
    else:
        print(f"Port {port} Failed to Connect!")
        exit(1)

def main() -> None:
    port = "/dev/ttyUSB0"

    client = connectToClient(port=port)

    client.read_register(
        registeraddress=1,
        count=1,
        functioncode=4
    )

    # TEST THE CRC FIRST
    data = b'Hello, World!'
    crc_16 = client.get_crc_ccitt_16(data)

    print(f"CRC Hi: 0x{crc_16[0]:02X}, CRC Li: 0x{crc_16[1]:02X}")

if __name__ == "__main__":
    main()