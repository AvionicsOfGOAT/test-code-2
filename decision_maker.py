from data_processor import DataProcessor
class DecisionMaker:
    def __init__(self):
        self.data_processor = DataProcessor()

    # 담당자 : 김예원
    # 입력 : bmp_value
    # 내용 : 고도 기준 하강 판단
    # 출력 : 판단 결과
    def is_altitude_descent(self, bmp_value):
        return False

    # 담당자 : 김예원
    # 입력 : ebimu_value
    # 내용 : 각도 기준 하강 판단
    # 출력 : 판단 결과
    def is_descent_angle(self, ebimu_value):
        return False

    # 담당자 : 김서영
    # 입력 : 없음
    # 내용 : 강제 사출 판단
    # 출력 : 판단 결과
    def is_force_ejection_active(self):
        return False
    
    # 담당자 : 김서영
    # 입력 : gps_value, ebimu_value
    # 내용 : 임계영역 판단
    # 출력 : 판단 결과
    def is_in_critical_area(self, gps_value, ebimu_value):
        position = self.data_processor(gps_value, ebimu_value)
        return False
