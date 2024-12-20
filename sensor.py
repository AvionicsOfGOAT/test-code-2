import keyboard
import time
from data_file import DataFile
from database import Database


class Sensor:
    def __init__(self):
        self.name = ""

    def init(self):
        self.data_file = DataFile(self.name)
        print(self.name + " connected.")

    def reader(self, queue):
        print(self.name + " process started.")
        while True:
            data = self.read()
            if data != None:
                queue.put(data)

    def save(self, data):
        if self.data_file:
            self.data_file.save(data)

    def save(self, data):
        self.data_file.save(data)

    def read(self):
        return

    def consol_print(self, data):
        # print(self.name,":",data)
        pass

class Bmp(Sensor):
    def __init__(self):
        super().__init__()
        self.name = "BMP"
        self.INIT_TIMES = 50
        self.init_altitude = 0
        self.sensor = self.init()

    def init(self):
        import board
        import adafruit_bmp280

        i2c = board.I2C()
        sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        sensor.sea_level_pressure = 1013.25
        init_buffer = []
        print("Wait BMP Initializing...")
        for i in range(self.INIT_TIMES):
            init_buffer.append(sensor.altitude)
            if (i + 1) % 10 == 0:
                print(f"{(i + 1) * 2} %")
        self.init_altitude = sum(init_buffer) / self.INIT_TIMES
        print("Done OK")
        super().init()
        return sensor

    def read(self):
        try:
            data = self.sensor.altitude - self.init_altitude
            self.save(data)
            return data
        except:
            print(self.name, "is unavailable")


class Gps(Sensor):
    def __init__(self):
        super().__init__()
        self.name = "GPS"
        self.sensor = self.init()

    def init(self):
        import serial
        from pyubx2 import UBXReader

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
                data = [latitude, longitude]
            except ValueError:
                pass
        if data:
            self.save(data)
            self.consol_print(data)
            return data
        return None

class Ebimu(Sensor):
    def __init__(self):
        super().__init__()
        self.name = "EBIMU"
        self.sensor = self.init()
        self.init_r = 0
        self.init_p = 0
        self.init_y = 0

    def init(self):
        import serial

        self.sensor = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.001)
        super().init()
        init_buffer_r = []
        init_buffer_p = []
        init_buffer_y = []
        self.INIT_TIMES = 50
        print("Wait EBIMU Initializing...")
        for i in range(self.INIT_TIMES):
            while True:
                data = self.read()
                if data is not None:
                    init_buffer_r.append(data[0])
                    init_buffer_p.append(data[1])
                    init_buffer_y.append(data[2])
                    break

            if (i + 1) % 10 == 0:
                print(f"{(i + 1) * 2} %")
        self.init_r = sum(init_buffer_r) / self.INIT_TIMES
        self.init_p = sum(init_buffer_p) / self.INIT_TIMES
        self.init_y = sum(init_buffer_y) / self.INIT_TIMES
        print(self.init_r, self.init_p, self.init_y)
        print("Done OK")

    def read(self):
        data = 0
        roll = 0
        pitch = 0
        yaw = 0
        x = 0
        y = 0
        z = 0
        try:
            if self.sensor.inWaiting():
                read_data = str(self.sensor.read()).strip()
                self.buf += read_data
                if read_data[3] == "n":
                    self.buf = self.buf.replace("'", "")
                    self.buf = self.buf.replace("b", "")
                try:
                   roll, pitch, yaw, x, y, z = map(float, read_data[1:-4].split(','))
                except Exception as e:
                   self.buf = ""

                data = [roll, pitch, yaw, x, y, z]
                # data = [((roll+360)-self.init_r)%180,((pitch+180)-self.init_p)%90,((yaw+360)-self.init_y)%180,x,y,z]
                self.buf = ""
        except Exception as e:
            print(self.name, "is unavailable:", e)

        if data != 0:
            self.consol_print(data)
            super().save(data)
            return data
        return None





def run_mock_sensor():
    print("Mock sensor mode activated.")
    import mock_sensor
    mock_sensor.run()

if __name__ == "__main__":
    print("Press 'q' within 5 seconds for mock sensor mode, or it will proceed to real sensor mode.")

    start_time = time.time()
    while True:
        if keyboard.is_pressed('q'):
            run_mock_sensor()
            break
        elif time.time() - start_time > 5:
            print("No input detected, proceeding to real sensors.")
            bmp_sensor = Bmp()
            gps_sensor = Gps()
            ebimu_sensor = Ebimu()

            for _ in range(100):
                bmp_data = bmp_sensor.read()
                gps_data = gps_sensor.read()
                ebimu_data = ebimu_sensor.read()

                if bmp_data is not None:
                    print(f"BMP Sensor Data: {bmp_data}")
                if gps_data is not None:
                    print(f"GPS Sensor Data: {gps_data}")
                if ebimu_data is not None:
                    print(f"EBIMU Sensor Data: {ebimu_data}")

                time.sleep(0.5)
            break
