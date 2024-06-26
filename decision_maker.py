from database import Database

class DecisionMaker:
    def __init__(self):
        self.db = Database()
        return

    def is_altitude_descent(self, bmp_value):
        # 작성
        return False

    def is_descent_angle(self, ebimu_value):
        # 작성
        return False

    def is_force_ejection_active(self):
        is_force_ejection_active = self.db.get_last("force_ejection")
        if is_force_ejection_active == 1:
            return True
        return False
        
    def is_in_critical_area(self):
        is_in_critical_area = self.db.get_last("critical_area")
        if is_in_critical_area == 1:
            return True
        return False
