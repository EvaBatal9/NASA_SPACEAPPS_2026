import cv2 as cv
import numpy as np
import tifffile
import zarr

def convertCoordinatesToPixel(image,coordinates):
    height=image.shape[0]
    width=image.shape[1]
    lat=90.0+coordinates[0]
    lon=coordinates[1]
    pVert=round(height*(lat/180.0))
    pHor=round(width*(lon/360.0))
    return (width-pHor,pVert)
def pointSafeRadius(point,image):
    circleMask=cv.imread("test.png",cv.IMREAD_GRAYSCALE)
    cv.circle(circleMask,point,10,255,-1)
    targetCircle=cv.bitwise_and(image,circleMask);
    if cv.countNonZero(targetCircle)>=cv.countNonZero(circleMask)*0.95:
        return True
    else:
        return False;

glacierPointsFile=open("glaciers.txt")
glacierPoints=[]
for point in glacierPointsFile.readlines():
    point=point.replace(",",".")
    point=point.split("\t")
    lat=float(point[1])
    lon=float(point[0])
    glacierPoints.append([lat,lon])

topo=tifffile.imread("topo.tiff",aszarr=True)
z = zarr.open(topo, mode="r")
mars=cv.imread("mars.png")
okAreas=cv.imread("testmap.png",cv.IMREAD_GRAYSCALE)
for point in glacierPoints:
    pixel=convertCoordinatesToPixel(okAreas,point)
    if pointSafeRadius(pixel,okAreas):
        cv.circle(mars,pixel,2,(0,255,0),-1)
cv.imwrite("output.png",mars)
croppedTopo=z[0, 0:500, 0:500];
cv.imwrite("please.png",croppedTopo)