import numpy as np
import cv2

# print keyboard usage
print('This is a HSV color detection demo. Use the keys to adjust the \
selection color in HSV space. Circle in bottom left.')
print('The masked image shows only the pixels with the given HSV color within \
a given range.')
print('Use h/H to de-/increase the hue.')
print('Use s/S to de-/increase the saturation.')
print('Use v/V to de-/increase the (brightness) value.\n')

# capture webcam image
cap = cv2.VideoCapture(0)

# get camera image parameters from get()
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
codec = int(cap.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT))
print('Video properties:')
print('  Width = ' + str(width))
print('  Height = ' + str(height))
print('  Codec = ' + str(codec))

# drawing helper variables
thick = 10
thin = 3
thinner = 2
font_size_large = 3
font_size_small = 1
font_size_smaller = .6
font = cv2.FONT_HERSHEY_SIMPLEX


# define  RGB colors as variables
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# exemplary color conversion (only for the class), tests usage of cv2.cvtColor

# TODO enter found default values and uncomment
hue = 120
# ungefähr im Blau-Bereich
hue_range = 10
saturation = 200
saturation_range = 10
value = 200
# ist eher im hellen Bereich
value_range = 10


# implement the callback to pick the color on double click
# es wird was ausgerufen und man bekommt die Funktion zurück
def color_picker(event, x, y, flags, param):
    # mit dem color picker werden die Farbwerte ausgegeben
    global hue, saturation, value
    if event == cv2.EVENT_LBUTTONDBLCLK:
        (h, s, v) = hsv[y, x]
        hue = int(h)
        saturation = int(s)
        value = int(v)
        print('New color selected:', (hue, saturation, value))


while True:
    # get video frame (always BGR format!)
    ret, frame = cap.read()
    if (ret):
        # copy image to draw on
        img = frame.copy()

        # TODO draw arrows (coordinate system)

        # TODO computing color ranges for display
        lower_hue = hue - hue_range
        lower_saturation = saturation - saturation_range
        lower_value = value - value_range
        lower_bound = (lower_hue, lower_saturation, lower_value)
        upper_hue = hue + hue_range
        upper_saturation = saturation + saturation_range
        upper_value = value + value_range
        upper_bound = (upper_hue, upper_saturation, upper_value)

        # TODO draw selection color circle and text for HSV values

        # convert to HSV
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # BGR wird zu HSV konvertiert

        # create a bitwise mask
        # mask ist ein Teil/Abschnitt von dem Bild
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        # Maske sagt im Bild welche Pixel wir behalten sollen und welche nicht
        # Ein neues Bild/Abschnitt, wo nur die lower/upper bound
        # Pixel angezeigt werden

        # apply mask
        masked_lag = cv2.bitwise_and(img, img, mask=mask)
        # Eigentlich werden zwei Bilder vermischt und die Maske wird benutzt
        # um zu schauen welche Pixel man behalten soll und welche nicht
        # Aber in dem Fall werden die Bits in der Maske mit den Bits
        # in unserem Bild verglichen und die MAske sagt dann welche Pixel wir
        # behalten und welche nicht

        # show the original image with drawings in one window
        title = "Original Bild von der Kamera"
        cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
        cv2.setMouseCallback(title, color_picker)
        # Name des Fensters und die Funktion angeben
        cv2.imshow(title, img)

        # show the masked image in another window
        cv2.imshow("Maske", mask)

        # show the mask image in another window
        cv2.imshow("Maskes", masked_lag)

        # deal with keyboard input
        key = cv2.waitKey(10)
        if (key == ord("q")):
            break

    else:
        print('Could not start video camera')
        break

cap.release()
cv2.destroyAllWindows()
