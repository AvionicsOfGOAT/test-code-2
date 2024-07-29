
import datetime
from database import Database
import numpy as np
import time
import math
from sensor import Bmp

class DataProcessor:
    def __init__(self):
        self.init_altitude()
    def calculate_exact_position(self, imu_data, gps_data):
        return [0,0,0]
        
        

