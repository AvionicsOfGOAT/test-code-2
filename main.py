from decision_maker import DecisionMaker
from sensor import Sensor
from parachute import Parachute
import time

def main():
    sensor = Sensor()
    parachute = Parachute()
    decision_maker = DecisionMaker()
    
    while True:
        bmp_value = sensor.read_bmp()
        ebimu_value = sensor.read_ebimu()
        gps_value = sensor.read_gps()
        bno_value = sensor.read_bno()

        is_altitude_descent = decision_maker.is_altitude_descent(bmp_value)
        is_descent_angle = decision_maker.is_descent_angle(ebimu_value)
        is_in_critical_area = decision_maker.is_in_critical_area(gps_value, ebimu_value)
        is_force_ejection_active = decision_maker.is_force_ejection_active()

        parachute_statue = parachute.is_parachute_deployed

        if parachute_statue == False:
            if is_altitude_descent or is_descent_angle or is_in_critical_area or is_force_ejection_active:
                parachute.deploy()

        print(parachute_statue)
        time.sleep(0.02)

if __name__ == "__main__":
    main()
