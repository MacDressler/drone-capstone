import cv2
import numpy as np
import cv2.aruco as aruco
import inspect
from os.path import join
import argparse
import imutils
import matplotlib.pyplot as plt
from random import *

#
# for i in range(5):
#     j=randint(0,249)
#     print(j)
#     tag = np.zeros((300, 300, 1), dtype="uint8")
#     cv2.aruco.drawMarker(aruco.Dictionary_get(aruco.DICT_6X6_250),j, 300, tag, 1)
# # write the generated ArUCo tag to disk and then display it to our
# # screen
#     cv2.imshow("ArUCo Tag", tag)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


tag = np.zeros((300, 300, 1), dtype="uint8")
cv2.aruco.drawMarker(aruco.Dictionary_get(aruco.DICT_6X6_250),8, 300, tag, 1)
cv2.imshow("ArUCo Tag", tag)
cv2.waitKey(0)
cv2.destroyAllWindows()