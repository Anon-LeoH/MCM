import sys
sys.path.append('../')

from Road import Road
from copy import deepcopy as cpy
import random

minTime = 1800
maxTime = 4000
perTime = 0.25

class test(object):
    def __init__(self):
        self.road = Road()
        self.drivers = []
        self.testTime = random.randint(minTime, maxTime)
        self.inCar = 0
        self.receiveCar = 0
        self.crashCar = 0
        self.PoissonCoef = random.uniform(0.05, 0.99)
        self.type = "RightHand"
    
    def handleCarIn(self,tmpCar):
        self.drivers.append(cpy(tmpCar))
        self.inCar += 1
    
    def handleCarOut(self):
        removeList = []
        for item in self.drivers:
            if item.journey >= self.road.length:
                removeList.append(item)
        for item in removeList:
            self.drivers.remove(item)
            self.receiveCar += 1
    
    def clearCrash(self):
        removeList = []
        for item in self.drivers:
            if item.crash:
                if item.crashTime <= 0:
                    removeList.append(item)
                else:
                    item.crashTime -= 1
        for item in removeList:
            self.drivers.remove(item)
            self.crashCar += 1
    
    def handleMove(self):
        widthOfCar = 2.5
        for item in self.drivers:
            deltaS = item.car.velocity * perTime + 0.5 * item.car.a * (perTime ** 0.5)
            #if item.option == "changeLane":
             #   deltaS = (deltaS ** 2 - widthOfCar ** 2) ** 0.5
            item.journey += deltaS
            item.car.velocity += item.car.a * perTime
            if item.car.velocity > item.maxV:
                item.car.velocity = item.maxV
            if item.car.velocity < 0:
                item.car.velocity = 0
            if item.crash:
                continue
            tmpPos = item.pos[1] + deltaS
            tmpPiece = item.pos[0]
            if tmpPos >= item.pos[0].length:
                try:
                    tmpPiece = self.road.piece[self.road.piece.index(item.pos[0]) + 1]
                    tmpPos = tmpPos - item.pos[0].length
                    if tmpPiece.curve:
                        item.viewRange = tmpPiece.viewRange
                        if item.chaseRange > item.viewRange:
                            item.chaseRange = item.viewRange
                        if item.safeLine > item.viewRange:
                            item.safeLine = item.viewRange
                    else:
                        item.viewRange = item.basicViewRange
                        item.chaseRange = item.basicChaseRange
                        item.safeLine = item.basicSafeLine
                except IndexError:
                    print "error id: " + str(item._id)
            item.pos = (tmpPiece, tmpPos, item.journey + deltaS, item.journey + deltaS)    
    
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
        for i in xrange(0, length - 2):
            if self.drivers[i].journey >= self.drivers[i + 1].journey and self.drivers[i].FSA.nowStatus["lane"] == self.drivers[i + 1].FSA.nowStatus["lane"]:
                self.drivers[i].crash = self.drivers[i+1].crash = True                
                crashTime = abs(self.drivers[i].car.velocity - self.drivers[i + 1].car.velocity) * 360
                self.drivers[i].car.velocity = self.drivers[i+1].car.velocity = (self.drivers[i].car.velocity + self.drivers[i+1].car.velocity) / 2
                self.drivers[i].crashTime = max(self.drivers[i].crashTime, crashTime)
                self.drivers[i+1].crashTime = max(self.drivers[i+1].crashTime, crashTime)
            elif self.drivers[i].journey >= self.drivers[i + 2].journey and self.drivers[i].FSA.nowStatus["lane"] == self.drivers[i + 2].FSA.nowStatus["lane"]:
                self.drivers[i].crash = self.drivers[i+2].crash = True                
                crashTime = abs(self.drivers[i].car.velocity - self.drivers[i + 2].car.velocity) * 360
                self.drivers[i].car.velocity = self.drivers[i+2].car.velocity = (self.drivers[i].car.velocity + self.drivers[i+2].car.velocity) / 2
                self.drivers[i].crashTime = max(self.drivers[i].crashTime, crashTime)
                self.drivers[i+2].crashTime = max(self.drivers[i+2].crashTime, crashTime)
        if self.drivers[-2].journey >= self.drivers[-1].journey and self.drivers[-2].FSA.nowStatus["lane"] == self.drivers[-1].FSA.nowStatus["lane"]:
            self.drivers[-2].crash = self.drivers[-1].crash = True            
            crashTime = abs(self.drivers[-2].car.velocity - self.drivers[-1].car.velocity) * 360
            self.drivers[-2].car.velocity = self.drivers[-1].car.velocity = (self.drivers[-2].car.velocity + self.drivers[-1].car.velocity) / 2
            self.drivers[-2].crashTime = max(self.drivers[-2].crashTime, crashTime)
            self.drivers[-1].crashTime = max(self.drivers[-1].crashTime, crashTime)
    
    def makeDecision(self):
        index = 0
        length = len(self.drivers)
        for item in self.drivers:
            fl = fr = bl = br = None
            for i in xrange(index - 1, -1, -1):
                if bl != None and br != None:
                    break
                if (abs(self.drivers[i].journey - item.journey) > item.viewRange):
                    break
                if bl == None and self.drivers[i].FSA.nowStatus["lane"] == "Left":
                    bl = self.drivers[i]
                if br == None and self.drivers[i].FSA.nowStatus["lane"] == "Right":
                    br = self.drivers[i]
            for i in xrange(index + 1, length, 1):
                if fl != None and fr != None:
                    break
                if (abs(self.drivers[i].journey - item.journey) > item.viewRange):
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
            item.option = item.FSA.judge(viewList, safeList, backList, chaseList,perTime)
            index += 1
    
    def finish(self):
        self.drivers.sort(cmp=lambda x,y:cmp(x.journey, y.journey))
    
    #calculateSafe for further use
    def calculateSafe(self):
        preCar = { "Left" : None , "Right" : None }
        oneBig = 20
        oneSmall = 5
        for item in self.drivers:
            lane = item.FSA.nowStatus["lane"]
            if preCar[lane] == None:
                item.safeLine = oneBig
            else:
                delv = item.car.velocity - preCar[lane].car.velocity
                if delv > 0:
                    item.safeLine = delv * 3
                else:
                    item.safeLine = oneSmall
            preCar[lane] = item

    def calculateDensity(self):
        maxDis = self.road.length / 10 / 2
        for item in self.drivers:
            item.density = 0.0
        i = 0
        length = len(self.drivers)
        for j in xrange(0,length,1):
            while self.drivers[j].journey - self.drivers[i].journey > maxDis:
                self.drivers[i].density += j - i - 1
                i += 1
        for j in xrange(i,length,1):
            self.drivers[j].density += length - j - 1
            
        i = length - 1
        for j in xrange(length-1,-1,-1):
            while self.drivers[i].journey - self.drivers[j].journey > maxDis:
                self.drivers[i].density += i - j - 1
                i -= 1
        for j in xrange(i,-1,-1):
            self.drivers[j].density += j
        for item in self.drivers:
            item.density /= maxDis * 2