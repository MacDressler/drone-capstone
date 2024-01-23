import cv2
import numpy as np
import cv2.aruco as aruco
import inspect
from os.path import join
import argparse
import imutils
import matplotlib.pyplot as plt

def we_are_here():
    return os.getcwd()

fullPath = inspect.getfile(we_are_here)
shortPathIndex = fullPath.rfind("/")
if (shortPathIndex == -1):
    # handle Windows paths
    shortPathIndex = fullPath.rfind("\\")
Path = fullPath[0:shortPathIndex]
picturesPath = join(Path, "Aruco_board.png")
image=cv2.imread(picturesPath)


# aruco_dict=aruco.Dictionary_get(aruco.DICT_6X6_250)
#aruco_dict=aruco.Dictionary_get(aruco.DICT_4X4_50)
aruco_dict_list=[
cv2.aruco.DICT_4X4_50,
 cv2.aruco.DICT_4X4_100,
 cv2.aruco.DICT_4X4_250,
 cv2.aruco.DICT_4X4_1000,
 cv2.aruco.DICT_5X5_50,
 cv2.aruco.DICT_5X5_100,
 cv2.aruco.DICT_5X5_250,
 cv2.aruco.DICT_5X5_1000,
 cv2.aruco.DICT_6X6_50,
cv2.aruco.DICT_6X6_100,
 cv2.aruco.DICT_6X6_250,
 cv2.aruco.DICT_6X6_1000,
 cv2.aruco.DICT_7X7_50,
 cv2.aruco.DICT_7X7_100,
 cv2.aruco.DICT_7X7_250,
 cv2.aruco.DICT_7X7_1000,
 cv2.aruco.DICT_ARUCO_ORIGINAL,
 cv2.aruco.DICT_APRILTAG_16h5,
 cv2.aruco.DICT_APRILTAG_25h9,
 cv2.aruco.DICT_APRILTAG_36h10,
 cv2.aruco.DICT_APRILTAG_36h11
]


# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i",picturesPath, required=True,
# 	help="path to input image containing ArUCo tag")
# args = vars(ap.parse_args())

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

ARUCO_DICT1={"DICT_6X6_250": cv2.aruco.DICT_6X6_250}

# load the input image from disk and resize it
print("[INFO] loading image...")
image = cv2.imread(picturesPath)
image = imutils.resize(image, width=600)
# loop over the types of ArUco dictionaries
for (arucoName, arucoDict) in ARUCO_DICT.items():
	# load the ArUCo dictionary, grab the ArUCo parameters, and
	# attempt to detect the markers for the current dictionary
	arucoDict = cv2.aruco.Dictionary_get(arucoDict)
	arucoParams = cv2.aruco.DetectorParameters_create()
	(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)
	#print(corners,ids,rejected)
	print(corners,ids)
	# if at least one ArUco marker was detected display the ArUco
	# name to our terminal
	if len(corners) > 0:
		print("[INFO] detected {} markers for '{}'".format(
			len(corners), arucoName))




# allocate memory for the output ArUCo tag and then draw the ArUCo
# # tag on the output image
# #print("[INFO] generating ArUCo tag type '{}' with ID '{}'".format(
# #  # 	args["type"], args["id"]))
# tag = np.zeros((300, 300, 1), dtype="uint8")
# cv2.aruco.drawMarker(aruco.Dictionary_get(aruco.DICT_6X6_250), 16, 300, tag, 1)
# # write the generated ArUCo tag to disk and then display it to our
# # screen
# # cv2.imwrite(args["output"], tag)
# cv2.imshow("ArUCo Tag", tag)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# b, g, r = cv2.split(image)
# image = cv2.merge([r, g, b])
# plt.imshow(tag)
# plt.show()

aruco_dict=aruco.Dictionary_get(aruco_dict_list[5])
aruco_parameters=aruco.DetectorParameters_create()

# verify *at least* one ArUco marker was detected
if len(corners) > 0:
	# flatten the ArUco IDs list
	ids = ids.flatten()
	# loop over the detected ArUCo corners
	for (markerCorner, markerID) in zip(corners, ids):
		# extract the marker corners (which are always returned in
		# top-left, top-right, bottom-right, and bottom-left order)
		corners = markerCorner.reshape((4, 2))
		(topLeft, topRight, bottomRight, bottomLeft) = corners
		# convert each of the (x, y)-coordinate pairs to integers
		topRight = (int(topRight[0]), int(topRight[1]))
		bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
		bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
		topLeft = (int(topLeft[0]), int(topLeft[1]))
# draw the bounding box of the ArUCo detection
		cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
		cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
		cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
		cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
		# compute and draw the center (x, y)-coordinates of the ArUco
		# marker
		cX = int((topLeft[0] + bottomRight[0]) / 2.0)
		cY = int((topLeft[1] + bottomRight[1]) / 2.0)
		cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
		# draw the ArUco marker ID on the image
		cv2.putText(image, str(markerID),
			(topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 255, 0), 2)
		print("[INFO] ArUco marker ID: {}".format(markerID))
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

def draw_markers(dictionary,img):
    arucoDict = cv2.aruco.Dictionary_get(dictionary)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
    if ids is None:
        return False
    for (markerCorner, markerID) in zip(corners, ids):
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        #draw the corners
        cv2.line(img, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 2)
        # marker
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
        # draw the ArUco marker ID on the image
        cv2.putText(img, str(markerID),
        (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

dico= cv2.aruco.DICT_4X4_1000

