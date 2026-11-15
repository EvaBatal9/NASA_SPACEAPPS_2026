import cv2
import numpy as np

#give it the file name for the tile with the landing site and the tile with the collection site
def generateMapImage(landingSiteTile,collectionSiteTile):
    if(landingSiteTile==collectionSiteTile):
        return cv2.imread(landingSiteTile)
    else:
        rowL=int(landingSiteTile.split("x")[0][-1])
        colL=int(landingSiteTile.split("x")[1][0])
        rowC=int(collectionSiteTile.split("x")[0][-1])
        colC=int(collectionSiteTile.split("x")[1][0])
        landingSite=cv2.imread(landingSiteTile)
        collectionSite=cv2.imread(collectionSiteTile)
        if rowL<rowC:
            merged=np.vstack((landingSite,collectionSite))
        elif(rowL>rowC):
            merged=np.vstack((collectionSite,landingSite))
        elif(colL<colC):
            merged=np.hstack((landingSite,collectionSite))
        else:
            merged=np.hstack((collectionSite,landingSite))
        midWidth=merged.shape[1]//2
        midHeight=merged.shape[0]//2
        widthLower=midWidth-(landingSite.shape[1]//2)
        widthUpper=midWidth+(landingSite.shape[1]//2)
        heightLower=midHeight-(landingSite.shape[0]//2)
        heightUpper=midHeight+(landingSite.shape[0]//2)
        merged=merged[heightLower:heightUpper,widthLower:widthUpper]
        return merged
