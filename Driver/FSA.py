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
                             "onLaneDistance": driver.viewRange + 1,
                             "braking!": 0,
                         }
    
    def driveInRoad(self, carInView, carInSafeLine):
        self.nowStatus["carInViewLeft"] = carInView[1]
        self.nowStatus["carInViewRight"] = carInView[0]
        self.nowStatus["carInSafeLineLeft"] = carInSafeLine[1]
        self.nowStatus["carInSafeLineRight"] = carInSafeLine[0]
        if self.nowStatus["carInSafeLineRight"] == None:
            self.nowStatus["lane"] = "Right"
            if self.nowStatus["carInViewRight"] != None:
                self.nowStatus["onLaneDistance"] = self.nowStatus["carInViewRight"].journey
        elif self.nowStatus["carInSafeLineRight"].velocity >= self.driver.holdV:
            self.nowStatus["lane"] = "Right"
            self.nowStatus["onLaneDistance"] = self.nowStatus["carInSafeLineRight"].journey
        elif self.nowStatus["carInSafeLineLeft"] == None:
            self.nowStatus["lane"] = "Left"
            if self.nowStatus["carInViewLeft"] != None:
                self.nowStatus["onLaneDistance"] = self.nowStatus["carInViewLeft"].journey
        elif self.nowStatus["carInSafeLineLeft"].velocity >= self.driver.holdV:
            self.nowStatus["lane"] = "Left"
            self.nowStatus["onLaneDistance"] = self.nowStatus["carInSafeLineLeft"].journey
        else:
            self.driver.car.velocity = self.nowStatus["carInSafeLineRight"].velocity
            self.nowStatus["lane"] = "Right"
            self.nowStatus["onLaneDistance"] = self.nowStatus["carInSafeLineRight"].journey
    
    def judge(self, carInView, carInSafeLine, carBack, carChase):
        self.nowStatus["pos"] = driver.pos
        self.nowStatus["carInViewLeft"] = carInView[1]
        self.nowStatus["carInViewRight"] = carInView[0]
        self.nowStatus["carInSafeLineLeft"] = carInSafeLine[1]
        self.nowStatus["carInSafeLineRight"] = carInSafeLine[0]
        self.nowStatus["carBackLeft"] = carBack[1]
        self.nowStatus["carBackRight"] = carBack[0]
        self.nowStatus["carInChaseLeft"] = carChase[1]
        self.nowStatus["carInChaseRight"] = carChase[0]
        
        if self.nowStatus["braking!"] >= self.driver.reflectTime:
            self.driver.car.a = self.nowStatus["pos"][0].maxa
            return "braking!"
        
        if self.nowStatus["carInSafeLine" + self.nowStatus["lane"]] != None:
            self.nowStatus["braking!"] += 2
            if self.nowStatus["braking!"] >= self.driver.reflectTime:
                self.driver.car.a = self.nowStatus["pos"][0].maxa 
                return "braking!"
            return "reflecting"
        
        self.nowStatus["braking!"] = 0
        
        if self.driver.car.velocity < self.driver.holdV:
            self.driver.car.a = min(self.driver.holdV - self.driver.car.velocity, self.nowStatus["pos"][0].maxa)
        
        if not self.nowStatus["pos"][0].curve:
            if self.nowStatus["carInView" + self.nowStatus["lane"]] == None:
                self.driver.car.a = min(self.nowStatus["pos"][0].Vmax - self.driver.car.velocity, self.nowStatus["pos"][0].maxa)
            elif self.driver.car.velocity > self.driver.holdV:
                self.driver.car.a = -min(self.driver.car.velocity - self.driver.holdV, self.nowStatus["pos"][0].maxa)
            else:
                self.driver.car.a = min(self.driver.holdV - self.driver.car.velocity, self.nowStatus["pos"][0].maxa)
            if self.nowStatus["lane"] == "Right":
                if self.nowStatus["carInChaseRight"] != None:
                    if self.nowStatus["carInSafeLineLeft"] == None and self.nowStatus["carBackLeft"] == None:
                        self.driver.car.a = 0
                        return "changeLane"
                    else:
                        self.driver.car.a = -min(self.driver.car.velocity - self.nowStatus["carInChaseRight" + self.nowStatus["lane"]].velocity, self.nowStatus["pos"][0].maxa)
            else:
                if self.nowStatus["carInChaseRight"] == None and self.nowStatus["carBackRight"] == None:
                    self.driver.car.a = 0
                    return "changeLane"
                else:
                    self.driver.car.a = -min(self.driver.car.velocity - self.nowStatus["carInChaseLeft" + self.nowStatus["lane"]].velocity, self.nowStatus["pos"][0].maxa)
        else:
            if self.driver.car.velocity > self.driver.holdV:
                self.driver.car.a = -min(self.driver.car.velocity - self.driver.holdV, self.nowStatus["pos"][0].maxa)
            elif self.driver.car.velocity < self.driver.holdV:
                self.driver.car.a = min(self.driver.holdV - self.driver.car.velocity, self.nowStatus["pos"][0].maxa)
            if self.nowStatus["carInView" + self.nowStatus["lane"]] != None:
                if self.driver.car.velocity > self.nowStatus["carInView" + self.nowStatus["lane"]].velocity:
                    self.driver.car.a = -min(self.driver.car.velocity - self.nowStatus["carInView" + self.nowStatus["lane"]].velocity, self.nowStatus["pos"][0].maxa)
        
        return "move"
            
        
        
        
        
        