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


# Create a command line parser
parser = argparse.ArgumentParser(prog = "Tapomatic Computer Vision", description = __doc__, add_help=True)
parser.add_argument("-f", "--filename", type=str, default="Update.py", help="Local or cloud software to be loaded on ki$
parser.add_argument("-l", "--loop", type=int, default=0, help="Set to 1 to loop this driver program.")
args = parser.parse_args()


def LoadImage(filename):
    """
    Load a PNG image on the local harddrive into RAM
    
    Key arguments:
    filename -- PNG file to load into memory
    
    Return value:
    img -- 
    """
    
    print("TODO: CHECK FOR >PNG?")
    path = "../static/images/" + fileName
    img = cv2.imread(path)
    return img
                                                                                
                                                                                
def FindScale():
    """
    Find the ruler or object in background that define scale between pixel and real life size
    
    """


def IncreaseContrast(image):
    """
    Increase contrast to make edge dection easier
    
    Key arguments:
    image --
    
    """


def ConvertToBW(colorImage):
    """
    Convert image to Black & White to make processing faster and more discrete
    
    """

def FindSideToSideEdges(bwImage):
    """
    
    """
    

def FindTopToBottomEdges(bwImage):
    """
    
    """


def MeasurePixels(edge1, edge2):
    """
    
    Return values:
    numOfPixels -- Number of pixels between two nearly perpendicular lines
    """


    return numOfPixels

    
if __name__ == "__main__":

    # The CV flow should probably be done in the following order
    img = LoadImage(filename)
    
    scale = FindScale(filename)  #TODO HARD

    contrastColorImg = IncreaseContrast(image)
    bwImg = ConvertToBW(contrastColorImg)

    columnList = FindSideToSideEdges(bwImg)
    columnList[1] = edge1
    columnList[2] = edge2    
    sideToSidePixels = MeasurePixels(edge1, edge2)
    coconutWidth = ConvertToLength(scale, sideToSidePixels)
    
    rowList = FindTopToBottomEdges(bwImage)
    rowList[1] = edge1
    rowList[2] = edge2    
    topToBottomPixels = MeasurePixels(edge1, edge2)
    coconutHeight = ConvertToLength(scale, topToBottomPixels)
