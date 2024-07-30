from multiprocessing import Process, Queue
from decision_maker import DecisionMaker
from sensor import Bmp, Ebimu, Gps
from parachute import Parachute
from data_processor import DataProcessor

def main():
    bmp = Bmp()
    ebimu = Ebimu()
    gps = Gps()

    bmp_queue = Queue()
    ebimu_queue = Queue()
    gps_queue = Queue()

    bmp_process = Process(target=bmp.reader, args=(bmp_queue,))
    ebimu_process = Process(target=ebimu.reader, args=(ebimu_queue,))
    gps_process = Process(target=gps.reader, args=(gps_queue,))

    bmp_process.daemon = True
    ebimu_process.daemon = True
    gps_process.daemon = True

    bmp_process.start()
    ebimu_process.start()
    gps_process.start()

    parachute = Parachute()
    decision_maker = DecisionMaker()
    data_processor = DataProcessor()
   
    bmp_value = -1
    ebimu_value = -1
    gps_value = -1

    is_altitude_descent = False
    is_descent_angle = False
    is_force_ejection_active = False
    while True:
        if not bmp_queue.empty(): 
            bmp_value = bmp_queue.get()
            print(bmp_value)
        if not ebimu_queue.empty(): 
            ebimu_value = ebimu_queue.get()
            print(ebimu_value)
        if not gps_queue.empty():
            gps_value = gps_queue.get()
            print(gps_value)
        exact_position = [0,0,0]

        decision_maker.is_in_critical_area(exact_position)
        if bmp_value != -1:
            is_altitude_descent = decision_maker.is_altitude_descent(bmp_value)
        if ebimu_value != -1:
            is_descent_angle = decision_maker.is_descent_angle(ebimu_value)
        is_force_ejection_active = decision_maker.is_force_ejection_active()

        parachute_statue = parachute.is_parachute_deployed
        if parachute_statue == False:
            if is_altitude_descent or is_descent_angle or is_force_ejection_active:
                parachute.deploy() 

if __name__ == "__main__":
    main()
