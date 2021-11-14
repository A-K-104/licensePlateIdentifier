import cv2
import numpy as np
import constants
import findGeometricalShapes
import numberIdentifier


def getNumbers(approx, contours):
    x = []
    y = []
    for i in range(len(approx)):
        tempX, tempY = (approx[i][0])
        x.append(tempX)
        y.append(tempY)
    maxY = max(y)
    minX = min(x)
    minY = min(y)
    maxX = max(x)
    pointsOnBottom = []
    pointsOnRight = []
    pointsOnLeft = []
    pointsOnTop = []
    for i in range(len(approx)):
        if maxY - constants.boxYSize <= y[i] <= maxY:
            pointsOnBottom.append(maxX - x[i])
        if maxX - constants.boxXToRight <= x[i] <= maxX:
            pointsOnRight.append(approx[i])
        if minX + constants.boxXToLeft >= x[i] >= minX:
            pointsOnLeft.append(approx[i])
        if minY + constants.boxTopSize >= y[i] >= minY:
            pointsOnTop.append(approx[i])
    pointsOnRight = np.array(pointsOnRight)
    pointsOnLeft = np.array(pointsOnLeft)
    pointsOnTop = np.array(pointsOnTop)
    insideObjs = checkObjInside(approx, contours)
    (lMinX, lMaxX, lMinY, lMaxY) = numberIdentifier.getContainersMinMaxPoints(pointsOnLeft)
    (rMinX, rMaxX, rMinY, rMaxY) = numberIdentifier.getContainersMinMaxPoints(pointsOnRight)
    # if there are 2 objects inside it's 8
    if len(insideObjs) == 2:
        return 8, maxX, maxY - minY
    # if there are 1 objects inside it's 0/9/6
    if len(insideObjs) == 1:
        return checkObjNumberByInsideObj(insideObjs[0], approx), maxX, maxY - minY
    # if the max left delta height is over value and the right delta height is close to 1
    if ((lMaxY - lMinY) / (maxY - minY) < constants.oneLeftRatio) and\
            (rMaxY - rMinY) / (maxY - minY) > constants.oneRightRatio:
        return 1, maxX, maxY - minY
    # test the lower part and if there are only in the bottom left it's 7
    if (min(pointsOnBottom) / (maxX - minX) >= constants.sevenBottomLeftPositionRatio) and (
            max(pointsOnBottom) / (maxX - minX) >= constants.sevenBottomRightPositionRatio):
        return 7, maxX, maxY - minY
    # test the lower part and if there are only in the bottom right it's 4
    if (min(pointsOnBottom) / (maxX - minX) < constants.fourBottomLeftPositionRatio) and (
            max(pointsOnBottom) / (maxX - minX) < constants.fourBottomRightPositionRatio):
        return 4, maxX, maxY - minY
    # test the right part and if almost all filled it's 3
    if cv2.contourArea(pointsOnRight) / findGeometricalShapes.getSurface(
            pointsOnRight) > constants.treeLeftPoPositionRatio:
        return 3, maxX, maxY - minY
    # test the upper part and if almost all filled it's 5
    if cv2.contourArea(pointsOnTop) / findGeometricalShapes.getSurface(
            pointsOnTop) > constants.fiveUpperPoPositionRatio:
        return 5, maxX, maxY - minY
    return 2, maxX, maxY - minY
    # return '#', maxX, maxY-minY


# checks how many objects are inside the object
def checkObjInside(obj, approx):
    objMinX, objMaxX, objMinY, objMaxY = numberIdentifier.getContainersMinMaxPoints(obj)
    listOfItemsInside = []
    for approxObj in approx:
        approxObjMinX, approxObjMaxX, approxObjMinY, approxObjMaxY = numberIdentifier.getContainersMinMaxPoints(
            approxObj)
        if (objMinX < approxObjMinX < objMaxX) and (objMinX < approxObjMaxX < objMaxX):
            if (objMinY < approxObjMinY < objMaxY) and (objMinY < approxObjMaxY < objMaxY):
                listOfItemsInside.append(approxObj)
    return listOfItemsInside


# checks the proportion difference if in range it's a 0
# if the difference is too big it check if it's on the upper or
# lower by that it's 9/6
def checkObjNumberByInsideObj(obj, parent):
    (objMinX, objMaxX, objMinY, objMaxY) = numberIdentifier.getContainersMinMaxPoints(obj)
    (parentMinX, parentMaxX, parentMinY, parentMaxY) = numberIdentifier.getContainersMinMaxPoints(parent)
    if ((objMaxY - objMinY) / (parentMaxY - parentMinY)) > constants.zeroInnerObjRatio:
        return 0
    objCenter = objMinY + (objMaxY - objMinY) / 2
    parentCenter = parentMinY + (parentMaxY - parentMinY) / 2
    if parentCenter > objCenter:
        return 9
    return 6
