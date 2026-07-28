import minimalmodbus

# Possible Debug Solution
# https://forum.seeedstudio.com/t/minimalmodbus-rs485-shield-for-raspberry-pi/255372
# https://forums.raspberrypi.com/viewtopic.php?t=298220

address = 1
instrument = minimalmodbus.Instrument("/dev/serial0", address)

instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

instrument.clear_buffers_before_each_transaction = True
instrument.close_port_after_each_call = True 
instrument.debug = True 

print(instrument)

print()
print("Requesting Data From Sensor...")

# Read registers
# temperature = instrument.read_register(1, 1, 4, False)
# print(f"Temperature: {temperature}")

# One of the solution, but it does not work!
reg_0 = instrument.read_register(0, 0)
reg_1 = instrument.read_register(1, 0)
print(f"{reg_0} {reg_1}")

instrument.serial.close()

print()
print("Ports Closed!")