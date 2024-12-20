import time
import numpy as np
from sensor_data import bmp_data_list

class MockDecisionMaker:
    def __init__(self):
        self.datas = []
        self.moving_averages = []
        self.falling_count = 0
        self.ma_count = 0
        self.mock_index = 0

        self.WINDOW = 10
        self.FALLING_CONFIRMATION = 4
        self.NO_DEPLOY_ALTITUDE = 100
        self.ESTIMATED_MAX_ALTITUDE = 400
        self.ESTIMATED_MIN_ALTITUDE = -10
        self.prev_altitude = None

    def get_altitude(self):
        if self.mock_index < len(bmp_data_list):
            altitude = bmp_data_list[self.mock_index]
            print(f" {altitude}")
            self.mock_index += 1
            return altitude
        else:
            print("모의 데이터가 끝났습니다.")
            return None

    def is_altitude_descent(self, bmp_value):
        altitude = bmp_value
        if self.ESTIMATED_MIN_ALTITUDE <= altitude <= self.ESTIMATED_MAX_ALTITUDE:
            self.datas.append(altitude)
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
            print("deployed")
            return True
        return False

    def run(self):
        while True:
            altitude = self.get_altitude()
            if altitude is None:
                print("mock_data_end")
                break
            result = self.is_altitude_descent(altitude)
            if result:
                print("deployed")
                break
            time.sleep(1)

# 실행 예시
if __name__ == "__main__":
    decision_maker = MockDecisionMaker()
    decision_maker.run()
