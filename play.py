import cv2
import numpy as np
import time

width =1280
height = 820

cam = cv2.VideoCapture(0)
cam.set(3,width)
cam.set(4,height)
# give the camera to warm up
time.sleep(1)
count = 0
back_ground = 0

for i in range(60):
    return_val, back_ground = cam.read()
    if return_val == False:
        continue

back_ground = np.flip(back_ground, axis=1)  # flipping of the frame

while (cam.isOpened()):
    return_val, img = cam.read()
    if not return_val:
        break
    count = count + 1
    img = np.flip(img, axis=1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])
    mask1 = cv2.inRange(hsv, lower_blue, upper_blue)
    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])
    mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3),
                                                            np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(back_ground, back_ground, mask=mask1)
    res2 = cv2.bitwise_and(img, img, mask=mask2)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow("magic frame", final_output)
    k = cv2.waitKey(10)
    if k == 27:
        break
