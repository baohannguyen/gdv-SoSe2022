# Edge detection on an example image

from cv2 import CAP_OPENNI_GRAY_IMAGE
import numpy as np
import cv2

from GDV_tutorial_14 import T_lower, T_upper


def show_images_side_by_side(img_A, img_B):
    '''Helper function to draw two images side by side'''
    cv2.imshow(window_name, np.concatenate((img_A, img_B), axis=1))


# TODO: Define callback function
def change(val):
    # callback function für die trackbar
    '''callback function for the sliders'''
    # read slider positions
    blur_position = cv2.getTrackbarPos("Blur: ", window_name)
                                    # (Trackbarname, Fenstername)
    # damit krieg man die trackbar position raus
    kernel_size = (blur_position, blur_position)
    T_lower = cv2.getTrackbarPos("T_lower: ", window_name)
    T_upper = cv2.getTrackbarPos("T_upper: ", window_name)

    # blur the image
    img = cv2.blur(img_clone, kernel_size)
    # run Canny edge detection with thresholds set by sliders
    canny_img = cv2.Canny(img, T_lower, T_upper)
    # (Bild, lower wert, upper wert)
    # show the resulting images in one window
    show_images_side_by_side(img, canny_img)


# TODO load example image as grayscale
img = cv2.imread("images\\nl_clown.jpg", cv2.IMREAD_GRAYSCALE)
# resize if needed
img = cv2.resize(img, (500, 500))
# clone if needed
img_clone = np.copy(img)

# TODO initial Canny edge detection result creation
T_lower = 40
T_upper = 250
canny_img = cv2.Canny(img, T_lower, T_upper)


# TODO create window with sliders
# define a window name
window_name = 'Canny edge detection demo Tutorial'
# TODO show the resulting images in one window
show_images_side_by_side(img, canny_img)
# TODO create trackbars (sliders) for the window and define one callback function
cv2.createTrackbar("Blur: ", window_name, 0, 100, change)
cv2.createTrackbar("T_lower: ", window_name, 0, 200, change)
cv2.createTrackbar("T_upper: ", window_name, 0, 200, change)


# wait until a key is pressed and end the application
cv2.waitKey(0)
cv2.destroyAllWindows()
