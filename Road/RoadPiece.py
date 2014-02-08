import random
class RoadObject(object):
    def __init__(self):
        pass

class pieceOfRoad(object):
    def __init__(self, length):
        self.length = length
        self.curve = False

def makeCurve(RoadPiece, minRadius):
    RoadPiece.curve = True
    RoadPiece.radius = random.uniform(minRadius, minRadius + 1000)
    RoadPiece.viewRange = ((RoadPiece.radius + 7.5) ** 2 - RoadPiece.radius ** 2) ** 0.5
    return RoadPiece
    