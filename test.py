import cv2
import numpy as np

img_gray = cv2.imread()
img_color = cv2.imread()
# damit kann man Bilder auslesen lassen

img_color = cv2.resize(img_color, new_size)
# die größe wird in integer gespeichert und nicht in float deswegen immer davor in integer casten

print(type(img_color))
print(img_color.shape)
# speichert jedem pixel im bild als bgr
array = np.array([[1, 1, 1], [2, 2, 2]])
# so wird ein array gespeichert

img_color[:, :, 0] = np.zeros([img_color.shape[0], img_color.shape[1]])

cv2.imshow("title", img_color)
cv2.waitKey(0)