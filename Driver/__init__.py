import sys
sys.path.append('../')

from Car import car
from . import FSA
import random

TYPE = ["normal", "badSight", "old", "drunk"]
delta = {
            "normal": (0, 0, 1),
            "badSight": (-30, 0, 2),
            "old": (-30, 1, 2),
            "drunk": (-50, random.randint(2, 4), -1)
        }

class driver(object):
    def __init__(self, _id, road):
        self._id = _id
        self.road = road
        #self.car = car()
        #self.pos = (road.piece[0], 0, -self.car.length, 0)
        self.journey = 0
        Probability = random.random()
        if Probability < 0.7:
            self.type = TYPE[0]
        elif Probability < 0.85:
            self.type = TYPE[1]
        elif Probability < 0.99:
            self.type = TYPE[2]
        else:
            self.type = TYPE[3]
        safeLineError = random.normalvariate(0, 1)
        if abs(safeLineError) > 1.2:
            safeLineError = safeLineError / abs(safeLineError) * 1.2
        self.safeLine = 10 + safeLineError + delta[self.type][2]
        reflectTimeError = random.normalvariate(0, 0.3)
        if abs(reflectTimeError) > 0.8:
            reflectTimeError = reflectTimeError / abs(reflectTimeError) * 0.8
        self.reflectTime = 0.2 + reflectTimeError + delta[self.type][1]
        viewRangeError = random.normalvariate(0, 10)
        if abs(viewRangeError) > 40:
            viewRangeError = viewRangeError / abs(viewRangeError) * 40
        self.viewRange = 380 + viewRangeError + delta[self.type][0]
        tmpHoldV = random.normalvariate(road.Vmin + (road.Vmax - road.Vmin) / 2, 5)
        if tmpHoldV < road.Vmin + (road.Vmax - road.Vmin) / 3:
            tmpHoldV = road.Vmin + (road.Vmax - road.Vmin) / 3
        elif tmpHoldV > road.Vmax:
            tmpHoldV = road.Vmax
        self.holdV = tmpHoldV
        #revisited
        self.car = car(self.holdV)
        self.pos = (road.piece[0], 0, -self.car.length, 0)
        chaseRangeError = random.normalvariate(0, 3)
        if abs(chaseRangeError) > 6:
            chaseRangeError = chaseRangeError / abs(chaseRangeError) * 10
        self.chaseRange = 25 + chaseRangeError
        if road.weather == "wet":
            self.viewRange -= 40
            self.chaseRange -= 10
            self.safeLine += 1
        self.FSA = FSA.driveFSA(self)
        self.crashTime = 0
        self.crash = False
        self.option = "move"
        
        
        