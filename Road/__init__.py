from RoadPiece import pieceOfRoad, makeCurve
import random

VLimit = [(40 / 3.6, 80 / 3.6), (40 / 3.6, 120 / 3.6),
          (60 / 3.6, 120 / 3.6), (60 / 3.6, 160 / 3.6),
          (80 / 3.6, 160 / 3.6)]
ROADTYPE = ["asphalt", "concrete", "gravel"]
FC = {
         ("asphalt", "dry"): 0.675, 
         ("asphalt", "wet"): 0.45, 
         ("concrete", "dry"): 0.62,
         ("concrete", "wet"): 0.485,
         ("gravel", "dry"): 0.5,
         ("gravel", "wet"): 0.35,
     }
g = 9.83218
     
class Road(object):
    def __init__(self):
        Probability = random.random()
        for i in xrange(5):
            if Probability <= (i + 1) * 0.2:
                (self.Vmin, self.Vmax) = VLimit[i]
                break
        self.piece = []
        Probability = random.random()
        if Probability <= 0.5:
            self.type = ROADTYPE[0]
        elif Probability <= 0.9:
            self.type = ROADTYPE[1]
        else:
            self.type = ROADTYPE[2]
        Probability = random.random()
        if Probability <= 0.5:
            self.weather = "dry"
        else:
            self.weather = "wet"
        self.fc = FC[(self.type, self.weather)]
        self.minRadius = self.Vmax ** 2 / self.fc / g
        numberOfCurve = random.randint(0, 10)
        self.piece.append(pieceOdRoad(randint(2000, 80000)))
        for i in xrange(numberOfCurve):
            self.piece.append(makeCurve(pieceOfRoad(random.randint(1000, 5000)), self.minRadius))
            self.piece.append(pieceOdRoad(randint(2000, 80000)))
        self.numberOfPiece = len(self.piece)
        
