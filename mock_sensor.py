# mock_sensor.py
from data_file import DataFile
import sensor_data
import time

class Sensor:
    def __init__(self):
        self.name = ""
        self.data_file = None
        self.data_list = []
        self.current_index = 0

    def init(self):
        self.data_file = DataFile(self.name)
        print(self.name + " connected.")

    def save(self, data):
        self.data_file.save(data)

    def reader(self, queue):
        print(self.name + " process started.")
        while True:
            data = self.read()
            if data != None:
                queue.put(data)

    def read(self):
        if self.current_index < len(self.data_list):
            data = self.data_list[self.current_index]
            self.current_index += 1
            self.save(data)
            return data
        return None

    def consol_print(self, data):
        print(self.name + ":", data)


class Bmp(Sensor):
    def __init__(self):
        super().__init__()
        self.name = "BMP"
        self.INIT_TIMES = 50
        self.init_altitude = 0
        self.data_list = sensor_data.bmp_data_list
        self.current_index = 0
        self.init()

    def init(self):
        init_buffer = []
        print("Wait BMP Initializing...")
        for i in range(self.INIT_TIMES):
            altitude = self.data_list[i]
            init_buffer.append(altitude)
            if (i + 1) % 10 == 0:
                print(f"{(i + 1) * 2} %")

        self.init_altitude = sum(init_buffer) / self.INIT_TIMES
        print("Done OK")
        super().init()


    def read(self):
        try:
            raw_data = self.data_list[self.current_index]
            self.current_index += 1
            data = raw_data - self.init_altitude
            self.save(data)
            return data
        except IndexError:
            print(self.name, "data is unavailable")
            return None


class Gps(Sensor):
    def __init__(self):
        super().__init__()
        self.name = "GPS"
        self.data_list = sensor_data.gps_data_list
        self.init()

    def init(self):
        super().init()
        return None

    def read(self):
        raw_data = super().read()
        if raw_data is None:
            return None

        lines = str(raw_data).split('$')
        gngll_data = ""
        for line in lines:
            if line.startswith('GNGLL'):
                gngll_data = line
                break

        gngll_data = gngll_data.replace(',,', ',')
        parts = gngll_data.split(',')

        data = [0, 0]
        if len(parts) > 5:
            try:
                latitude = float(parts[1][:2]) + float(parts[1][2:]) / 60
                longitude = float(parts[3][:3]) + float(parts[3][3:]) / 60
                data = [latitude, longitude]  # 위도와 경도 데이터
            except ValueError:
                print("ValueError: Unable to parse latitude/longitude.")

        if data != [0, 0]:
            self.save(data)
            self.consol_print(data)
            return data
        return None


class Ebimu(Sensor):
    def __init__(self):
        super().__init__()
        self.buf = ""
        self.name = "EBIMU"
        self.data_list = sensor_data.ebimu_data_list
        self.current_index = 0
        self.init_r = 0
        self.init_p = 0
        self.init_y = 0
        self.initialized = False
        self.init()

    def init(self):
        init_buffer_r = []
        init_buffer_p = []
        init_buffer_y = []
        self.INIT_TIMES = 50
        print("Wait EBIMU Initializing...")

        for i in range(self.INIT_TIMES):
            data = self.read_data()
            if data is not None:
                init_buffer_r.append(data[0])
                init_buffer_p.append(data[1])
                init_buffer_y.append(data[2])

            if (i + 1) % 10 == 0:
                print(f"{(i + 1) * 2} %")

        self.init_r = sum(init_buffer_r) / self.INIT_TIMES
        self.init_p = sum(init_buffer_p) / self.INIT_TIMES
        self.init_y = sum(init_buffer_y) / self.INIT_TIMES
        print(self.init_r, self.init_p, self.init_y)
        print("Done OK")
        self.initialized = True

        super().init()

    def read_data(self):
        if self.current_index < len(self.data_list):
            raw_data = self.data_list[self.current_index]
            self.current_index += 1

            read_data = raw_data.strip().replace("b'", "").replace("'", "").replace("n", "").strip()

            try:
                read_data_list = [item for item in read_data.split(',') if item]
                if len(read_data_list) == 6:
                    roll, pitch, yaw, x, y, z = map(float, read_data_list)
                    return [roll, pitch, yaw, x, y, z]
                else:
                    print(f"Data Length Error: {read_data_list}")
            except Exception as e:
                print(f"Parsing Error: {e}")
        return None

    def read(self):
        if not self.initialized:
            return None

        data = self.read_data()

        if data is not None:
            self.consol_print(data)
            self.save(data)
            return data
        return None









def run():
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
