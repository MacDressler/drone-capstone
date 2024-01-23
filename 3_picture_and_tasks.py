#Useful module importation
import cv2
import numpy as np
import imutils
#colors
from webcolors import rgb_to_name,CSS3_HEX_TO_NAMES,hex_to_rgb #python3 -m pip install webcolors
from scipy.spatial import KDTree
from pyparrot.Minidrone import Mambo
import inspect
from os.path import join
import numpy as np





def is_red_here(picturepath):
    image=cv2.imread(picturepath)
    mask1 = cv2.inRange(image, (0, 0, 50), (50, 50,255))
    number_of_white_pix = np.sum(mask1== 255)
    print(number_of_white_pix)
    if number_of_white_pix!=0:
        return True
    else:
        return False

def is_blue_here(picturepath):
    image=cv2.imread(picturepath)
    mask1 = cv2.inRange(image, (50, 0, 0), (255, 50,50))
    # cv2.imshow("groundcam",mask1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    number_of_white_pix = np.sum(mask1== 255)
    print(number_of_white_pix)
    if number_of_white_pix!=0:
        return True
    else:
        return False


def get_path(picturename):
    #we assume that the file is in the same folder as this file
    fullPath = inspect.getfile(is_red_here)
    shortPathIndex = fullPath.rfind("/")
    if (shortPathIndex == -1):
        # handle Windows paths
        shortPathIndex = fullPath.rfind("\\")
    #print(shortPathIndex)
    shortPath = fullPath[0:shortPathIndex]
    filename=picturename
    storageFile = join(shortPath, filename)
    return storageFile


#Class Shapedetector
class ShapeDetector:
    def __init__(self):
        pass
    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        #print(len(approx))
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) ==3:
            shape = "triangle"
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
        elif len(approx) == 6:
            shape = "hexagon"
        elif len(approx) == 10:
            shape = "star"
        elif len(approx) == 12:
            shape="cross"
            #print("it's a cross")
        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"
        # return the name of the shape
        return shape



def is_cross_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="cross":
            return True
    return False

def is_square_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="square" or shape=="rectangle":
            return True
    return False

def draw_contour(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cv2.imshow("cross_edge",edge_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    contours,_=cv2.findContours( edge_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        cv2.drawContours(image, [contour], 0, (0, 0, 255), 5)
    cv2.imshow("cross_edge_contours",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def is_red_cross_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,200,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        #print(shape)
        if shape=="cross":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (0, 0, 50), (50, 50,255))
            print(mask1[pts[0][0]][pts[1][0]])

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow("cross",image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False

def is_green_cross_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,200,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        #print(shape)
        if shape=="cross":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (0, 50, 0), (50, 255,50))
            print(mask1[pts[0][0]][pts[1][0]])
            print(image[pts[0][100]][pts[1][100]])

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow("cross",image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False

def is_blue_cross_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        #print(shape)
        if shape=="cross":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (50, 0, 0), (255, 50,50))
            print(mask1[pts[0][0]][pts[1][0]])
            print(len(pts[0]))
            print(len(pts[1]))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow("cross",image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False


def is_blue_hexagon_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        #print(shape)
        if shape=="hexagon":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (50, 0, 0), (255, 50,50))
            # print(mask1[pts[0][0]][pts[1][0]])
            # print(len(pts[0]))
            # print(len(pts[1]))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        print(image[pts[0][i]][pts[1][j]])
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow(shape,image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False

def is_blue_square_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        #print(shape)
        if shape=="square" or shape=="rectangle":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (50, 0, 0), (255, 50,50))
            print(mask1[pts[0][0]][pts[1][0]])
            # print(len(pts[0]))
            # print(len(pts[1]))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow(shape,image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False


def is_red_square_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        #print(shape)
        if shape=="square" or shape=="rectangle":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (0, 0, 50), (50, 50,255))
            print(mask1[pts[0][0]][pts[1][0]])
            print(len(pts[0]))
            print(len(pts[1]))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow(shape,image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False

def is_red_triangle_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="triangle":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (0, 0, 50), (50, 50,255))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow(shape,image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False



def save_picture(mambo_object,pictureName,filename):


    fullPath = inspect.getfile(is_red_here)
    shortPathIndex = fullPath.rfind("/")
    if (shortPathIndex == -1):
        # handle Windows paths
        shortPathIndex = fullPath.rfind("\\")
    print(shortPathIndex)
    shortPath = fullPath[0:shortPathIndex]
    # filename="marker.jpg"
    storageFile = join(shortPath, filename)
    print('Your Mambo groundcam files will be stored here',storageFile)

    if (mambo_object.groundcam.ftp is None):
        print("No ftp connection")

    # otherwise return the photos
    mambo_object.groundcam.ftp.cwd(mambo.groundcam.MEDIA_PATH)
    try:
        mambo_object.groundcam.ftp.retrbinary('RETR ' + pictureName, open(storageFile, "wb").write) #download


    except Exception as e:
        print('error')

#student can code this function as an exercise
#l1=l0old
#l2=lnew
def is_in_the_list(l1,l2):
    for i in range(min(len(l1),len(l2))):
        if l1[i]!=l2[i]:
            return [i,l2[i]]
    return [len(l2)-1,l2[len(l2)-1]]


mambo = Mambo(None, use_wifi=True) #address is None since it only works with WiFi anyway
print("trying to connect to mambo now")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

if (success):
    # get the state information
    print("sleeping")
    mambo.smart_sleep(1)
    mambo.ask_for_state_update()
    mambo.smart_sleep(1)
    mambo.safe_takeoff(5)


    #get list of all the files stored inside the Mambo
    picture_names_old = mambo.groundcam.get_groundcam_pictures_names()

    #taking a picture
    pic_success = mambo.take_picture()
    print("picture")
    mambo.smart_sleep(0.5)

    #get list of all the files stored inside the Mambo
    picture_names_new = mambo.groundcam.get_groundcam_pictures_names()

    #get the right picture
    picture_name=is_in_the_list(picture_names_old,picture_names_new)[1]
    filename=input("Filename ?")

    save_picture(mambo,picture_name,filename)
    mambo.smart_sleep(1)
    picturePath=get_path(filename)
    draw_contour(picturePath)

    c=0

    #processing the picture
    if is_red_cross_here(picturePath):
        print("There is a red cross in this picture ")
        c=c+1
    if is_green_cross_here(picturePath):
        print("There is a green cross in this picture ")
        c=c+1

    if is_red_square_here(picturePath):
        print("There is red square or rectangle in this picture")
        c=c+1

    if is_blue_cross_here(picturePath):
        print("There is a blue cross in this picture ")
        c=c+1

    if is_blue_square_here(picturePath):
        print("There is a blue square or rectangle in this picture")
        c=c+1

    if is_red_triangle_here(picturePath):
        print("There is a red triangle is this picture")
        c=c+1


    if c==0:
        print("Impossible to determine what is on this picture")
        #mambo.flip(direction='left')

    mambo.safe_land(5)

print("disconnect")
mambo.disconnect()


