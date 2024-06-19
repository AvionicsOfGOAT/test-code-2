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

BMP = "BMP"
GPS = "GPS"
EBIMU = "EBIMU"
BNO = "BNO"

class Sensor:
    def __init__(self):
        self.db = Database()
        self.init_bmp()
        self.init_gps()
        self.init_ebimu()
        self.init_bno()

    # 담당자 : 정민준
    # 입력 : 없음
    # 내용 : bmp 센서 연결
    # 출력 : 없음
    def init_bmp(self):
        self.bmp_data_File = DataFile(BMP)
        print(BMP+" connected")

    # 담당자 : 정민준
    # 입력 : 없음
    # 내용 : gps 센서 연결
    # 출력 : 없음
    def init_gps(self):
        self.gps_data_File = DataFile("GPS")
        print(GPS+" connected")

    # 담당자 : 정민준
    # 입력 : 없음
    # 내용 : ebimu 센서 연결
    # 출력 : 없음
    def init_ebimu(self):
        self.ebimu_data_File = DataFile("EBIMU")
        print(EBIMU+" connected")

    # 담당자 : 정민준
    # 입력 : 없음
    # 내용 : bno 센서 연결
    # 출력 : 없음
    def init_bno(self):
        self.bno_data_File = DataFile("BMP")
        print(BNO+" connected")
        
    # 담당자 : 정민준
    # 입력 : 없음
    # 내용 : bmp 센서 값 읽기
    # 출력 : 데이터반환, 형식 : 숫자   
    def read_bmp(self):
        data = 0

        self.bmp_data_File.save(data)
        self.db .save(BMP,data)
        return data
    
    # 담당자 : 정민준
    # 입력 : 없음
    # 내용 : gps 센서 값 읽기
    # 출력 : 데이터반환, 형식 : [위도, 경도]   
    def read_gps(self):
        data = [0,0] # 위도 경도

        self.gps_data_File.save(data)
        self.db .save(GPS,data)
        return data

    # 담당자 : 정민준
    # 입력 : 없음
    # 내용 : ebimu 센서 값 읽기
    # 출력 : 데이터반환, 형식 : [roll, pitch, yaw, x, y, z]
    def read_ebimu(self):
        data = [0,0,0,0,0,0] # roll, pitch, yaw, x, y, z

        self.ebimu_data_File.save(data)
        self.db .save(EBIMU,data)
        return data

    # 담당자 : 정민준
    # 입력 : 없음
    # 내용 : bno 센서 값 읽기
    # 출력 : 데이터반환, 형식 : [roll, pitch, yaw]
    def read_bno(self):
        data = [0,0,0] # roll, pitch, yaw

        self.bno_data_File.save(data)
        self.db .save(BNO,data)
        return data

