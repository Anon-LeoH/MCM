from Test import test
from copy import deepcopy as cpy
from Road import Road
import random

f1 = open("Data/data", "w")
road = Road()
PoissonCoef = random.uniform(0.05, 0.6)

def runTest(template_test,type_name):
    tmpTest1 = cpy(template_test)
    tmpTest1.type = type_name
    tmpTest1.road = road
    tmpTest1.PoissonCoef = PoissonCoef
    time = 0
    for j in xrange(tmpTest1.testTime):
        tmpTest1.clearCrash()
        tmpTest1.handleCarIn()
        tmpTest1.handleCarOut()        
        tmpTest1.handleMove()
        tmpTest1.handleSwitch()
        tmpTest1.handleCrash()
        tmpTest1.finish()
        tmpTest1.calculateDensity()
        tmpTest1.makeDecision()
    f1.write(type_name + " : " + str( {"car in": tmpTest1.inCar, "car out": tmpTest1.receiveCar, "crash times": tmpTest1.crashCar, "test time": tmpTest1.testTime, "road length": tmpTest1.road.length, "Vmin": tmpTest1.road.Vmin, "Vmax": tmpTest1.road.Vmax, "frequency": tmpTest1.PoissonCoef} ) + "\n")

for i in xrange(20):
    tmpTest = test()
    runTest(tmpTest,"RightHand")
    runTest(tmpTest,"NoRule")
    f1.write('\n')
    print "Finish Case " + str(i + 1)
    
f1.close()