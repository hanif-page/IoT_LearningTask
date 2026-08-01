import serial
import sys

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

    def read_register(
            self,
            registeraddress: int,
            number_of_decimals: int,
            functioncode: int = 4 # default for input register. The user needs to change the functioncode to 3 if they want to read the holding register!
    ):
        # determine the argument of this function first!
        return True 

    def write_register(
            self,
            registeraddress: int,
            value: int,
            functioncode: int = 6
    ):
        # determine the argument of this function first!

        return True