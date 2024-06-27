import self
import datetime
from database import Database
import numpy as np
import time
from sensor import Bmp

class DecisionMaker:
    db = Database()
    datas = []
    moving_averages = []
    falling_count = 0

    WINDOW = 3
    FALLING_CONFIRMATION = 10
    NO_DEPLOY_ALTITUDE = 1
    ESTIMATED_MAX_ALTITUDE = 400
    ESTIMATED_MIN_ALTITUDE = -10

    def __init__(self):
        self.init_altitude()

    def init_altitude(self):
        bmp = Bmp()
        init_buffer = []
        INIT_TIMES = 50
        print("Wait Altitude Initialing...")
        for i in range(INIT_TIMES):
            init_buffer.append(bmp.read())
            if (i + 1) % 10 == 0:
                print(f"{(i + 1) * 2} %")
        DecisionMaker.init_altitude = sum(init_buffer) / INIT_TIMES
        print("Done OK")

    def is_altitude_descent(self, bmp_value):
        altitude = bmp_value - DecisionMaker.init_altitude

        if DecisionMaker.ESTIMATED_MIN_ALTITUDE <= altitude <= DecisionMaker.ESTIMATED_MAX_ALTITUDE:
            DecisionMaker.datas.append(altitude)

        mean = np.mean(DecisionMaker.datas[-DecisionMaker.WINDOW:])
        DecisionMaker.moving_averages.append(mean)

        is_valid_falling = False
        if DecisionMaker.moving_averages[-1] > DecisionMaker.NO_DEPLOY_ALTITUDE:
            is_valid_falling = True

        if len(DecisionMaker.moving_averages) > 2 and DecisionMaker.moving_averages[-2] > DecisionMaker.moving_averages[-1]:
            if is_valid_falling:
                DecisionMaker.falling_count += 1
        else:
            DecisionMaker.falling_count = 0

        if DecisionMaker.falling_count >= DecisionMaker.FALLING_CONFIRMATION:
            return True
        return False

    def is_descent_angle(self, ebimu_value):
        r, p, y, x, y, z = ebimu_value
        if abs(r) + abs(p) >= 80:
            return True
        else:
            return False




    def is_force_ejection_active(self):
        is_force_ejection_active = self.db.get_last("force_ejection")
        if is_force_ejection_active == 1:
            return True
        return False
        
    def is_in_critical_area(self):
        is_in_critical_area = self.db.get_last("critical_area")
        if is_in_critical_area == 1:
            return True
        return False

