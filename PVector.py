# Rylan Hunter
# ECEN 689 - Final Project Code

# THIS IS A SUPPORTING FILE FOR THE SMART_ROCKETS PROJECT
# It is basically a simple vector class, 2D (x,y) coordinate pairs. Has methods to add, calculate distance
# between vectors, initialize from an input angle, limit its magnitude, etc.
import math

class PVector:

    def __init__(self, xx=0, yy=0, lim=9999999999):
        self.x = xx
        self.y = yy
        self.limit = lim

    def nul(self):
        self.x, self.y = 0.0, 0.0
        self.limit = 9999999999

    def __add__(self, other):
        newx = self.x + other.x
        newy = self.y + other.y
        return PVector(newx, newy)

    def add(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        mag = self.magnitude(self)
        if mag>self.limit:
            #normalize
            xtmp = (self.x / mag) * self.limit
            ytmp = (self.y / mag) * self.limit
            self.x = xtmp
            self.y = ytmp

    def setLimit(self,lim):
        self.limit = lim

    def getVec(self):
        return [self.x,self.y]

    def getTuple(self):
        return (self.x,self.y)

    @staticmethod
    def dist(pvec1, pvec2):
        x_dist = pvec1.x - pvec2.x
        y_dist = pvec1.y - pvec2.y
        return math.sqrt(x_dist * x_dist + y_dist * y_dist)

    @staticmethod
    def fromAngle(theta=0):
        return PVector(math.cos(theta),math.sin(theta))

    @staticmethod
    def magnitude(pvec):
        mag = math.sqrt(math.pow(pvec.x,2) + math.pow(pvec.y,2))
        return mag


'''
p1 = PVector().fromAngle(13*math.pi/180)
arr1 = p1.getVec()
print(arr1)

directions = []
for i in range(0, 3):
    ang = (30+i*15)*math.pi/180
    directions.append(PVector.fromAngle(ang))


for i in range(0, 3):
    arr = directions[i].getVec()
    print(arr)

#print(p2.x)
#print(directions)
arr = directions[1].getVec()
#print(arr)


p11 = PVector(2,1)
p11.setLimit(3)
p12 = PVector(1,3)

p11.add(p12)
arr = p11.getVec()
print(arr)
'''
