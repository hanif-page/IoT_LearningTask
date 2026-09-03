import serial
import time

def echo_test(port, baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        time.sleep(1)  # wait for device init

        ser.write(b'AT\r\n')
        response = ser.readline()
        print(f"Sent: AT")
        print(f"Received: {response.decode('utf-8').strip()}")

        ser.close()

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except FileNotFoundError:
        print("Port not found. Check device connection.")
    except PermissionError:
        print("Permission denied. Add yourself to the dialout group (Linux).")

if __name__ == "__main__":
    echo_test('/dev/ttyUSB0')