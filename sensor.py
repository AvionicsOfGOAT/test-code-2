# import board
# import adafruit_bmp280
# import RPi.GPIO as GPIO
# import numpy as np
# import serial
# import datetime
# from multiprocessing import Process
# import sys
# import matplotlib.pyplot as plt
# import keyboard
# import os
# import random 
# from pyubx2 import UBXReader

from data_file import DataFile
from database import Database

class Sensor:
    db = Database()
    def __init__(self):
        self.name = "센서이름"

    def init(self):
        self.data_file = DataFile(self.name)
        print(self.name +" connected")

    def save(self, data):
        self.data_file.save(data)
        Sensor.db .save(self.name,data)

    def read(self):
        data = 0
        return data

class Bmp(Sensor):
    def __init__(self):
        self.name = "BMP"
        self.sensor = self.init()

    def init(self):
        # 작성
        super().init()
        return "센서객체"

    def read(self):
        data = 0
        # 작성
        super().save(data)
        return data

class Gps(Sensor):
    def __init__(self):
        self.name = "GPS"
        self.sensor = self.init()

    def init(self):
        # 작성
        super().init()
        return "센서객체"

    def read(self):
        data = 0
        # 작성
        super().save(data)
        return data
    
class Ebimu(Sensor):
    def __init__(self):
        self.name = "EBIMU"
        self.sensor = self.init()

    def init(self):
        # 작성
        super().init()
        return "센서객체"

    def read(self):
        data = 0
        # 작성
        super().save(data)
        return data
    
class Bno(Sensor):
    def __init__(self):
        self.name = "BNO"
        self.sensor = self.init()

    def init(self):
        # 작성
        super().init()
        return "센서객체"

    def read(self):
        data = 0
        # 작성
        super().save(data)
        return data
