class Car:
    def __init__(self, velocity, position=0, length=0):
        self.velocity = velocity
        self.pos = position
        self.turn_rate = 0.15
        self.length = 0

    def __str__(self):
        return str(self.pos)
    
    def __repr__(self):
        return self.__str__()