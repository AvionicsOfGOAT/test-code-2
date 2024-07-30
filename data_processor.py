import math
import random
import time
import numpy as np

class DataProcessor:
    def __init__(self, alpha):
        self.alpha = alpha
        self.attitude = np.zeros(3)

        # trunk-ignore(bandit/B311)
        self.alpha = random.random()
        self.filter = ComplementaryFilter(alpha)

        self.position = np.zeros(3)
        self.velocity = np.zeros(3)

        # Simulated IMU and GPS data
        self.accel_data = np.random.rand(3)  # Accelerometer data (x, y, z)
        self.gyro_data = np.random.rand(3)   # Gyroscope data (roll, pitch, yaw)
        self.gps_data = np.random.rand(3)    # GPS data (latitude, longitude, altitude)

    d = 0.1

    def update(self, accel, gyro, dt):
        accel_norm = accel / np.linalg.norm(accel)

        pitch_accel = math.atan2(
            -accel_norm[0], math.sqrt(accel_norm[1] ** 2 + accel_norm[2] ** 2)
        )
        roll_accel = math.atan2(accel_norm[1], accel_norm[2])

        self.attitude[0] += gyro[0] * dt  # Roll
        self.attitude[1] += gyro[1] * dt  # Pitch
        self.attitude[2] += gyro[2] * dt  # Yaw

        self.attitude[0] = (1 - self.alpha) * self.attitude[0] + self.alpha * roll_accel
        self.attitude[1] = (1 - self.alpha) * self.attitude[1] + self.alpha * pitch_accel

        return self.attitude
    
    def calculate_exact_position(self, imu_data, gps_data, bmp_data):
        attitude = filter.update(accel_data, gyro_data, self.d)
        self.position = self.gps_data - np.array([0.0, 0.0, 200.0])
        self.velocity += self.accel_data * self.d

        print("Attitude (roll, pitch, yaw):", self.attitude)
        print("Position (latitude, longitude, altitude):", self.position)
        print("Velocity (x, y, z):", self.velocity)
        print("=" * 50)

        # Simulate new data for the next iteration
        accel_data = imu_data[:3]
        gyro_data = imu_data[3:] * 0.1
        gps_data += gps_data+[bmp_data] * 0.1

        time.sleep(self.d)
        return self.position