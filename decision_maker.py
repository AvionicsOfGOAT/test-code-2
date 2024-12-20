class DecisionMaker:
    def __init__(self):

        from database import Database
        self.db = Database()
        self.init_theta()
        self.datas = []
        self.moving_averages = []
        self.falling_count = 0
        self.ma_count = 0

        self.WINDOW = 10
        self.FALLING_CONFIRMATION = 5
        self.NO_DEPLOY_ALTITUDE = 100
        self.ESTIMATED_MAX_ALTITUDE = 400
        self.ESTIMATED_MIN_ALTITUDE = -10
        self.theta = 0

    def init_theta(self):
        self.theta = 9.514

    def is_altitude_descent(self, bmp_value):
        altitude = bmp_value

        if self.ESTIMATED_MIN_ALTITUDE <= altitude <= self.ESTIMATED_MAX_ALTITUDE:
            self.datas.append(altitude)

        import numpy as np  # 필요할 때만 임포트
        mean = np.mean(self.datas[-self.WINDOW:])
        self.moving_averages.append(mean)
        self.ma_count += 1

        is_valid_falling = False
        if self.moving_averages[-1] > self.NO_DEPLOY_ALTITUDE:
            is_valid_falling = True

        if self.ma_count > 2 and (self.moving_averages[-2] - self.moving_averages[-1]) > 0.0:
            if is_valid_falling:
                print("down")
                self.falling_count += 1
        else:
            self.falling_count = 0
            print("up")
        if self.falling_count >= self.FALLING_CONFIRMATION:
            # print("deployed")
            return True
        return False

    #def is_descent_angle(self, ebimu_value):
        return False
        r = ebimu_value[0]
        p = ebimu_value[1]
        if abs(r) + abs(p) >= 80:
            #            print(ebimu_value)
            return True
        else:
            return False

    def is_force_ejection_active(self):
        try:
            from database import Database
            response = self.db.get_last("FE")
            # print(response)
            if response == "1":
                return True
            return False
        except:
            return False

    def is_in_critical_area(self, exact_position):
        x = exact_position[0]
        y = exact_position[1]
        z = exact_position[2]

        import math
        length = math.sqrt(x ** 2 + y ** 2)
        height = length * self.theta

        if height < abs(z):
            return True
        else:
            return False




import time
import keyboard
from mock_decision_maker import MockDecisionMaker
from decision_maker import DecisionMaker
from sensor import Bmp, Gps, Ebimu

def run_mock_sensor():
    print("Mock sensor mode activated.")
    mock_dm = MockDecisionMaker()
    mock_dm.run()

def run_real_sensor():
    print("Real sensor mode activated.")
    bmp_sensor = Bmp()
    gps_sensor = Gps()
    ebimu_sensor = Ebimu()
    real_dm = RealDecisionMaker(bmp_sensor, gps_sensor, ebimu_sensor)
    real_dm.run()

if __name__ == "__main__":
    print("Press 'w' within 5 seconds for mock sensor mode, or it will proceed to real sensor mode.")

    start_time = time.time()
    while True:
        if keyboard.is_pressed('w'):
            run_mock_sensor()
            break
        elif time.time() - start_time > 5:
            print("No input detected, proceeding to real sensor mode.")
            run_real_sensor()
            break

