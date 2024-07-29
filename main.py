from decision_maker import DecisionMaker
from sensor import Bmp, Ebimu, Gps
from parachute import Parachute
from data_processor import DataProcessor
import time

def main():
    bmp = Bmp()
    ebimu = Ebimu()
    gps = Gps()

    parachute = Parachute()
    decision_maker = DecisionMaker()
    data_processor = DataProcessor()
    
    while True:
        bmp_value = bmp.read()
        ebimu_value = ebimu.read()
        gps_value = gps.read()
    
        exact_position = data_processor(ebimu_value, gps_value)
        decision_maker.is_in_critical_area(exact_position)

        is_altitude_descent = decision_maker.is_altitude_descent(bmp_value)
        is_descent_angle = decision_maker.is_descent_angle(ebimu_value)
        is_force_ejection_active = decision_maker.is_force_ejection_active()

        parachute_statue = parachute.is_parachute_deployed
        if parachute_statue == False:
            if is_altitude_descent or is_descent_angle or is_force_ejection_active:
                parachute.deploy()

        print(parachute_statue)

if __name__ == "__main__":
    main()
