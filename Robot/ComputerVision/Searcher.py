import time
import cv2 #as cv
import numpy as np
import sys
import math

# ================
# ---- Notes: ----
# ================
#
#
# TODO: I haven't been able to let 'findTarget' return 'Forward' maybe the range needs to be extended
# TODO: this class will take in account that the camera uses a resolution which shows the ground, and the walls
#       this is why it calculates the average: because the walls don't need to be scanned for objects
#       however a resolution may be given on which only the ground will be seen (for example for optimalisation purposes)
#       when this is done, the average calculations need to be removed
#       please keep this in mind
#
# --Function--
#
# the 'Searcher' class has the purpose of finding any objects in a terrain, it can be used to get a direction for a robot to steer in, in order to find the biggest object
# the biggest object has been given the highest priority because it is most likely the most nearby
# either 'Forward', 'Steer left', 'Steer right', 'No items found' or 'Error', will be returned as a string depending on the location of any found objects
#
#
# --How to use--
#
# 1. call the 'findTarget' function, which will almost immeadially call the 'createRadar' function
# 2. the purpose for the 'createRadar' method is to first create a radar, which it uses to check diferences in height on a terrain
#    when the difference is under the average of the radar, this class will classify it as an object
#    this method will return a black image on which a surten number of objects may be located
#    these objects will be represented as thick, red lines
# 3. after calling the 'createRadar' method, the findTarget will first check if there are any items at all
#    if there are found items, it will search for the biggest target and draw that target on an emty black image (otherwise 'No items found' will be returned)
#    finally, it will determine if the target is at left, or the right of the middle of the screen (but not before checking if the target is in front of the screen)
#
#
# to have created the radar function, code from the Big face Robotics has been moddified: https://github.com/BigFace83/BFRMR1
class Searcher:

    # a lot of variables will be defined within the '__init__' class
    # the camera argument needs to be the videocapture
    # Debugg is a boolean which determines if images should be shown, make it true when this is needed
    def __init__(self, camera, Debugg):
        # 'black' is a literal black image, which is used to put the ground drawing on, making it more noticeable
        self.black = cv2.imread('img/Pure_Black.png')
        self.capture = camera
        #self.capture.set(3,640) # 1024 640 1280 800 384
        #self.capture.set(4,480) # 600 480 960 600 288
        self.StepSize = 8
        self.DisplayImage = Debugg

     
    def createRadar(self):
        
        
        # 'EdgeArray' stores the X and Y values of any found edges within the 'imgEdge' image
        # do NOT define any array at __init__, when running in a while loop
        EdgeArray = []
        AverageY = []
        DetectionArray = []
        # when async, black needs to be defined again, to clear radar
        black = self.black
        # let image settle
        time.sleep(0.1)
        ret,img = self.capture.read() # get a bunch of frames to make sure current frame is the most recent
        ret,img = self.capture.read() 
        ret,img = self.capture.read()
        ret,img = self.capture.read()
        ret,img = self.capture.read() # 5 seems to be enough

        # resize the black background to the cameraframe
        width = int(img.shape[1])
        height = int(img.shape[0])
        dim = (width, height)
        black = cv2.resize(black, dim, interpolation = cv2.INTER_AREA)
        
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #convert img to grayscale and store result in imgGray
        imgGray = cv2.bilateralFilter(imgGray,9,30,30) #blur the image slightly to remove noise             
        imgEdge = cv2.Canny(imgGray, 50, 100)             #edge detection
        
        imagewidth = imgEdge.shape[1] - 1 # the width of the 'imEdge' image = 639
        imageheight = imgEdge.shape[0] - 1 # the height of the 'imEdge' image  = 479
        
        for j in range (0,imagewidth,self.StepSize): # for the width of image array
            for i in range(imageheight-5,0,-1):      # step through every pixel in height of array from bottom to top
                                                        # ignore first couple of pixels as may trigger due to undistort
                if imgEdge.item(i,j) == 255:         # check to see if the pixel is white which indicates an edge has been found
                    EdgeArray.append((j,i))          # if it is, add x,y coordinates to ObstacleArray
                    AverageY.append(i)               # every found y coordinate will be stored in a list, with the purpose of calculating the average later
                    break                            # if white pixel is found, skip rest of pixels in column
            else:                                    # no white pixel found
                EdgeArray.append((j,0))              # if nothing found, assume no obstacle. Set pixel position way off the screen to indicate
                                                        # no obstacle detected
                
        
        for x in range (len(EdgeArray)-1):      #draw lines between points in ObstacleArray 
            cv2.line(black, EdgeArray[x], EdgeArray[x+1],(255,255,255),1) 
        for x in range (len(EdgeArray)):        #draw lines from bottom of the screen to points in ObstacleArray
            cv2.line(black, (x*self.StepSize,imageheight), EdgeArray[x],(255,255,255),1)
            
        # the average of all y coordinates will be calculated here
        sumy = sum(AverageY)
        leny = len(AverageY)
        # the if statement is protection: it prevents the program trying to divide with zero (will result in a crash)
        if sumy == 0 | leny == 0:
            Average = 1
        else:
            Average = sum(AverageY) / len(AverageY)
        # the print line is for debugg purposes, may be deleted later
        #print('Average: ', Average)
        
        for j in range (0,imagewidth,self.StepSize): # we'll draw lines again, using imgEdge, but with a few differences
            for i in range(imageheight-5,0,-1):      # for starters the line drawn is thicker and red, for easy detection
                                                        # but more importantly, it will only draw a line when the y value is higher than the average
                if imgEdge.item(i,j) == 255:         # this solution may be temporary, a fixed int may be assigned later
                    if i > Average:
                        DetectionArray.append((j,i)) #
                        break                        # the drawing of the lines happens within the for loop, because the function can only draw one line at a time
                    elif DetectionArray != []:
                        for x in range (len(DetectionArray)-1):     
                            cv2.line(black, DetectionArray[x], DetectionArray[x+1],(0,0,255),10)
                        DetectionArray = []
            else:                                   
                EdgeArray.append((j,0))             
                                                    
        # 'target' will be only the thick, red lines
        target = Searcher.findStuff(black) 
        # display both the camera and the radar
        if self.DisplayImage is True:
            cv2.imshow("camera", img)
            cv2.imshow("Radar", black)
            cv2.imshow("Target",target)
            
        return target


    # the 'findStuff' method is some kind of filter that will remove the radar effect on a black image, while keeping the thick, red lines
    # it takes a black image, containing the radar and the targets as an argument and will return the same image without the radar
    def findStuff(img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # define range of red color in HSV
        lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        lower_red2 = np.array([170,50,50])
        upper_red2 = np.array([180,255,255])
        
        # Threshold the HSV image to get only red colors
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 | mask2

        res = cv2.bitwise_and(img,img, mask= mask)
        return res

    # 'findTarget' will return a string containing either: 'forward', 'steer left', 'steer right', 'no items found' or 'Error'
    # when 'Error' is returned, something went wrong within this method
    def findTarget(self):
        direction = 'Error'
        # try to find objects, using the createRadar method
        junk = Searcher.createRadar(self)
        
        if self.DisplayImage is True:
            cv2.imshow('debugg1', junk)
        black = self.black
        # resize the black background to the cameraframe again
        width = int(junk.shape[1])
        height = int(junk.shape[0])
        dim = (width, height)
        black = cv2.resize(black, dim, interpolation = cv2.INTER_AREA)
        # convert to grayscale
        junkgray = cv2.cvtColor(junk, cv2.COLOR_BGR2GRAY)

        # checks if the image has found no targets
        # you can emulate this by covering the camera, while running 'createRadar'
        itemcheck = False
        for j in range (0,width,self.StepSize):
                for i in range(height-5,0,-1):      
                                                         
                    if junkgray.item(i,j) != 0:         
                        itemcheck = True         
                        break                      
        if itemcheck is False:
            direction = ('No items found')
            return direction
        
        
        # invert colour
        ret,th = cv2.threshold(junkgray,1,255,cv2.THRESH_BINARY)
        # make image binary
        ret, thresh = cv2.threshold(th, 127, 255, 0)
        AreaArray = []
    
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        hierarchy = hierarchy[0]
        # this for loop collects all areas of the contours
        for cnr in range(len(contours)):
            cnt = contours[cnr]
            area = cv2.contourArea(cnt)
            AreaArray.append(area)
        # calculate the max area
        maxarea = max(AreaArray)
        counter = 0
        for cnr in range(len(contours)):
            cnt = contours[cnr]
            area = cv2.contourArea(cnt)
            if area >= maxarea:
                #print('Target number: ', counter)
                target = cv2.drawContours(black, [cnt], -1, (255,255,255), 3)
                break
            else:
                counter = counter + 1
        if self.DisplayImage is True:
            cv2.imshow('result', target)

        targetwidth = target.shape[1] - 1 # the width of the 'target' image
        targetheight = target.shape[0] - 1 # the height of the 'target' image
        # 'halfwidth' is currently a magic number, this can be changed with the commented code beneath, but it gave certain troubles
        halfwidth = 319
        #halfwidth = targetwidth / 2 - width % 2
        
        
        # convert to grayscale, because the .item check does difficult with colour images
        targetgray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        # first checks if the target is located at the center of the screen
        for j in range (halfwidth): 
                for i in range(targetheight-5,0,-1):
                                                     
                    if targetgray.item(i,j) == 255:     
                        direction = 'Forward'
                        return direction
                        break                       
                else:                               
                    break
        # after this, it will check if it is located either left or right of the center of the screen
        for j in range (0,targetwidth,self.StepSize):    
                for i in range(targetheight-5,0,-1):     
                                                         
                    if targetgray.item(i,j) == 255:          
                        if j < halfwidth:
                            direction = 'Steer left'
                        else:
                            direction = 'Steer right'
                        break                            
                              
                                                         
        return direction

            
#
#
#
#
#
#   XXXXXXX         XXXXXXX         JJJJJJJJJJJJJJJ                             999999999
#    XXXXXXX       XXXXXXX          JJJJJJJJJJJJJJJ                           9999999999999
#     XXXXXXX     XXXXXXX                 JJJJ                               999999   999999
#      XXXXXXX   XXXXXXX                  JJJJ                              999999     999999
#       XXXXXXX XXXXXXX                   JJJJ                              99999       99999
#         XXXXXXXXXXX                     JJJJ          ------------        999999     999999
#         XXXXXXXXXXX                     JJJJ          ------------        9999999   9999999
#       XXXXXXX XXXXXXX           JJJJ    JJJJ                               9999999999999999
#      XXXXXXX   XXXXXXX          JJJJ    JJJJ                                   9999999999
#     XXXXXXX     XXXXXXX         JJJJ    JJJJ                                      999999
#    XXXXXXX       XXXXXXX        JJJJJJJJJJJ                                         9999
#   XXXXXXX         XXXXXXX        JJJJJJJJ                                  9999   99999 
#                                                                             9999999999
#                                                                              9999999
#
#
#
#                           TTTTTT  h       eee         WW       WW     A     KK  KK   EEEE    MM MM       A     N  N   SSS
#                             TT    h hh   e   e         WW WWW WW     A A    KK KK    EEE    MMMMMMM     A A    NN N   SS
#                             TT    hh  h  eeeee          WWWWWWW     AAAAA   KKKK     EEE   MM MMM MM   AAAAA   N NN    SS
#                             TT    h   h   e              WW WW     AA   AA  KK  KK   EEEE  MM     MM  AA   AA  N  N   SSS
#
#
#

