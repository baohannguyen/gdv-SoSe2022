import cv2
import math
import operator

# capture webcam image
cap = cv2.VideoCapture(0)

# get camera image parameters from get()
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
codec = int(cap.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT))
# Werte werden auf dem Terminal ausgegeben
print(width, height, codec)

# create helper variables for drawing and writing text
# thickness
thick = 10
thin = 3

# color
blue = (255, 0, 0)
red = (0, 0, 255)
green = (20, 200, 20)
black = (0, 0, 0)

# fonts
font_large = 3
font_small = 1
# normal size sans serif font
font = cv2.FONT_HERSHEY_SIMPLEX

# create a function and a timer variable for the moving rectangle
# def steht für eine Funktion


def circle_path(t, scale, offset):
    res = (int(scale*math.cos(t)+offset), int(scale*math.sin(t)+offset))
    return res


timer = 0.0

#  start a loop
while True:

    #  (in loop) capture the image
    # Zugriff auf die Kamera
    ret, img = cap.read()

#  (in loop) check if capture succeeded
    if (ret):

        # (in loop) draw a blue diagonal cross over the image
        img = cv2.line(img, (0, 0), (width, height), blue, thick)
        # (0, 0) = Startkoordinate (oben links)
        # (width, height) = unten rechts (Endkoordinate)
        # (x = width, y = height)
        img = cv2.line(img, (0, height), (width, 0), blue, thick)
        # (0, height) = unten links, (width, 0) = oben rechts

#  (in loop) draw a circle
        img = cv2.circle(img, (width-40, 40), 20, red, cv2.FILLED, cv2.LINE_4)
        # width - 40 = 600 = Mittelpunkt
        # 20 = Radius
        # FILLED = ausgefüllt, LINE_4 = 4-connected line
#  (in loop) write some text
        img = cv2.putText(img, "Hello", (10, height - 10),
                          font, font_large, black, thick)

#  (in loop) draw arrows
        img = cv2.arrowedLine(img, (10, 10), (100, 10), green, thin)
        img = cv2.putText(img, "X", (115, 25), font,
                          font_small, black, thin)
        img = cv2.arrowedLine(img, (10, 10), (10, 100), green, thin)
        img = cv2.putText(img, "Y", (5, 130), font,
                          font_small, black, thin)

# TODO (in loop) draw a rectangle that moves on a circular path
        timer += 0.1
        pt1 = circle_path(timer, 100, 300)
        size = (20, 20)
        pt2 = tuple(map(operator.add, pt1, size))
        # tuple funktioniert wie eine Liste
        # operator.add ist die Funktion
        img = cv2.rectangle(img, pt1, pt2, red, thin)

# (in loop) display the image
        cv2.imshow("Video", img)

# (in loop) press q to close the window
# 10 wegen 10 millisekunden
        if cv2.waitKey(10) == ord("q"):
            break
        else:
            print("Could not get the video")
            break

# release the video capture object and window
cap.release()
cv2.destroyAllWindows()
