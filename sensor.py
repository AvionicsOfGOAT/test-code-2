import board
import adafruit_bmp280
import serial
from pyubx2 import UBXReader

from data_file import DataFile
from database import Database

class Sensor:
    db = Database()
    def __init__(self):
        self.name = ""

    def init(self):
        self.data_file = DataFile(self.name)
        print(self.name +" connected.")

    def reader(self, n):
        print(self.name +" process started.")
        while True:
            self.read()

    def save(self, data):
        self.data_file.save(data)
        Sensor.db.save(self.name,data)

    def get_last_from_file(self):
        return

    def read(self):
        return
    
    def consol_print(self, data):
        print(self.name,":",data)

class Bmp(Sensor):
    def __init__(self):
        self.name = "BMP"
        self.INIT_TIMES = 50
        self.init_altitude = 0
        self.sensor = self.init()

    def init(self):
        i2c = board.I2C()  
        sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        sensor.sea_level_pressure = 1013.25
        init_buffer = []
        self.INIT_TIMES = 50
        print("Wait Altitude Initialing...")
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
            data = self.sensor.altitude-self.init_altitude
            self.consol_print(data)
            super().save(data)
        except:
            print(self.name,"is unavailable")
    
    def get_last_from_file(self):
        data = self.data_file.get_last()
        print(data)
        return 0

class Gps(Sensor):
    def __init__(self):
        self.name = "GPS"
        self.sensor = self.init()

    def init(self):
        stream = serial.Serial("/dev/ttyAMA2", baudrate=9600, timeout=50)
        sensor = UBXReader(stream)
        super().init()
        return sensor

    def read(self):
        data = [0,0]
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
                data = [latitude, latitude]
            except ValueError:
                pass
        super().save(data)
        self.consol_print(data)
    
    def get_last_from_file(self):
        data = self.data_file.get_last()
        print(data)
        return [0,0]
    
class Ebimu(Sensor):
    def __init__(self):
        self.buf = "" 
        self.name = "EBIMU"
        self.sensor = self.init()

    def init(self):
        sensor = serial.Serial('/dev/ttyUSB0',115200,timeout=0.001)
        super().init()
        return sensor

    def read(self):
        data = 0
        try:
            if self.sensor.inWaiting():
                read_data = str(self.sensor.read()).strip() 
                self.buf += read_data
                if read_data[3] == "n":
                    self.buf = self.buf.replace("'","")
                    self.buf = self.buf.replace("b","") 

                    try : 
                        roll, pitch, yaw, x, y, z = map(float,self.buf[1:-4].split(','))
                    except Exception as e:
                        self.buf = ""
                    
                    data = [roll,pitch,yaw,x,y,z]
                    self.buf = ""
        except:
            print(self.name,"is unavailable")
        
        if data != 0:
            self.consol_print(data)
            super().save(data)
    
    def get_last_from_file(self):
        data = self.data_file.get_last()
        print(data)
        return [0,0]
