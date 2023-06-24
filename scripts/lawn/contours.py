import numpy as np
import cv2

image = cv2.imread("lawn_1.jpg")
assert image is not None, "file could not be read, check with os.path.exists()"
imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
# visualize the binary image

cv2.imwrite("image_thres1.jpg", thresh)


# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
image_copy = image.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
cv2.imwrite('contours_none_image1.jpg', image_copy)

