from math import atan, pi
import imutils
import numpy as np
import cv2
import constants
import recognize_digits


def numberIdentifier(approx, image, originalContour):
    warped = cropImg(image, approx)
    warped = cv2.resize(warped, constants.imageSize)
    ang = findObjectAngle(originalContour)
    warped = imutils.rotate(warped, ang)
    changeColors = cv2.bitwise_not(warped)
    gray = cv2.cvtColor(changeColors, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray, constants.thresholdThresh, constants.thresholdMaxval, 0)
    contours, _ = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cleanContours = []
    for contour in contours:
        (w, h) = getWidthHeight(contour)
        if (w <= constants.numberMaxWidth) \
                and \
                (h <= constants.numberMaxHeight):
            cleanContours.append(contour)
    cleanContours = cleanObjectInObject(cleanContours)
    foundNumbers = []
    for contour in cleanContours:
        (w, h) = getWidthHeight(contour)
        if cv2.contourArea(contour) > constants.numberMinSurfaceArea and \
                (w <= constants.numberMaxWidth) and \
                (constants.numberMinHeight <= h <= constants.numberMaxHeight):
            number, location, height = recognize_digits.getNumbers(contour, contours)
            foundNumbers.append([location, number, height])
    foundNumbers.sort()
    foundNumbers = checkForAverageHeight(foundNumbers)
    return extract(foundNumbers)


# clean to high objects in photo
def checkForAverageHeight(listOfNumbers):
    if len(listOfNumbers) > 0:
        avg = [item[2] for item in listOfNumbers]
        avg = sum(avg) / len(listOfNumbers)
        output = []
        for item in listOfNumbers:
            if avg - constants.numberHeightDelta < item[2] < avg + constants.numberHeightDelta:
                output.append(item)
        return output
    return listOfNumbers


# crop image by the
def cropImg(image, approx):
    minX, maxX, minY, maxY = getContainersMinMaxPoints(approx[0])
    cropped = image[minY:maxY, minX:maxX]
    return cropped


# return the width and the height of an object
def getWidthHeight(contour):
    minX, maxX, minY, maxY = getContainersMinMaxPoints(contour)
    return maxX - minX, maxY - minY


# extract the first value of list in lists
def extract(lst):
    return [item[1] for item in lst]


# return min/max x,y points of the object (rectangle 4 total)
def getContainersMinMaxPoints(approx):
    x = []
    y = []
    for i in range(len(approx)):
        if len(approx[i]) > 1:
            (tempX, tempY) = (approx[i])
        else:
            (tempX, tempY) = (approx[i][0])
        x.append(tempX)
        y.append(tempY)
    return min(x), max(x), min(y), max(y)


# if there is a object inside it will delete it
def cleanObjectInObject(approx):
    newApprox = []
    for i in range(len(approx)):
        tempList = approx
        np.delete(tempList, i)
        if not (checkObIinObj(approx[i], tempList)):
            newApprox.append(approx[i])
    return newApprox


# if there is an object inside
def checkObIinObj(obj, approx):
    objMinX, objMaxX, objMinY, objMaxY = getContainersMinMaxPoints(obj)
    for approxObj in approx:
        approxObjMinX, approxObjMaxX, approxObjMinY, approxObjMaxY = getContainersMinMaxPoints(approxObj)
        if (approxObjMinX < objMinX < approxObjMaxX) and (approxObjMinX < objMaxX < approxObjMaxX):
            if (approxObjMinY < objMinY < approxObjMaxY) and (approxObjMinY < objMaxY < approxObjMaxY):
                return True
    return False


def findObjectAngle(contour):
    minX, maxX, minY, maxY = getContainersMinMaxPoints(contour)
    y1 = []
    y2 = []
    angle = 0
    for obj in contour:
        if (minX - constants.rotationDeltaX) <= obj[0][0] <= (minX + constants.rotationDeltaX):
            y1.append(obj[0][1])
        if maxX - constants.rotationDeltaX <= obj[0][0] <= maxX + constants.rotationDeltaX:
            y2.append(obj[0][1])
    if (abs(max(y1) - min(y1))/(maxY-minY) < constants.minRotationSize) and\
            (abs(max(y1) - min(y1))/(maxY-minY) < constants.minRotationSize):
        if min(y1) < min(y2):
            angle = (min(y1) - minY) / (maxX - minX)
        if min(y1) > min(y2):
            angle = -(min(y2) - minY) / (maxX - minX)
    else:
        angle = 0
    angle = atan(angle) * 180 / pi

    return angle
