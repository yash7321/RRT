import random
import math
import matplotlib.pyplot as plt
import sys

#Class for representing a 2D point 
class Node:
    def __init__(self,x,y):
        self.x=x  #x-coordinate of a point 
        self.y=y #y-coordinate of a point
        self.parent=None  #parent point which will form an edge with the current point

class Obstacle:
    def __init__(self,x,y,radius):
        self.x=x
        self.y=y
        self.radius=radius
    def checkForCollisionInPath(self,startNode,endNode):
        if (startNode.x-self.x)**2+(startNode.y-self.y)**2<self.radius**2 or (endNode.x-self.x)**2+(endNode.y-self.y)**2<self.radius**2:
            return True
        slope=(endNode.y-startNode.y)/(endNode.x-startNode.y)
        c=endNode.y-slope*endNode.x
        #perpendicular Intersection
        x=(self.x+self.y*slope-slope*c)/(slope*slope+1)
        y=slope*x+c
        if (startNode.x<=x<=endNode.x or endNode.x<=x<=startNode.x) and (startNode.y<=y<=endNode.y or endNode.y<=y<=startNode.y):
            if math.sqrt((startNode.x-x)**2+(startNode.y-y)**2)>0.01 and math.sqrt((endNode.x-x)**2+(endNode.y-y)**2)>0.01:
                return True
        return False


#class for implementing Rapidly Exploring Random Trees
class RRT:
    def __init__(self,startingPoint,finalPoint,obstacles,xMax,yMax,step):
        self.startingPoint=Node(startingPoint[0],startingPoint[1]) 
        self.finalPoint=Node(finalPoint[0],finalPoint[1])
        self.obstacles=obstacles # array of obstacles,where each obstacle is represented by the class Obstacle
        self.xMax=xMax
        self.yMax=yMax
        self.step=step #step size
        self.Nodes=[self.startingPoint] #array of nodes which are already in the path that leads to final point

    # method to get a random point
    def generateRandomNode(self):
        xCoordinate=random.uniform(0,self.xMax)
        yCoordinate=random.uniform(0,self.yMax)
        return Node(xCoordinate,yCoordinate)
    
    #method to get the closest point to the random point out of all the points in the path so far
    def getNearestNode(self,node):
        nearestNode=None
        nearestDistance=sys.maxsize
        for currNode in self.Nodes:
            currDistance=math.sqrt((node.x - currNode.x) ** 2 + (node.y - currNode.y) ** 2)
            if currDistance<nearestDistance:
                nearestDistance=currDistance
                nearestNode=currNode
        return nearestNode
    
    #method to check if the path between two points is free from any obstacles
    def isPathCollisionFree(self,startNode,endNode):
        for obstacle in self.obstacles:
            if obstacle.checkForCollisionInPath(startNode,endNode):
                return False
        return True
    
    #method to get the point after taking a step from nearest point of the random point
    def getStepNode(self,nearestNode,randomNode):
        if nearestNode==self.finalPoint:
            return self.finalPoint
        distanceBetweenRandomAndNearest=math.sqrt((randomNode.x-nearestNode.x)**2+(randomNode.y-nearestNode.y)**2)
        if distanceBetweenRandomAndNearest<=self.step:
            return randomNode
        #using the trigonometric relations to find the required point
        angle=math.atan2(randomNode.y-nearestNode.y,randomNode.x-nearestNode.x)
        x=nearestNode.x+self.step*math.cos(angle)
        y=nearestNode.y+self.step*math.sin(angle)
        if x<0 or x>self.xMax or y<0 or y>self.yMax:
            return None
        return Node(x,y)

    #method to return the first path which connects starting point and ending point
    def findPath(self):
        for obstacle in self.obstacles:
            plotCircle=plt.Circle((obstacle.x, obstacle.y), obstacle.radius, color='k')
            plt.gca().add_artist(plotCircle)

        plt.plot(self.startingPoint.x, self.startingPoint.y, 'ro', markersize=5)
        plt.plot(self.finalPoint.x, self.finalPoint.y, 'go', markersize=5)

        while True:
            randomNode=self.generateRandomNode()
            plt.plot(randomNode.x, randomNode.y, 'bo', markersize=1) 

            nearestNode=self.getNearestNode(randomNode)
            nodeAfterStep=self.getStepNode(nearestNode,randomNode)

            if self.isPathCollisionFree(nearestNode,randomNode) and nodeAfterStep:
                nodeAfterStep.parent=nearestNode
                self.Nodes.append(nodeAfterStep)

                plt.plot([nodeAfterStep.x, nearestNode.x], [nodeAfterStep.y, nearestNode.y], '-g',
                         linewidth=0.5)  # plot the new path
                plt.pause(0.15) 

                if math.sqrt((nodeAfterStep.x-self.finalPoint.x)**2+(nodeAfterStep.y-self.finalPoint.y)**2)<self.step:
                    requiredPath=[]
                    currNode=nodeAfterStep

                    while currNode.parent:
                        requiredPath.append((currNode.x,currNode.y))
                        currNode=currNode.parent

                    requiredPath.append((self.startingPoint.x,self.startingPoint.y))
                    xValues=[]
                    yValues=[]

                    for i in range(len(requiredPath)):
                        xValues.append(requiredPath[i][0])
                        yValues.append(requiredPath[i][1])

                    plt.plot(xValues, yValues, '-r')  # plot the final path
                    plt.plot([nodeAfterStep.x, self.finalPoint.x], [nodeAfterStep.y, self.finalPoint.y], '-r',
                             linewidth=2)  # draw last edge to goal
                    return requiredPath[::-1]
           
        return []  
            
                
            

            

startingPoint=[float(x) for x in input("Enter Start Point - Provide X and Y Coordinate ").split()] #starting point
finalPoint = [float(x) for x in input("Enter Final Point - Provide X and Y Coordinate ").split()] #ending point

k=int(input("Enter Number of Obstacles to be placed ")) #number of obstacles
obstacles=[]
for i in range(k):
    currObstacleData=[int(x) for x in input().split()]
    obstacles.append(Obstacle(currObstacleData[0],currObstacleData[1],currObstacleData[2]))


xMax=float(input("Enter Maximum X Coordinate "))
yMax=float(input("Enter Maximum Y Coordinate "))


step=float(input("Enter Step Size Value "))



RapidlyExploringRandomTree=RRT(startingPoint,finalPoint,obstacles,xMax,yMax,step)

path=RapidlyExploringRandomTree.findPath()
            

if path:
    path.append(finalPoint)
    print(path)
    xValues,yValues=[],[]
    for i in range(len(path)):
      xValues.append(path[i][0])
      yValues.append(path[i][1])
    plt.plot(xValues, yValues, '-r')
else:
    print("Could not find path.")

for obstacle in obstacles:
    circle = plt.Circle((obstacle.x, obstacle.y), obstacle.radius, color='k')
    plt.gcf().gca().add_artist(circle)

plt.plot(startingPoint[0], startingPoint[1], 'bo')
plt.plot(finalPoint[0], finalPoint[1], 'go')
plt.axis('scaled')
plt.xlim((0, xMax))
plt.ylim((0, yMax))
plt.show()