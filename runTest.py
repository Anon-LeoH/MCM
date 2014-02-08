from Test import test
from copy import deepcopy as cpy

f1 = open("Data/data", "w")

def runTest(template_test,type_name):
    tmpTest1 = cpy(template_test)
    tmpTest1.type = type_name
    time = 0
    for j in xrange(tmpTest1.testTime):
        tmpTest1.clearCrash()
        tmpTest1.handleCarIn()
        tmpTest1.handleCarOut()
        tmpTest1.handleSwitch()
        tmpTest1.handleMove()
        tmpTest1.handleCrash()
        tmpTest1.finish()
        tmpTest1.makeDecision()
        time += 1
    while tmpTest1.drivers != []:
        tmpTest1.clearCrash()
        tmpTest1.handleCarOut()
        tmpTest1.handleSwitch()
        tmpTest1.handleMove()
        tmpTest1.handleCrash()
        tmpTest1.finish()
        tmpTest1.makeDecision()
        time += 1
    f1.write(type_name + " : " + str( {"car in": tmpTest1.inCar, "car out": tmpTest1.receiveCar, "crash times": tmpTest1.crashCar, "test time": time, "road length": tmpTest1.road.length, "Vmin": tmpTest1.road.Vmin, "Vmax": tmpTest1.road.Vmax} ) + "\n")

for i in xrange(10):
    tmpTest = test()
    runTest(tmpTest,"RightHand")
    runTest(tmpTest,"NoRule")
    f1.write('\n')
    
f1.close()