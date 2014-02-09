import random

class driveFSA(object):
    def __init__(self, driver):
        self.driver = driver
        self.nowStatus = {
                             "pos": driver.pos,
                             "carInViewLeft": None,
                             "carInSafeLineLeft": None,
                             "carInViewRight": None,
                             "carInSafeLineRight": None,
                             "carInChaseRight": None,
                             "carInChaseLeft": None,
                             "carBackLeft": None,
                             "carBackRight": None,
                             "lane": "Right",
                             "braking!": 0,
                         }
    
    def judge(self, carInView, carInSafeLine, carBack, carChase,perTime):
        if self.driver.crash:
            self.driver.car.a = -self.driver.road.maxa
            return "crash"
        self.nowStatus["pos"] = self.driver.pos
        self.nowStatus["carInViewLeft"] = carInView[1]
        self.nowStatus["carInViewRight"] = carInView[0]
        self.nowStatus["carInSafeLineLeft"] = carInSafeLine[1]
        self.nowStatus["carInSafeLineRight"] = carInSafeLine[0]
        self.nowStatus["carBackLeft"] = carBack[1]
        self.nowStatus["carBackRight"] = carBack[0]
        self.nowStatus["carInChaseLeft"] = carChase[1]
        self.nowStatus["carInChaseRight"] = carChase[0]
        
        #brakeforp
        Probability = random.random()
        if Probability < (self.driver.density ** 0.5) * 0.5:
            self.driver.car.a = -random.normalvariate(1,self.driver.road.maxa)
            return "braking!"
        
        if self.nowStatus["carInSafeLine" + self.nowStatus["lane"]] != None:
            if self.nowStatus["braking!"] >= self.driver.reflectTime:
                self.driver.car.a = -self.driver.road.maxa
                return "braking!"
            self.nowStatus["braking!"] += perTime
            return "reflecting"
        
        self.nowStatus["braking!"] = 0
        
        Probability = random.random()
        if Probability <= self.driver.trance:
            self.driver.car.a = 0
            return "move"
            
        ThisBefore = None
        ThisAfter = None
        OtherBefore = None
        OtherAfter = None
        This = self.nowStatus["lane"]
        if This == "Right":
            Other = "Left"
        else:
            Other = "Right"
        
        if self.nowStatus["carInSafeLine" + This] != None:
            ThisBefore = self.nowStatus["carInSafeLine" + This]
        elif self.nowStatus["carInChase" + This] != None:
            ThisBefore = self.nowStatus["carInChase" + This]
        elif self.nowStatus["carInView" + This] != None:
            ThisBefore = self.nowStatus["carInView" + This]
        else:
            ThisBefore = None
        
        if self.nowStatus["carInSafeLine" + Other] != None:
            OtherBefore = self.nowStatus["carInSafeLine" + Other]
        elif self.nowStatus["carInChase" + Other] != None:
            OtherBefore = self.nowStatus["carInChase" + Other]
        elif self.nowStatus["carInView" + Other] != None:
            OtherBefore = self.nowStatus["carInView" + Other]
        else:
            OtherBefore = None
            
        ThisAfter = self.nowStatus["carBack" + This]
        OtherAfter = self.nowStatus["carBack" + Other]
        
        nowVelocity = self.driver.car.velocity
        maxVelocity = self.driver.road.Vmax
        
        if ThisBefore == None:
            ThisBeforeDis = maxVelocity
        else:
            ThisBeforeDis = abs(ThisBefore.journey - self.driver.journey)
        
        if ThisAfter == None:
            ThisAfterDis = maxVelocity
        else:
            ThisAfterDis = abs(ThisAfter.journey - self.driver.journey)
        
        if OtherBefore == None:
            OtherBeforeDis = maxVelocity
        else:
            OtherBeforeDis = abs(OtherBefore.journey - self.driver.journey)
        
        if OtherAfter == None:
            OtherAfterDis = maxVelocity
        else:
            OtherAfterDis = abs(OtherAfter.journey - self.driver.journey)
        
        vnext = min(maxVelocity - nowVelocity , ThisBeforeDis - 1)
        self.driver.car.a = min(vnext - nowVelocity , self.driver.road.maxa)
        
        if nowVelocity > ThisBeforeDis and nowVelocity < OtherBeforeDis:
            return "changeLane"
            
        return "move"
