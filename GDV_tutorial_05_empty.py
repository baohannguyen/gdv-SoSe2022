import cv2
import math
import operator

# capture webcam image
cap = cv2.VideoCapture(0)

# get camera image parameters from get()
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
codec = int(cap.get(cv2.cv2.CAP_PROP_CODEC_PIXEL_FORMAT))
print(width, height, codec)

# TODO create helper variables for drawing and writing text
# thickness
thick = 10
thin = 3

# color
blue = (255, 0, 0)
red = (0, 0, 255)
black = (0, 0, 0)

# fonts
font_large = 3
font_small = 1
# normal size sans serif font
font = cv2.FONT_HERSHEY_SIMPLEX

# TODO create a function and a timer variable for the moving rectangle


# def steht für eine Funktion
def circle_path(t, scale, offset):
    res = (int(scale*math.cos(t) + offset), int(scale*math.sin(t) + offset))
    return res


timer = 0.0

# TODO start a loop
while True:

    # TODO (in loop) capture the image
    ret, img = cap.read()

# TODO (in loop) check if capture succeeded
    if (ret):

        # TODO (in loop) draw a blue diagonal cross over the image
        img = cv2.line(img, (0, 0), (width, height), blue, thick)
        img = cv2.line(img, (0, height), (width, 0), blue, thick)

# TODO (in loop) draw a circle
        img = cv2.circle(img, (width-40, 40), 20, red, cv2.FILLED, cv2.LINE_4)
        # FILLED = ausgefüllt, LINE_4 = 4-connected line
# TODO (in loop) write some text
        img = cv2.putText(img, "Hello", (10, height - 10),
                          font, font_large, black, thick)

# TODO (in loop) draw arrows
        img = cv2.arrowedLine(img, (10, 10), (100, 10), black, thin)
        img = cv2.putText(img, "X", (115, 25), font,
                          font_small, black, thin)
        img = cv2.arrowedLine(img, (10, 10), (100, 10), black, thin)
        img = cv2.putText(img, "Y", (5, 130), font,
                          font_small, black, thin)

# TODO (in loop) draw a rectangle that moves on a circular path
    timer += 0.1
    pt1 = circle_path(timer, 100, 300)
    size = (20, 20)
    pt2 = tuple(map(operator.add, pt1, size))
    img = cv2.rectangle(img, pt1, pt2, red, thin)

# TODO (in loop) display the image
    cv2.imshow("Video", img)

# TODO (in loop) press q to close the window
    if cv2.waitKey(10) == ord("q"):
        break
    else:
        print("Could not get the video")
        break

# TODO release the video capture object and window
cap.release()
cv2.destroyAllWindows()
