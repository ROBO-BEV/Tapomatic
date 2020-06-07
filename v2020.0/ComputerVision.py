#!/usr/bin/env python
"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.mvp"
__company__ = "CocoTaps"
__status__  = "Development"
__date__    = "Late Updated: 2020-05-21"
__doc__     = "Script to analyze the size of coconuts, so that we make 99% reliable Tapomatic"
"""

# Useful standard Python system jazz
import sys, time, traceback, argparse, string

# OpenCV magic
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_table_of_contents_imgproc/py_table_of_contents_imgproc.html
import cv2
import numpy as np

# Create a command line parser
# parser = argparse.ArgumentParser(prog = "Tapomatic Computer Vision", description = __doc__, add_help=True)
# parser.add_argument("-f", "--filename", type=str, default="Update.py", help="Local or cloud software to be loaded on ki$
# parser.add_argument("-l", "--loop", type=int, default=0, help="Set to 1 to loop this driver program.")
# args = parser.parse_args()

##GUIDE TO BEGINNERS
##Treat the Image as a matrix and that is how computers see and store the images.
## [x,y]

class ComputerVision():
    def printImageForTestingPurpose(self, img):
        """
        Prams:Img to be printed
        :return: NA
        PRESS KEY TO PROCEED.
        """
        cv2.imshow('COCO IMAGE', img)
        cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
        if cv2.waitKey(0) == ord('q'):
            print('Done')
    
    def LoadImage(self, filename, mode):
        """
        Load a PNG image on the local harddrive into RAM
        
        Key arguments:
        filename -- PNG file to load into memory
        mode - 0 to read image in grayscale mode.
               1 to read image in rgb mode.
    
        Return value:
        img -- Image header object 
        """
        print("TODO: CHECK FOR >PNG?")
        path = "static/CVImages/" + filename
        print(" path " + path)
        img = cv2.imread(path, mode) #0 for black, 1 for rgb
        return img

    def FindScale(self):
        """
        Find the ruler or object in background that define scale between pixel and real life size
    
        """
        print("TODO: Very hard")


    def IncreaseContrast(self, image, percentage):
        """
        Create new image object with increased contrast to make edge dection easier
        
        Key arguments:
        image -- 
        percentage -- ??? TODO Blaze please read the following explanation and let me know new arguments suitable for this function.
        Image Contrast and Brightness can be formulated like the following.
        g(x) = af(x)+b  where f(x) is the old image and g(x) is the new image.
        To increase the contrast, multiply each pixel by constant a (GAIN) and add a
        constant b (BIAS). To increase the contrast choose a > 1 and to decrease choose a < 1

        """
        # copyImage  = [ [0...0][0...0][0...0][0...0]]
        # copyImage = np.zeros(image.shape, image.dtype) # dtype is the data type ex:int
        # newImg = loop x,y,c (old_image) * a + b

        a = 1.5 #[1.0..3.0] Responsible for Contrast #TODO GET PARAMS
        b = 35  #[0.. 100]  Responsible for Brightness #TODO GET PARAMS
        newImg = cv2.convertScaleAbs(image, alpha=a, beta=b)
        return newImg

    def ConvertToBW(self,colorImage):
        """
        Convert image to Black & White to make processing faster and more discrete

        Key arguments:
        image -- 
        
        Return value:
        bwImg -- Black & White image header object 
        
        """

        grayImg = cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY)
        self.printImageForTestingPurpose(grayImg)
        ## Input 1st Param Image
        # 2nd Param : Threshold, if the pixel is less than this, value will be 0 (black) or set to 3rd param (white)
        #Usually coconuts are close to white, set this to > 200. so that they convert to black
        (threshold, bwImg) = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY)
        self.printImageForTestingPurpose(bwImg)
        return bwImg

    def FindSideToSideEdges(self, bwImage):
        """
        Scan image left to right and find two mostly vertical lines
        
        Key arguments:
        bwImage -- Black & White image to analyze
        
        Return value:
        columnList -- Two item list holding equation for a line
        """
        
        columnList = ["y=100/98x-420", "y=-100/97+690"]     # Temp List
        return columnList

    def FindTopToBottomEdges(self, bwImage):
        """
        Scan image top to bottom and find two mostly horizontal lines
        
        Key arguments:
        bwImage -- Black & White image to analyze
        
        Return value:
        rowList -- Two item list holding equation for a line
        """
        
        rowList = ["y=1/98x-69", "y=-1/97+70"]     # Temp List        
        return rowList

    def MeasurePixels(self, edge1, edge2):
        """
    
        Return values:
        numOfPixels -- Number of pixels between two nearly perpendicular lines
        """


        return numOfPixels

if __name__ == "__main__":
    object = ComputerVision()
    # The CV flow should probably be done in the following order
    ##TODO Remove this later, only testing purposes loading images statically here.
    filename = "coco_1.jpg"
    img = object.LoadImage(filename, 1)
    ##TODO REMOVE LATER, Will open loaded images in a seperate window.
    object.printImageForTestingPurpose(img)

    ##TODO COMMENT UNTIL MURALI GET SOME CLARITY FROM BLAZE ON WHAT TO DO.
    #scale = FindScale(filename)  #TODO HARD

    contrastColorImg = object.IncreaseContrast(img, 100) ##TODO BLAZE, SEE MY EXPLANATION
    ##TODO Remove later Testing Purpose Only.
    object.printImageForTestingPurpose(contrastColorImg)

    ##Convert TO Black and White.
    bwImg = object.ConvertToBW(img)
    ##TODO Remove later Testing Purpose Only.
    object.printImageForTestingPurpose(bwImg)

    columnList = object.FindSideToSideEdges(bwImg)
    # columnList[1] = edge1
    #  columnList[2] = edge2
    # sideToSidePixels = object.MeasurePixels(edge1, edge2)
    # coconutWidth = object.ConvertToLength(scale, sideToSidePixels)
        
    # rowList = FindTopToBottomEdges(bwImage)
    # rowList[1] = edge1
    # rowList[2] = edge2
    # topToBottomPixels = MeasurePixels(edge1, edge2)
    # coconutHeight = ConvertToLength(scale, topToBottomPixels)
