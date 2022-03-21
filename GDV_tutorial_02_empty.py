import numpy as np
import cv2


# TODO load images in grey and color
img_color = cv2.imread("images/logo.png", cv2.IMREAD_COLOR)
img_gray = cv2.imread("images/logo.png", cv2.IMREAD_GRAYSCALE)
img = img_gray

# TODO do some print out about the loaded data
print(type(img))
# dtype z.B uint8 (gibt die Daten aus)
print(img.dtype)
# gibt die Größe des Arrays aus
print(img.shape)
# print(img_gray)
# print(img_color)
# uint8 = unsigned integer 8bit

# TODO Continue with the color image or the grayscale image


# TODO Extract the size or resolution of the image

# TODO resize image

# TODO print first row

# TODO print first column

# TODO set an area of the image to black

# TODO find all used colors in the image
# all_rgb_codes = img.reshape(-1, img.shape[-1])
# print(all_rgb_codes)
# unique_rgb_codes = np.unique(all_rgb_codes, axis=0, return_counts=True)
# print(unique_rgb_codes)

# TODO copy one part of an image into another one
# : = von ... bis
letters = img[30:105, 5:130]
# Bild wird geschnitten
img[115:190, 150:275] = letters
# Bild wird hinzugefüt
# TODO save image

# TODO show the image
cv2.imshow("tutorial 2", img)
cv2.waitKey(0)
# TODO show the original image (copy demo)
# Fenster wird erstellt
# title = "GDV-Turotial 2"
# Hinweis zu title und Größe des Fensters wird hinzugefügt
# cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
# Bild wird angezeigt (Name des Fensters, das Bild)
# cv2.imshow(title, img_gray)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
