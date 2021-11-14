import imutils
import numpy as np
import cv2
import constants
import numberIdentifier


def getSurface(approx):
    points = get4Points(approx)  # points: [[minX, minY], [maxX, minY], [maxX, maxY], [minX, maxY]]
    return (points[1][0] - points[0][0]) * (points[2][1] - points[0][1])


def get4Points(approx):
    (minX, maxX, minY, maxY) = numberIdentifier.getContainersMinMaxPoints(approx)
    return np.array([[minX, minY], [maxX, minY], [maxX, maxY], [minX, maxY]])


def getSurfaceMachRat(surface1, surface2):
    try:
        if surface1 < surface2:
            return surface1 / surface2
        return surface2 / surface1
    except:
        return 0


def plateFinder(img, original):
    img = imutils.resize(img, width=constants.widthOfNewImage)
    original = imutils.resize(original, width=constants.widthOfNewImage)
    img = cv2.blur(img, (7, 7), 1000)

    _, threshold = cv2.threshold(img, 50, 60, cv2.THRESH_BINARY_INV)
    cannyImage = cv2.Canny(threshold, 40, 50)
    contours = cv2.findContours(cannyImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    cntrRect = []

    for contour in contours:

        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if (len(approx) == 4 or
            (getSurfaceMachRat(getSurface(approx), cv2.contourArea(contour)) > 0.7 and
             len(approx) >= 4)) \
                and cv2.contourArea(contour) > constants.minSurfaceAreaOfLicencePlate:
            if getSurfaceMachRat(getSurface(approx), cv2.contourArea(contour)) > 0.5:
                cntrRect.append(get4Points(contour))
                original = cv2.drawContours(original, cntrRect, -1, constants.colorOfLicencePlate, 2)

                numbers = numberIdentifier.numberIdentifier(cntrRect, original, contour)
                return numbers



