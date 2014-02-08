import random
carLength = [(3.5, 5.0), (9.0, 12.5)]

class car(object):
    def __init__(self, velocity):
        Probability = random.random()
        if Probability <= 0.8:
            self.mass = random.randint(800, 1500)
        else:
            self.mass = random.randint(9000, 24000)
        self.velocity = velocity
        self.a = 0
        if self.mass > 1500:
            self.length = random.uniform(carLength[1][0], carLength[1][1])
        else:
            self.length = random.uniform(carLength[0][0], carLength[0][1])
