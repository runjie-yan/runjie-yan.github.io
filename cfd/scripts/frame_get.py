import cv2
import os
import numpy as np
import imageio
from PIL import Image
# Example usage
input_teaser = './assets/videos/head_teaser/cat.mp4'
output_teaser = './assets/videos/head_teaser/cat.png'
# get 240 frame of input teaser, save to output teaser, cut 1024*1024
cap = cv2.VideoCapture(input_teaser)
i = 0
print("start")
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        print("Can't receive frame (stream end?). Exiting...")
        break
    if i == 225:
        print("250 frame")
        # cut 1024*1024
        frame = frame[0:1024, 0:1024]
        
        cv2.imwrite(output_teaser, frame)
        break
    i += 1
cap.release()
cv2.destroyAllWindows()