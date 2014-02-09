from Test import test
from copy import deepcopy as cpy
from Road import Road
from Driver import driver
import random

f1 = open("Data/data", "a")
f2 = open("Data/driver", "w")
test_type = ["RightHand","NoRule","SpeedFirst","NS"]
type_len = 4
road_type = Road()
drivers_list = [ [] , [] , [] , [] ]
show_time = [ [] , [] , [] , [] ]
PoissonCoef = random.uniform(0.05, 0.7)
testTimes = 1

def runTest(template_test,type_id):
    tmpTest1 = cpy(template_test)
    tmpTest1.type = test_type[type_id]
    #tmpTest1.road = road_type
    #tmpTest1.PoissonCoef = PoissonCoef
    pointer = 0
    totalCar = len(drivers_list[type_id])
    for j in xrange(tmpTest1.testTime):
        tmpTest1.clearCrash()
        if pointer < totalCar and show_time[type_id][pointer] == j:
            tmpTest1.handleCarIn(drivers_list[type_id][pointer])
            pointer += 1
        tmpTest1.handleCarOut()        
        tmpTest1.handleMove()
        tmpTest1.handleSwitch()
        tmpTest1.handleCrash()
        tmpTest1.finish()
        tmpTest1.calculateDensity()
        tmpTest1.makeDecision()
    f1.write(test_type[type_id] + " : " + str( {"car in": tmpTest1.inCar, "car out": tmpTest1.receiveCar, "crash times": tmpTest1.crashCar}) + "\n")

def init_drivers(testTime):
    inCarPro = 0
    cnt = 0
    for i in xrange(type_len):
        drivers_list[i] = []
        show_time[i] = []
    
    for j in xrange(testTime):
        Probability = random.random()
        inCarPro += Probability
        if inCarPro >= 1:
            inCarPro -= 1
        if inCarPro <= PoissonCoef:
            for i in xrange(type_len):
                drivers_list[i].append(driver(cnt,road_type,test_type[i]))
                show_time[i].append(j)
            cnt += 1
            inCarPro = 0
        else:
            drivers_list.append(None)

def outputCarInfo():
    for item in drivers_list[0]:
        f2.write(str({"HoldV" : item.holdV , "ReflectTime" : item.reflectTime , "ViewRange" : item.viewRange , "ChaseRange" : item.chaseRange , "SafeRange" : item.safeLine}) + "\n")
    
for i in xrange(testTimes):
    tmpTest = test()
    init_drivers(tmpTest.testTime)
    outputCarInfo()
    f1.write("Road type : " + str({"road length": tmpTest.road.length, "Vmin": tmpTest.road.Vmin, "Vmax": tmpTest.road.Vmax, "frequency": tmpTest.PoissonCoef , "test time": tmpTest.testTime}) + "\n")
    for j in xrange(type_len):
        runTest(tmpTest,j)
    f1.write("\n")
    print "Finish Case " + str(i + 1)
    
f1.close()
f2.close()