from Test import test

f1 = open("Data/data", "w")

for i in xrange(100000):
    tmpTest = test()
    time = 0
    for j in xrange(tmpTest.testTime):
        tmpTest.clearCrash()
        tmpTest.handleCarIn()
        tmpTest.handleCarOut()
        tmpTest.handleSwitch()
        tmpTest.handleMove()
        tmpTest.handleCrash()
        tmpTest.finish()
        tmpTest.makeDecision()
        time += 1
    while tmpTest.drivers != []:
        tmpTest.clearCrash()
        tmpTest.handleCarIn()
        tmpTest.handleCarOut()
        tmpTest.handleSwitch()
        tmpTest.handleMove()
        tmpTest.handleCrash()
        tmpTest.finish()
        tmpTest.makeDecision()
        time += 1
    f1.write(str( {"car in": tmpTest.inCar, "car out": tmpTest.receiveCar, "crash times": tmpTest.crashCar, "put in time": tmpTest.testTime, "finish time": time, "road length": tmpTest.road.length} ) + "\n")

f1.close()
    