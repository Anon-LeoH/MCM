from Test import test
from copy import deepcopy as cpy

f1 = open("Data/data", "w")

for i in xrange(20):
    tmpTest1 = test()
    tmpTest2 = cpy(tmpTest1)
    tmpTest2.type = "NoRule"
    for j in xrange(tmpTest1.testTime):
        tmpTest1.clearCrash()
        tmpTest1.handleCarIn()
        tmpTest1.handleCarOut()
        tmpTest1.handleSwitch()
        tmpTest1.handleMove()
        tmpTest1.handleCrash()
        tmpTest1.finish()
        tmpTest1.makeDecision()
    f1.write("Right hand: " + str( {"car in": tmpTest1.inCar, "car out": tmpTest1.receiveCar, "crash times": tmpTest1.crashCar, "test time": tmpTest1.testTime, "road length": tmpTest1.road.length, "Vmin": tmpTest1.road.Vmin, "Vmax": tmpTest1.road.Vmax} ) + "\n")
    time = 0
    for j in xrange(tmpTest2.testTime):
        tmpTest2.clearCrash()
        tmpTest2.handleCarIn()
        tmpTest2.handleCarOut()
        tmpTest2.handleSwitch()
        tmpTest2.handleMove()
        tmpTest2.handleCrash()
        tmpTest2.finish()
        tmpTest2.makeDecision()
    f1.write("No Rule: " + str( {"car in": tmpTest2.inCar, "car out": tmpTest2.receiveCar, "crash times": tmpTest2.crashCar, "test time": tmpTest2.testTime, "road length": tmpTest2.road.length, "Vmin": tmpTest2.road.Vmin, "Vmax": tmpTest2.road.Vmax} ) + "\n")
    f1.write("\n")
f1.close()
    