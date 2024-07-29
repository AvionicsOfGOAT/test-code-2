class Parachute:
    def __init__(self):
        self.is_parachute_deployed = False

    def deploy(self):
        self.is_parachute_deployed = True
        print("Parachute deployed")
