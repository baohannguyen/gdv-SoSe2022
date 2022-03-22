import numpy as np
import cv2
# Dasselbe wie in tut03 aber nur mit einer Video-Datei
# open a video file
file = "videos/hello_UH.m4v"
# Zugriff auf die Video-Datei
cap = cv2.VideoCapture(file)

# get camera image parameters from get()
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width, height)

# start a loop
while True:
    # (in loop) read one video frame
    ret, frame = cap.read()

# (in loop) create four tiles of the image
    if(ret):
        img = np.zeros(frame.shape, np.uint8)

#  (in loop) show the image
        cv2.imshow("Video", img)
    else:
        print("Could not get the video")
        break
# TODO (in loop) close the window and stop the loop if 'q' is pressed
    if cv2.waitKey(10) == ord("q"):
        break
# TODO release the video and close all windows
