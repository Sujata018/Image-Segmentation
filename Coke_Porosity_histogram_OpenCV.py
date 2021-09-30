import cv2 as cv
from matplotlib import pyplot as plt
from itertools import combinations
from math import dist 
from shapely.geometry import LineString,Polygon
import numpy as np

'''
Program for porosity calculation of a coke image, using openCV and shapely
'''
def identifyPores(img,areaThresh,circleThresh=0.2):
        '''
        Given a binary image with black portions converted to white, this functin, looks at the size and type of each white contour
        to differentiate between pores and minerals in a coke image

        Imput:   img          -> binary negative image of the coke.
                 areaThresh   -> threshold value of area of a contour. Bigger contours than this threshold are classified as pores.
                 circleThresh -> threshold for the difference of area between a circle just enclosing the contour and the contour area
                                 as a percentage of the contour area. If the difference is less than this threshold, then the contour
                                 is identified as circular. And circular regions are identified as pores.
                                 Default value : 0.2 (=20%).
        Output:  img, with pixels in following gray level values:
                 127 : The contour regions identified as pores because there are wholes in them.
                 175 : The contour regions with no holes, but area > areaThresh.
                 210 : The contour regins with no holes and area <= areaThresh, but are circular.
                 0   : Rest of the regions.
                 
        Logic:   Identify all contour hiararchy.
                 1. For each parent contour, identify if it has a child (that means id there is a hole in the contour).
                    Pores in coke will have whiter reflections from bottom of the pores, in image. If there is such
                    whiter portion (hole inside contour), then the contour is definitely a pore.
                    Color the contour area in gray level 127.
                 2. If there is no such reflection, but the contour is large, then it is classified as a pore. A threshold, areaThresh,
                    of the area of the contour, is used for this classification. Color the contour with gray level 175.
                 3. In case the contour area is smaller than or equal to areaThresh, but the contour is almost circular, then also it
                    is classified as a pore. A threshold circleThresh is passed in input, that is used to measure how close the contour has
                    to be to a circle, to be identified as a pore. Color the pore with gray level 210.
                 Rest of the contours remain in white.
                 
                 The program, using output image from this function, can choose some or all of thes above criteria for pore identification.
                 Convert the gray levels related to the criteria chosen, to black, and rest to white.
        '''
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

'''
This is the main program.
For each file name in the list 'file', read the file and identify pores in it, and then create a histogram with the inter-pore distances.

Parameters used:
        file       : Add all input file names in this list
        areaThresh : gray scale image area / 528. Increase 528, if smaller areas should also be pores.
        maxDist    : 0.01. Decrease it to make more accurate approximation of pores as polygons.
        kernel     : ellipse(20,20). Increase 20s if more effects required for open and close operations.
'''
if __name__=='__main__':

    file=['s_0053.jpg','s_0002.tif','s_0001.tif','s_0012.tif','s_0213.jpg','s_0026.tif','s_0010.jpg','s_0016.tif','s_0024.tif','s_0027.tif','s_0028.tif',
          's_0032.tif','s_0034.tif','s_0054.jpg','s_0056.jpg','s_0104.jpg','s_0120.jpg',
          's_0162.jpg','s_0179.jpg','s_0180.jpg','s_0194.jpg','s_0213.jpg']

 #   for i in range(len(file)):
    for i in range(1):        
        ## read image
        img=cv.imread(file[i])                                    # read input image
        print(img.shape)
        
        if img is None:
            sys.exit('File name '+file+' does not exist')

        imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)              # BGR to grayscale
        
        areaThresh=(img.shape[0]*img.shape[1])/528                # contours with area > 0.189 % of the whole image are identified as pores
        maxDist=0.01                                              # Accuracy for approximatiopn of pore contours as polygons. This is the maximum distance (as percentage of the pore perimeter) between the original curve and its approximation.
        kernel=cv.getStructuringElement(cv.MORPH_ELLIPSE,(20,20)) # create disc kernel for morphological operations open and close
        
        ## segment on HE image based on Otsu threshold
        himg=cv.equalizeHist(imgray)                              # histogram equalization 
        thresh,_=cv.threshold(himg,255,0,cv.THRESH_BINARY+cv.THRESH_OTSU)# Otsu thresholding of histogram equalised image, and negative (255 for pixel value < threshold, 0 for value > threshold)
        ohimgi=np.where(himg>thresh,0,255)
        cv.imwrite(file[i][:-4]+'_HE_Otsu.jpg',ohimgi)
        
        ## identfy pores
        ohimgi=ohimgi.astype(np.uint8)                            # convert to accepted unsigned 8 bit integer for open CV
        ohimgi=cv.morphologyEx(ohimgi,cv.MORPH_OPEN,kernel)       # morphological open operation to remove small minerals

        pimg=identifyPores(ohimgi,areaThresh)                     # identify pores
        oimg=np.where((pimg==127)|(pimg==175),0,255)              # ignores small round pores (pimg==210), as they might appear out of open operation 
        oimg=oimg.astype(np.uint8)                                # convert to accepted unsigned 8 bit integer for open CV
        oimg=cv.morphologyEx(oimg,cv.MORPH_CLOSE,kernel)          # closing to make the boundary smooth
        cv.imwrite(file[i][:-4]+'_HE_Otsu_pores.jpg',oimg)
            
        ## calculate distances among all pairs of pores

        contour, _ = cv.findContours(255-oimg,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)  # identify contours in the negative pore image

        contours = [cv.approxPolyDP(c,maxDist*cv.arcLength(c,True),True) for c in contour] # reduce number of points in the contours, by approximating their shapes as a polygons

        distances=[]                                                                    # list to store all distances among pores, to be used to draw histigram of pore distances

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

        plt.clf()
        plt.hist(distances)                                                             # plot histogram between pores
        plt.title('Histogram of distances between pores')
        plt.xlabel('Distance in pixels')
        plt.savefig(file[i][:-4]+'_porosity histogram.png')
        
        cv.drawContours(img,contours,-1,(0,255,0),3)                                    # draw the pores as well, in green, on top of the original image
           
        cv.imwrite(file[i][:-4]+'_pore_distances.png',img)
        
