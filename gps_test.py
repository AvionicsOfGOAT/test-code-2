import serial
from pyubx2 import UBXReader

stream = serial.Serial("/dev/ttyAMA2", baudrate=9600, timeout=50)
ubr = UBXReader(stream)
file =  open("gps_data.txt", "a")
while True:
    (raw_data, parsed_data) = ubr.read()
    print(raw_data)
