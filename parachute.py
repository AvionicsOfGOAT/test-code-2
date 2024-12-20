import time
#import RPi.GPIO as GPIO
from datetime import datetime

try:
    import RPi.GPIO as GPIO
    RASPBERRY_PI = True
except (ImportError, RuntimeError):
    RASPBERRY_PI = False

if RASPBERRY_PI:
    SERVO_PIN = 18
    RELAY_PIN = 17
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    pwm = GPIO.PWM(SERVO_PIN, 50)
    pwm.start(0)

class Parachute:
    def __init__(self):
        self.is_parachute_deployed = False
        if RASPBERRY_PI:
            GPIO.output(RELAY_PIN, True)

    def set_angle(self, angle):
        if RASPBERRY_PI:
            duty_cycle = (angle / 18) + 2
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.4)
            pwm.ChangeDutyCycle(0)
        else:
            print(f"Simulating setting servo angle to {angle} degrees.")

    def deploy(self):
        print("Parachute deployed")
        self.is_parachute_deployed = True
        if RASPBERRY_PI:
            GPIO.output(RELAY_PIN, False)
            self.set_angle(180)
        else:
            print("Simulating relay activation and servo movement.")

        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("deploy.txt", 'w') as file:
                file.write(current_time)
        except:
            pass

# 테스트 코드
test = Parachute()
test.deploy()
