import cv2
import numpy as np
import cv2.aruco as aruco
import inspect
from os.path import join
import argparse
import imutils
import matplotlib.pyplot as plt
from random import *
from pyparrot.Minidrone import Mambo
from pyparrot.DroneVisionGUI import DroneVisionGUI
import os
import shutil


def we_are_here():
    return os.getcwd()

def get_path(filename):
    fullPath = inspect.getfile(we_are_here)
    shortPathIndex = fullPath.rfind("/")
    if (shortPathIndex == -1):
        # handle Windows paths
        shortPathIndex = fullPath.rfind("\\")
    Path = fullPath[0:shortPathIndex]
    picturesPath = join(Path, filename)
    return picturesPath

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        # print("in save pictures on image %d " % self.index)

        img = self.vision.get_latest_valid_picture()

        if (img is not None):
            filename = "test_image_%06d.png" % self.index
            # uncomment this if you want to write out images every time you get a new one
            #cv2.imwrite(filename, img)
            self.index +=1
            #print(self.index)


def find_marker(id,dictionary,image):
    arucoDict = cv2.aruco.Dictionary_get(dictionary)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)
    print(ids)
    if ids is None:
        return False
    for i in range(len(ids)):
        if ids[i][0]==id:
            print("Marker is in the picture")
            return True
    print("Marker is not is the picture")
    return False

def draw_markers(dictionary,img):
    arucoDict = cv2.aruco.Dictionary_get(dictionary)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
    if ids is None:
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
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

def save_picture(mambo_object,pictureName,filename):


    fullPath = inspect.getfile(we_are_here)
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

def is_in_the_list(l1,l2):
    for i in range(min(len(l1),len(l2))):
        if l1[i]!=l2[i]:
            return [i,l2[i]]
    return [len(l2)-1,l2[len(l2)-1]]

def do_action(action,mambo_vision,s):
    dico=cv2.aruco.DICT_6X6_250
    if action=="w":
        print("Drones will go forward")
        mambo.fly_direct(roll=0, pitch=20, yaw=0, vertical_movement=0, duration=0.25)

    if action=="a":
        print("Drones will go backward")
        mambo.fly_direct(roll=0, pitch=-20, yaw=0, vertical_movement=0, duration=0.25)

    if action=="s":
        print("Drones will go left")
        mambo.fly_direct(roll=-20, pitch=0, yaw=0, vertical_movement=0, duration=0.25)

    if action=="d":
        print("Drones will go right")
        mambo.fly_direct(roll=20, pitch=0, yaw=0, vertical_movement=0, duration=0.25)

    if action=="W":
        print("Drones will go up")
        mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=20, duration=0.25)

    if action=="A":
        print("Drones will go down")
        mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-20, duration=0.25)

    if action=="S":
        print("Drones will turn right")
        mambo.turn_degrees(30)

    if action=="D":
        print("Drones will turn left")
        mambo.turn_degrees(-30)

    if action=="z":
        uservision=UserVision(mambo_vision)
        img=uservision.vision.get_latest_valid_picture()
        filename='picture'+str(s)+'.png'
        cv2.imshow(filename,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if action=="Z":
        uservision=UserVision(mambo_vision)
        img=uservision.vision.get_latest_valid_picture()
        filename='picture'+str(s)+'.png'
        draw_markers(dico,img)
        cv2.imwrite(filename,img)
        file_source=join(we_are_here(),filename)
        file_destination=get_path(filename)
        shutil.move(file_source, file_destination)

    if action=="c":
        picture_names_old = mambo.groundcam.get_groundcam_pictures_names()
        pic_success = mambo.take_picture()
        print("picture")
        mambo.smart_sleep(0.5)
        picture_names_new = mambo.groundcam.get_groundcam_pictures_names()
        picture_name=is_in_the_list(picture_names_old,picture_names_new)[1]
        filename='picture'+str(s)+'.png'
        frame = mambo.groundcam.get_groundcam_picture(picture_name,True)
        cv2.imshow("Groundcam", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if action=="C":
        picture_names_old = mambo.groundcam.get_groundcam_pictures_names()
        pic_success = mambo.take_picture()
        print("picture")
        mambo.smart_sleep(0.5)
        picture_names_new = mambo.groundcam.get_groundcam_pictures_names()
        picture_name=is_in_the_list(picture_names_old,picture_names_new)[1]
        filename='picture'+str(s)+'.png'
        save_picture(mambo,picture_name,filename)
        mambo.smart_sleep(1)
        picturePath=get_path(filename)
        img=cv2.imread(picturePath)
        draw_markers(dico,img)
        cv2.imwrite(filename,img)
        file_source=join(we_are_here(),filename)
        file_destination=get_path(filename)
        shutil.move(file_source, file_destination)


# creating a MAMBO object
#We will use Wifi for this session, modify use_wifi to make it possible to use Wifi
testFlying=True
def demo_mambo_user_vision_function(mamboVision, args):
    """
    Demo the user code to run with the run button for a mambo

    :param args:
    :return:
    """
    mambo = args[0]

    if (testFlying):
        print("taking off!")
        mambo.safe_takeoff(5)

        if (mambo.sensors.flying_state != "emergency"):
            action=input("What do you want to do ?")
            c=0
            s=0
            #type exit to land
            while action!='exit':
                c=c+1
                print("Etape",c)
                do_action(action,mamboVision,s)
                if action=="Z" or action=="C":
                    s=s+1
                action=input("What do you want to do ?")


        print("landing")
        print("flying state is %s" % mambo.sensors.flying_state)
        mambo.safe_land(5)
    else:
        print("Sleeeping for 15 seconds - move the mambo around")
        mambo.smart_sleep(15)

    # done doing vision demo
    print("Ending the sleep and vision")
    mamboVision.close_video()

    mambo.smart_sleep(5)

    print("disconnecting")
    mambo.disconnect()




if __name__ == "__main__":

    # make my mambo object
    # remember to set True/False for the wifi depending on if you are using the wifi or the BLE to connect
    mambo = Mambo(None, use_wifi=True)
    print("trying to connect to mambo now")
    success = mambo.connect(num_retries=3)
    print("connected: %s" % success)

    if (success):
        # get the state information
        print("sleeping")
        mambo.smart_sleep(1)
        mambo.ask_for_state_update()
        mambo.smart_sleep(1)

        print("Preparing to open vision")
        mamboVision = DroneVisionGUI(mambo, is_bebop=False, buffer_size=200,
                                     user_code_to_run=demo_mambo_user_vision_function, user_args=(mambo, ))
        userVision = UserVision(mamboVision)
        mamboVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
        mamboVision.open_video()
