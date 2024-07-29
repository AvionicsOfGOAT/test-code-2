
import datetime
from database import Database
import numpy as np
import time
import math
from sensor import Bmp

class DecisionMaker:
    db = Database()
    def __init__(self):
        self.db = Database()
        self.init_theta()
        self.datas = []
        self.moving_averages = []
        self.falling_count = 0

        self.WINDOW = 3
        self.FALLING_CONFIRMATION = 10
        self.NO_DEPLOY_ALTITUDE = 1
        self.ESTIMATED_MAX_ALTITUDE = 400
        self.ESTIMATED_MIN_ALTITUDE = -10
        self.theta = 0

    def init_theta(self):
        self.theta = 9.514

    def init_altitude(self):
        bmp = Bmp()
        init_buffer = []
        INIT_TIMES = 50
        print("Wait Altitude Initialing...")
        for i in range(INIT_TIMES):
            init_buffer.append(bmp.read())
            if (i + 1) % 10 == 0:
                print(f"{(i + 1) * 2} %")
        self.init_altitude = sum(init_buffer) / INIT_TIMES
        print("Done OK")

    def is_altitude_descent(self, bmp_value):
        altitude = bmp_value

        if self.ESTIMATED_MIN_ALTITUDE <= altitude <= self.ESTIMATED_MAX_ALTITUDE:
            self.datas.append(altitude)

        mean = np.mean(self.datas[-self.WINDOW:])
        self.moving_averages.append(mean)

        is_valid_falling = False
        if self.moving_averages[-1] > self.NO_DEPLOY_ALTITUDE:
            is_valid_falling = True

        if len(self.moving_averages) > 2 and self.moving_averages[-2] > self.moving_averages[-1]:
            if is_valid_falling:
                self.falling_count += 1
        else:
            self.falling_count = 0

        if self.falling_count >= self.FALLING_CONFIRMATION:
            return True
        return False

    def is_descent_angle(self, ebimu_value):
        r = ebimu_value[0]
        p = ebimu_value[1]
        y = ebimu_value[2]
        x = ebimu_value[3]
        y = ebimu_value[4]
        z = ebimu_value[5]
        if abs(r) + abs(p) >= 80:
            return True
        else:
            return False

    def is_force_ejection_active(self):
        is_force_ejection_active = self.db.get_last("force_ejection")
        print(is_force_ejection_active)
        return False
        
    def is_in_critical_area(self,exact_position):
        x = exact_position[0]
        y = exact_position[1]
        z = exact_position[2]

        length = math.sqrt(x ** 2 + y **2)
        height = length * self.theta

        if height < abs(z):return True
        else:return False
