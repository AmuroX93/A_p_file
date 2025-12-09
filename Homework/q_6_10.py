class Laser():
    def does(self):
        return 'disintegrate'

class Claw():
    def does(self):
        return 'crush'

class SmartPhone():
    def does(self):
        return 'ring'

class Robot:
    def __init__(self):
        self.laser = Laser()
        self.claw = Claw()
        self.smartphone = SmartPhone()
    
    def does(self):
        return f"I have many attachments: My laser is to {self.laser.does()},\
              my claw is to {self.claw.does()}, and my smartphone is to\
                    {self.smartphone.does()}."
D=Robot()
print(D.does())
