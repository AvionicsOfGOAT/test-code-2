import board
import adafruit_bmp280
import RPi.GPIO as GPIO
import numpy as np
import serial
import datetime
from multiprocessing import Process
import sys
import matplotlib.pyplot as plt
import keyboard
import os
import random 
from pyubx2 import UBXReader

from data_file import DataFile
from database import Database

class Sensor:
    db = Database()
    def __init__(self):
        self.name = ""

    def init(self):
        self.data_file = DataFile(self.name)
        print(self.name +" connected")

    def save(self, data):
        self.data_file.save(data)
        Sensor.db.save("bmp",data)

    def read(self):
        data = 0
        return data

class Bmp(Sensor):
    def __init__(self):
        self.name = "BMP"
        self.sensor = self.init()

    def init(self):
        i2c = board.I2C()  
        sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        sensor.sea_level_pressure = 1013.25
        super().init()
        return sensor

    def read(self):
        data = self.sensor.altitude
        data = 0
        super().save(data)
        return data

class Gps(Sensor):
    def __init__(self):
        self.name = "GPS"
        self.sensor = self.init()

    def init(self):
        stream = serial.Serial("/dev/ttyAMA2", baudrate=9600, timeout=50)
        sensor = UBXReader(stream)
        super().init()
        return sensor

    def read(self):
        data = 0
        (raw_data, parsed_data) = self.sensor.read()
        lines = str(raw_data).split('$')
        gngll_data = ""
        for line in lines:
            if line.startswith('GNGLL'):
                gngll_data = line
                break
        gngll_data = gngll_data.replace(',,', ',')
        parts = gngll_data.split(',')

        if len(parts) > 5:  
            try:
                latitude = float(parts[1][:2]) + float(parts[1][2:]) / 60
                longitude = float(parts[3][:3]) + float(parts[3][3:]) / 60
                data = [latitude, latitude]
            except ValueError:
                pass
        super().save(data)
        return data
    
class Ebimu(Sensor):
    def __init__(self):
        self.buf = "" 
        self.name = "EBIMU"
        self.sensor = self.init()

    def init(self):
        sensor = serial.Serial('/dev/ttyUSB0',115200,timeout=0.001)
        super().init()
        return sensor

    def read(self):
        data = 0

        if self.sensor.inWaiting():
            read_data = str(self.sensor.read()).strip() 
            self.buf += read_data
            if read_data[3] == "n":
                self.buf = self.buf.replace("'","")
                self.buf = self.buf.replace("b","") 

                try : 
                    roll, pitch, yaw, x, y, z = map(float,self.buf[1:-4].split(','))
                except Exception as e:
                    self.buf = ""
                
                data = [roll,pitch,yaw,x,y,z]
                self.buf = ""

        if data != 0:
            super().save(data)
        return data
