class DecisionMaker:
    def __init__(self):
        pass

    def is_altitude_descent(self, bmp_value):
        return False
    
    def is_descent_angle(self, ebimu_value):
        return False
    
    def is_force_ejection_active(self):
        return False
    
    def is_in_critical_area(self, gps_value, ebimu_value):
        return False

