import time
import cv2
import imutils
import constants
import findGeometricalShapes


def creatImageMask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, constants.lower_red, constants.upper_red)
    return mask


def getImage(rawImage):
    rawImage = imutils.resize(rawImage, width=constants.widthOfNewImage)
    maskImage = creatImageMask(rawImage)
    numbers = findGeometricalShapes.plateFinder(maskImage, rawImage)
    return numbers
