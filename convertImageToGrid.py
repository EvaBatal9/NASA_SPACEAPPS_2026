import cv2 as cv
import numpy as np

def convertTopologyToGrid(file,tolerance,point):
    square=cv.imread(file)
    squareHSV=cv.cvtColor(square, cv.COLOR_BGR2HSV)
    colour=squareHSV[point[0],point[2]]
    lower=[0,0]
    upper=[255,255]
    if colour[0]-tolerance<0:
        lower.insert(0,0)
    else:
        lower.insert(0,colour[0]-tolerance)
    if colour[0]+tolerance>179:
        upper.insert(0,179)
    else:
        upper.insert(0,colour[0]+tolerance)
    lower=np.array([lower])
    upper=np.array([upper])
    squareHSV=cv.cvtColor(square, cv.COLOR_BGR2HSV)
    mask=cv.inRange(squareHSV,lower,upper)
    return mask