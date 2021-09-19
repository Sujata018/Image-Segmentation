import cv2 as cv
from skimage.filters import threshold_otsu
from skimage.filters.rank import entropy
from skimage.morphology import erosion,dilation,opening,closing,disk
from matplotlib import pyplot as plt
from itertools import combinations
from math import dist 
from shapely.geometry import LineString,Polygon
import numpy as np

def identifyPores(img,areaThresh,circleThresh=0.2):
        img=img.astype(np.uint8)                                  # convert to accepted unsigned 8 bit integer for open CV
        contours, hierarchy = cv.findContours(img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

        for j in range(len(contours)):                            # for each contour
            if hierarchy[0][j][2]>0:                              #   if it has a child contour (hole inside), fill it up in gray level 127
                cv.drawContours(img,[contours[j]],-1,127,thickness=cv.FILLED)
            else:
                area=cv.contourArea(contours[j])
                if area > areaThresh:                             # bigger contours are pores
                    cv.drawContours(img,[contours[j]],-1,175,thickness=cv.FILLED)
                else:
                    _,radius = cv.minEnclosingCircle(contours[j]) # get radius of the smallest enclosing circle
                    areaCircle=np.pi*radius*radius                # calculate area of the circle 
                    diffArea=areaCircle-area                      # difference between area of enclosing circle and the contour area
                    if diffArea/areaCircle <= circleThresh:       # circle like contours are pores
                         cv.drawContours(img,[contours[j]],-1,210,thickness=cv.FILLED)
        return img

if __name__=='__main__':

    file=['s_0053.jpg','s_0002.tif','s_0001.tif','s_0012.tif','s_0213.jpg','s_0026.tif','s_0010.jpg','s_0016.tif','s_0024.tif','s_0027.tif','s_0028.tif',
          's_0032.tif','s_0034.tif','s_0054.jpg','s_0056.jpg','s_0104.jpg','s_0120.jpg',
          's_0162.jpg','s_0179.jpg','s_0180.jpg','s_0194.jpg','s_0213.jpg']

 #   for i in range(len(file)):
    for i in range(4):        
        ## read image
        img=cv.imread(file[i])                       # read input image
        print(img.shape)
        
        if img is None:
            sys.exit('File name '+file+' does not exist')

        imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # BGR to grayscale
        
        areaThresh=(img.shape[0]*img.shape[1])/528   # contours with area > 0.189 % of the whole image are identified as pores
        kernel=disk(10)                              # create disc kernel for erosion

        ## segment on HE image based on Otsu threshold
        himg=255 - cv.equalizeHist(imgray)           # histogram equalization and negation 
        thresh=threshold_otsu(himg)                  # Otsu thresholding of histogram equalised image
        ohimgi=np.where(himg<thresh,0,255)
        cv.imwrite(file[i][:-4]+'_HE_Otsu.bmp',ohimgi)

        ## identfy pores
        ohimgi=opening(ohimgi,kernel)                # morphological open operation to remove small minerals 
        pimg=identifyPores(ohimgi,areaThresh)        # identify pores
        oimg=np.where((pimg==127)|(pimg==175),0,255) # ignores small round pores (pimg==210), as they might appear out of open operation 
        oimg=closing(oimg,kernel)                    # closing to make the boundary smooth
        oimg=oimg.astype(np.uint8)
        cv.imwrite(file[i][:-4]+'_HE_Otsu_pores.bmp',oimg)
        
        ## calculate distances among all pairs of pores

        contour, _ = cv.findContours(255-oimg,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)  # identify contours in the negative pore image

        contours = [cv.approxPolyDP(c,0.01*cv.arcLength(c,True),True) for c in contour] # reduce number of points in the contours, by approximating their shapes as a polygons

        distances=[]                                                                    # list to store all distances among pores, to be used to draw histigram of pore distances
        print("number of contours = ",len(contours),',points in the first contour = ',contours[0])
#        k=0

        for cnt1,cnt2 in combinations(contours,2):                                      # pick up each pair of pores
            for pt1 in cnt1:
                pt1=tuple(pt1[0])                                                       # convert contour points to (x,y) format
                for pt2 in cnt2:
                    pt2=tuple(pt2[0])
                    line=LineString([pt1,pt2])                                          # between each pairs of points from the two contours, draw a line
                    cross=False                                                         # this boolean variable denotes if the line crosses any of the pores in the image
                    for cnt in contours:
                        polygon=Polygon([tuple(c[0]) for c in cnt])
                        if line.crosses(polygon):                                       # for each contour in the images, check if the line crosses the contour
                            cross=True
                            break
                    if cross == False:        
                        distances.append(dist(pt1,pt2))                                 # if the line does not cross any of the pores, then add this distance to histogram 
                        cv.line(img,pt1,pt2,(0,255,255),2)                              # draw a line, in yellow, in the image, to show the distance
#            k += 1
#            print(len(distances),' distances recorded so far :',k)

        plt.clf()
        plt.hist(distances)                                                             # plot histogram between pores
        plt.title('Histogram of distances between pores')
        plt.xlabel('Distance in pixels')
        plt.savefig(file[i][:-4]+'_porosity histogram.png')
        
        cv.drawContours(img,contours,-1,(0,255,0),3)                                    # draw the pores as well, in green, on top of the original image
           
        cv.imwrite(file[i][:-4]+'_pore_distances.png',img)
