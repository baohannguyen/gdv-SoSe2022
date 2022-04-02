import numpy as np
import cv2

# capture webcam image
cap = cv2.VideoCapture(0)
# Indesx 0 ist Standard für Laptops; Zugriff auf die Webcam
# 0 heißt auch das nur auf einer Kamera zugegriffen wird
# get camera image parameters from get()
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width, height)

# create a window for the video
title = "Video-Webcam"
cv2.namedWindow(title, cv2.WINDOW_FREERATIO)
# mit freeratio kann man die Größe beliebig ändern
# start a loop
while True:
    # (in loop) read a camera frame and check if that was successful
    ret, frame = cap.read()
    if (ret):
        # (in loop) create four flipped tiles of the image
        img = np.zeros(frame.shape, np.uint8)
        # uint8 = unsigned integer 8-Bits = Typ des Arrays
        # np.zeros füllt das Array mit der Zahl 0
        # Bild ist dann von Anfang an schwarz
# (in loop) display the image
# Bild wird immer wieder angezeigt bis man auf "q" klickt
        cv2.imshow(title, frame)
    else:
        print("Could not get video frame")
        break

# (in loop) press q to close the window and exit the loop
    if cv2.waitKey(10) == ord("q"):
        break

# TODO release the video capture object and window
cap.release()
cv2.destroyAllWindows()
