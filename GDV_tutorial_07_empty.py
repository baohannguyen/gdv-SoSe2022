import cv2
import numpy as np

# Goal: Count the number of green smarties in the images
# define green in HSV
hue = 60  # 60 is pure green
hue_range = 10
saturation = 155
saturation_range = 100
value = 155
value_range = 100
lower_green = np.array([hue - hue_range, saturation -
                       saturation_range, value - value_range])
upper_green = np.array([hue + hue_range, saturation +
                       saturation_range, value + value_range])

# load image
img = cv2.imread('images\\smarties01.JPG', cv2.IMREAD_COLOR)
img = cv2.resize(img, (800, 600))

# convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# create a mask
mask = cv2.inRange(hsv, lower_green, upper_green)

# TODO morphological operations code


# die formen werden angelegt
def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE

# wissen wie es funktionieren soll


def erosion(img, shape, size):
    kernel: cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                      (size, size))
    return cv2.erode(img, kernel)
    # Methode gibt zwei Werte zurück (Bild & Kernel)


def dilation(img, shape, size):
    kernel: cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                      (size, size))
    return cv2.dilate(img, kernel)


def opening(img, shape, size):
    kernel: cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                      (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    # source, type of morph operation (opening), kernel
# TODO find connected components



# TODO go through all (reasonable) found connected components

# TODO (optional) check size and roundness as plausibility

# TODO find and draw center

# TODO find and draw bounding box

# print out number of connected components
print('We have found x green smarties.')


# show the original image with drawings in one window
cv2.imshow('Original image', img)
# show the masked image in another window

# show the mask image in another window
cv2.imshow('Mask image', mask)
# cv2.imwrite('mask.jpg',mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
