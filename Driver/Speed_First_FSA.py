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
        Probability = random.random()
        if Probability < 0.5:
            self.nowStatus["lane"] = "Left"
    
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
            self.nowStatus["braking!"] += 1
            return "reflecting"
        
        self.nowStatus["braking!"] = 0
        
        Probability = random.random()
        if Probability <= self.driver.trance:
            self.driver.car.a = 0
            return "move"
        
        self.driver.car.a = min(self.driver.maxV - self.driver.car.velocity, self.driver.road.maxa)

        if self.nowStatus["lane"] == "Right":
                if self.nowStatus["carInChaseRight"] != None:
                    if self.nowStatus["carInSafeLineLeft"] == None and self.nowStatus["carBackLeft"] == None:
                        self.driver.car.a = 0
                        return "changeLane"
        
        if self.nowStatus["lane"] == "Left":
                if self.nowStatus["carInChaseLeft"] != None:
                    if self.nowStatus["carInSafeLineRight"] == None and self.nowStatus["carBackRight"] == None:
                        self.driver.car.a = 0
                        return "changeLane"
            
        return "move"