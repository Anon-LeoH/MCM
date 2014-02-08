import sys
sys.path.append('../')

from Car import car
from . import FSA
from . import No_Rule_FSA
import random

TYPE = ["normal", "badSight", "old", "drunk"]
delta = {
            "normal": (0, 0, 1, 0),
            "badSight": (-30, 0, 2, 0),
            "old": (-30, 1, 2, 0),
            "drunk": (-50, random.randint(2, 4), -1, 0.1)
        }

class driver(object):
    def __init__(self, _id, road, type):
        self._id = _id
        self.road = road
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
        safeLineError = random.normalvariate(0, 4)
        if abs(safeLineError) > 8:
            safeLineError = safeLineError / abs(safeLineError) * 8
        self.safeLine = self.basicSafeLine = 20 + safeLineError + delta[self.type][2]
        reflectTimeError = random.normalvariate(0, 0.3)
        if abs(reflectTimeError) > 0.8:
            reflectTimeError = reflectTimeError / abs(reflectTimeError) * 0.8
        self.reflectTime = 0.6 + reflectTimeError + delta[self.type][1]
        viewRangeError = random.normalvariate(0, 10)
        if abs(viewRangeError) > 40:
            viewRangeError = viewRangeError / abs(viewRangeError) * 40
        self.viewRange = self.basicViewRange = 250 + viewRangeError + delta[self.type][0]
        tmpHoldV = random.normalvariate(road.Vmin + (road.Vmax - road.Vmin) / 3, 20)
        if tmpHoldV < road.Vmin:
            tmpHoldV = road.Vmin
        elif tmpHoldV > road.Vmax * 3 / 5:
            tmpHoldV = road.Vmax * 3 / 5
        self.holdV = tmpHoldV
        tmpMaxV = random.normalvariate(road.Vmin + (road.Vmax - road.Vmin) / 2, 5)
        if tmpMaxV < self.holdV:
            tmpMaxV = self.holdV
        elif tmpMaxV > road.Vmax:
            tmpMaxV = road.Vmax
        self.maxV = tmpMaxV
        #revisited
        self.car = car(self.holdV)
        self.pos = (road.piece[0], 0, -self.car.length, 0)
        chaseRangeError = random.normalvariate(0, 5)
        if abs(chaseRangeError) > 10:
            chaseRangeError = chaseRangeError / abs(chaseRangeError) * 10
        self.chaseRange = self.basicChaseRange = 50 + chaseRangeError
        if road.weather == "wet":
            self.viewRange -= 40
            self.chaseRange -= 10
            self.safeLine += 1
        if type == "RightHand":
            self.FSA = FSA.driveFSA(self)
        else:
            self.FSA = No_Rule_FSA.driveFSA(self)
        self.trance = 0.05 + delta[self.type][3]
        self.crashTime = 0
        self.crash = False
        self.option = "move"
        
        
        