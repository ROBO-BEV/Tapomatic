import numpy as np
import matplotlib.pyplot as plt 
from scipy import signal
from scipy import misc
import scipy

from matplotlib.pyplot import imread



def Generte_Masks(sigma,T):
    '''
    A method for generating Gaussian Derivative Filters.
    Arguments
    
    sigma: Standard Deviation of Gaussian
    T:     (T>=0.5) Threshold the gaussian for selecting 
            a finite segment of gaussian
    
    '''
    assert sigma>=0.5
    #Calculating Size of Filter By threshholding the value of Gaussian at T
    half_size=np.round(np.sqrt(-np.log(T)*2*sigma**2))
    size=half_size*2+1
    
    
    
    normal = 1 / (2.0 * np.pi * sigma**2)
    # Creating X and Y axis
    x, y = np.mgrid[-half_size:half_size+1, -half_size:half_size+1]
    
    # Creating Filters
    g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal 
    Gx =  (-x/(sigma**2))*np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    Gy =  (-y/(sigma**2))*np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    # Scaling by 255
    Gx=np.round(Gx*255)
    Gy=np.round(Gy*255)
    
    return Gx,Gy


def rgb2gray(rgb):
    '''
    A method for converting RGB to Gray scale
    '''
    
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


def hysteresis(img, TI, TH):
    '''
    An Implementation of hysteresis By getting iterating over all pixels
    which have values equal or greater than TI and its aat leat one from 
    eight neighbours is greater than TH.
    It is recursive because I am updating same Image.
    ARGUMENTS:
    img: input Image
    TI:  lower threshold
    TH:  upper threshold
    
    '''
    M, N = img.shape 
    for i in range(1, M-1):
        for j in range(1, N-1):
            if ((img[i,j] >= TI) and (img[i,j] < TH)):
                try:
                    if ((img[i+1, j-1] >= TH) or (img[i+1, j] >= TH) or (img[i+1, j+1] >= TH)
                        or (img[i, j-1] >= TH) or (img[i, j+1] >= TH)
                        or (img[i-1, j-1] >= TH) or (img[i-1, j] >= TH) or (img[i-1, j+1] >= TH)):
                        
                        img[i, j] = max( img[i+1, j-1]  , img[i+1, j]   , img[i+1, j+1], img[i, j-1] ,
                                         img[i, j+1]    , img[i-1, j-1] ,img[i-1, j]  ,img[i-1, j+1] )
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img















