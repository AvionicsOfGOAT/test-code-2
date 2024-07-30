from multiprocessing import Process
from decision_maker import DecisionMaker
from sensor import Bmp, Ebimu, Gps
from parachute import Parachute
from data_processor import DataProcessor

def main():
    bmp = Bmp()
    ebimu = Ebimu()
    gps = Gps()

    bmp_process = Process(target=bmp.reader, args=(1,))
    ebimu_process = Process(target=ebimu.reader, args=(1,))
    gps_process = Process(target=gps.reader, args=(1,))

    bmp_process.start()
    ebimu_process.start()
    gps_process.start()

    parachute = Parachute()
    decision_maker = DecisionMaker()
    data_processor = DataProcessor()

    while True:
        bmp_value = bmp.get_last_from_file()
        ebimu_value = ebimu.get_last_from_file()
        gps_value = gps.get_last_from_file()

        exact_position = data_processor.calculate_exact_position(ebimu_value, gps_value)

        decision_maker.is_in_critical_area(exact_position)
        is_altitude_descent = decision_maker.is_altitude_descent(bmp_value)
        is_descent_angle = decision_maker.is_descent_angle(ebimu_value)
        is_force_ejection_active = decision_maker.is_force_ejection_active()

        parachute_statue = parachute.is_parachute_deployed
        if parachute_statue == False:
            if is_altitude_descent or is_descent_angle or is_force_ejection_active:
                parachute.deploy()

if __name__ == "__main__":
    main()
