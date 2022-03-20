# first step is to import the opencv module which is called 'cv2'
import cv2
from cv2 import ROTATE_90_CLOCKWISE
from cv2 import ROTATE_180
from cv2 import ROTATE_90_COUNTERCLOCKWISE
# check the opencv version
print(cv2.__version__)
# TODO load an image with image reading modes using 'imread'
# cv2.IMREAD_UNCHANGED  - If set, return the loaded image as is (with alpha
#                         channel, otherwise it gets cropped). Ignore EXIF
#                         orientation.
# cv2.IMREAD_GRAYSCALE  - If set, always convert image to the single channel
#                         grayscale image (codec internal conversion).
# cv2.IMREAD_COLOR      - If set, always convert image to the 3 channel BGR
#                         color image.
img = cv2.imread("images/logo.png", cv2.IMREAD_COLOR)
# in der Klammer werden die Werte eingegeben (Name des Bildes)
height = 300
width = 200
newSize = (height, width)
img = cv2.resize(img, newSize)
# Bild bekommt eine neue Größe

img = cv2.rotate(img, ROTATE_90_COUNTERCLOCKWISE)
# Bild wird um 90 Grad rotiert

# img = cv2.imwrite()

# TODO resize image with 'resize'

# rotate image (but keep it rectangular) with 'rotate'

# TODO save image with 'imwrite'

# show the image with 'imshow'
title = "GDV-Turotial"
# Fenster wird erstellt
cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
# gibt den Namen und die Größe des Fensters aus

cv2.imshow(title, img)

cv2.waitKey(0)
cv2.destroyAllWindows()
