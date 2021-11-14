import numpy as np

# licencePlateIdentifier
lower_red = np.array([17, 70, 100])
upper_red = np.array([35, 255, 255])
widthOfNewImage = 700

# recognize_digits
boxYSize = 4
boxXToRight = 4
boxXToLeft = 3
boxTopSize = 1
oneLeftRatio = 0.5  # max 1, lower value is less sensitive higher is more.
oneRightRatio = 0.9  # max 1, lower value is more sensitive higher is less.
zeroInnerObjRatio = 0.5  # max 1, lower value is more sensitive higher is less.
sevenBottomLeftPositionRatio = 0.3  # max 1, lower value is less sensitive higher is more.
sevenBottomRightPositionRatio = 0.5  # max 1, lower value is more sensitive higher is less.
fourBottomLeftPositionRatio = 0.2  # max 1, lower value is less sensitive higher is more.
fourBottomRightPositionRatio = 0.7  # max 1, lower value is less sensitive higher is more.
treeLeftPoPositionRatio = 0.5  # max 1, lower value is more sensitive higher is less.
fiveUpperPoPositionRatio = 0.7  # max 1, lower value is more sensitive higher is less.

# numberIdentifier
imageSize = (200, 100)
thresholdThresh = 170
thresholdMaxval = 250
numberHeightDelta = 10  # lower value is less sensitive higher is more.
numberMinSurfaceArea = 100  # lower value is less sensitive higher is more.
numberMaxWidth = 100  # lower value is more sensitive higher is less.
numberMinHeight = 20  # lower value is less sensitive higher is more.
numberMaxHeight = 77  # lower value is more sensitive higher is less.
minRotationSize = 0.5  # max 1, lower value is less sensitive higher is more.
rotationDeltaX = 0  # lower value is less sensitive higher is more.

# findGeometricalShapes
colorOfLicencePlate = (0, 255, 0)
minSurfaceAreaOfLicencePlate = 700
