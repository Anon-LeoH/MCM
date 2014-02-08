import sys
sys.path.append('../')

from Road import Road
from Driver import driver
import random

class test(object):
    def __init__(self):
        self.road = Road()
        self.drivers = []
        self.testTime = random.randint(4000, 12000)
        self.inCar = 0
        self.receiveCar = 0
        self.crashCar = 0
        self.PoissonCoef = random.uniform(0.05, 0.34)
        self.inCarPro = 0
    
    def carIn(self):
        length = len(self.drivers)
        tmpCar = driver(length, self.road)
        #len -> length
        if length != 0 and self.drivers[length-1].journey < tmpCar.safeLine:
            return False
        fl = fr = None
        for i in xrange(0, len(self.drivers), 1):
            if fl != None and fr != None:
                break
            if fl == None and self.drivers[i].FSA.nowStatus["lane"] == "Left":
                fl = self.drivers[i]
            if fr == None and self.drivers[i].FSA.nowStatus["lane"] == "Right":
                fr = self.drivers[i]
        safeList = []
        viewList = []
        if fl != None:
            if abs(fl.journey - tmpCar.journey) <= tmpCar.safeLine:
                safeList.append(fl)
                viewList.append(fl)
            elif abs(fl.journey - tmpCar.journey) <= tmpCar.viewRange:
                safeList.append(None)
                viewList.append(fl)
            else:
                fl = None
        if fl == None:
            safeList.append(fl)
            viewList.append(fl)
        if fr != None:
            if abs(fr.journey - tmpCar.journey) <= tmpCar.safeLine:
                safeList.append(fr)
                viewList.append(fr)
            elif abs(fr.journey - tmpCar.journey) <= tmpCar.viewRange:
                safeList.append(None)
                viewList.append(fr)
            else:
                fr = None
        if fr == None:
            safeList.append(fr)
            viewList.append(fr)
        tmpCar.FSA.driveInRoad(viewList, safeList)
        self.drivers.append(tmpCar)
        self.inCar += 1
    
    def carOut(self, _id):
        for item in self.drivers:
            if item._id == _id:
                self.drivers.remove(item)
                self.receiveCar += 1
                break
    
    def handleCarIn(self):
        Probability = random.random()
        self.inCarPro += Probability
        if self.inCarPro >= 1:
            self.inCarPro -= 1
        if self.inCarPro <= self.PoissonCoef:
            self.carIn()
    
    #self.length -> self.road.length
    def handleCarOut(self):
        for item in self.drivers:
            if item.journey >= self.road.length:
                self.carOut(item._id)
    
    def clearCrash(self):
        for item in self.drivers:
            if item.crash:
                if item.crashTime <= 0:
                    self.drivers.remove(item)
                else:
                    item.crashTime -= 1
    
    def handleMove(self):
        for item in self.drivers:
            deltaS = item.car.velocity * 0.5 + 0.5 ** 3 * item.car.a
            item.journey += deltaS
            tmpPos = item.pos[1] + deltaS
            tmpPiece = item.pos[0]
            if tmpPos >= item.pos[0].length:
                tmpPiece = self.road.piece[self.road.piece.index(item.pos[0]) + 1]
                tmpPos = tmpPos - item.pos[0].length
            item.pos = (tmpPiece, tmpPos, item.pos[2] + deltaS, item.pos[3] + deltaS)
            item.car.velocity += item.car.a
            item.car.a = 0
    
    def handleSwitch(self):
        for item in self.drivers:
            if item.option == "changeLane":
                if item.FSA.nowStatus["lane"] == "Left":
                    item.FSA.nowStatus["lane"] = "Right"
                else:
                    item.FSA.nowStatus["lane"] = "Left"
    
    def handleCrash(self):
        if len(self.drivers) < 2:
            return
        length = len(self.drivers)
        for i in xrange(0, len(self.drivers) - 2):
            if self.drivers[i].pos[3] >= self.drivers[i + 1].pos[2] and self.drivers[i].FSA.nowStatus["lane"] == self.drivers[i + 1].FSA.nowStatus["lane"]:
                self.drivers[i].crash = self.drivers[i+1].crash = True
                crashTime = abs(self.drivers[i].car.velocity - self.drivers[i + 1].car.velocity) * 360
                self.drivers[i].crashTime = max(self.drivers[i].crashTime, crashTime)
                self.drivers[i+1].crashTime = max(self.drivers[i+1].crashTime, crashTime)
                self.crashCar += 1
            elif self.drivers[i].pos[3] >= self.drivers[i + 2].pos[2] and self.drivers[i].FSA.nowStatus["lane"] == self.drivers[i + 2].FSA.nowStatus["lane"]:
                self.drivers[i].crash = self.drivers[i+2].crash = True
                crashTime = abs(self.drivers[i].car.velocity - self.drivers[i + 2].car.velocity) * 360
                self.drivers[i].crashTime = max(self.drivers[i].crashTime, crashTime)
                self.drivers[i+2].crashTime = max(self.drivers[i+2].crashTime, crashTime)
                self.crashCar += 1
        if self.drivers[-2].pos[3] >= self.drivers[-1].pos[2] and self.drivers[-2].FSA.nowStatus["lane"] == self.drivers[-1].FSA.nowStatus["lane"]:
            self.drivers[-2].crash = self.drivers[-1].crash = True
            crashTime = abs(self.drivers[-2].car.velocity - self.drivers[-1].car.velocity) * 360
            self.drivers[-2].crashTime = max(self.drivers[-2].crashTime, crashTime)
            self.drivers[-1].crashTime = max(self.drivers[-1].crashTime, crashTime)
            self.crashCar += 1
    
    def makeDecision(self):
        for item in self.drivers:
            fl = fr = bl = br = None
            for i in xrange(self.drivers.index(item) - 1, -1, -1):
                if bl != None and br != None:
                    break
                if bl == None and self.drivers[i].FSA.nowStatus["lane"] == "Left":
                    bl = self.drivers[i]
                if br == None and self.drivers[i].FSA.nowStatus["lane"] == "Right":
                    br = self.drivers[i]
            for i in xrange(self.drivers.index(item) + 1, len(self.drivers), 1):
                if fl != None and fr != None:
                    break
                if fl == None and self.drivers[i].FSA.nowStatus["lane"] == "Left":
                    fl = self.drivers[i]
                if fr == None and self.drivers[i].FSA.nowStatus["lane"] == "Right":
                    fr = self.drivers[i]
            safeList = []
            chaseList = []
            viewList = []
            backList = []
            if fl != None:
                if abs(fl.journey - item.journey) <= item.safeLine:
                    safeList.append(fl)
                    chaseList.append(fl)
                    viewList.append(fl)
                elif abs(fl.journey - item.journey) <= item.chaseRange:
                    safeList.append(None)
                    chaseList.append(fl)
                    viewList.append(fl)
                elif abs(fl.journey - item.journey) <= item.viewRange:
                    safeList.append(None)
                    chaseList.append(None)
                    viewList.append(fl)
                else:
                    fl = None
            if fl == None:
                safeList.append(fl)
                chaseList.append(fl)
                viewList.append(fl)
            if fr != None:
                if abs(fr.journey - item.journey) <= item.safeLine:
                    safeList.append(fr)
                    chaseList.append(fr)
                    viewList.append(fr)
                elif abs(fr.journey - item.journey) <= item.chaseRange:
                    safeList.append(None)
                    chaseList.append(fr)
                    viewList.append(fr)
                elif abs(fr.journey - item.journey) <= item.viewRange:
                    safeList.append(None)
                    chaseList.append(None)
                    viewList.append(fr)
                else:
                    fr = None
            if fr == None:
                safeList.append(fr)
                chaseList.append(fr)
                viewList.append(fr)
            if bl != None:
                if abs(bl.journey - item.journey) <= item.safeLine:
                    backList.append(bl)
                else:
                    bl = None
            if bl == None:
                backList.append(bl)
            if br != None:
                if abs(br.journey - item.journey) <= item.safeLine:
                    backList.append(br)
                else:
                    br = None
            if br == None:
                backList.append(br)
            item.option = item.FSA.judge(viewList, safeList, backList, chaseList)
    
    def finish(self):
        self.drivers.sort(cmp=lambda x,y:cmp(x.journey, y.journey))
            
            
            
            
            
            
            
            
            
            
            
            
            