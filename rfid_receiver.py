import serial
import time

try:
    with serial.Serial('/dev/ttyACM0', 9600) as ser:
        time.sleep(2)
        while True:
            line = ser.readline()
            line = line.decode()
            string = line.rstrip()
            print(string)
            time.sleep(0.01)
except Exception as e:
    ser.close()
    raise e
