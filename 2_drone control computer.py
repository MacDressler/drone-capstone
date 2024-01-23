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

def marker_id(dictionary,image):
    arucoDict = cv2.aruco.Dictionary_get(dictionary)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)
    if  ids is None:
        return None
    if len(ids)>2:
        if ids[0]<ids[1]:
            return ids[1]
    return ids[0]


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

def do_action_fpv(mambo_vision,s,explored):
    #○take picture with FPV camera
    dico=cv2.aruco.DICT_6X6_250
    uservision=UserVision(mambo_vision)
    imgfpv=uservision.vision.get_latest_valid_picture()
    filenamefpv='picture'+str(s)+'.png'
    markerfpv=marker_id(dico,imgfpv)
    draw_markers(dico,imgfpv)
    detected=False

    #search the action to do with the FPV picture according to the detected marker

    if markerfpv==106:
        s=s+1
        explored.append(markerfpv)
        filenamefpv='picture'+str(markerfpv)+'.png'
        cv2.imwrite(filenamefpv,imgfpv)
        file_source=join(we_are_here(),filenamefpv)
        file_destination=get_path(filenamefpv)
        shutil.move(file_source, file_destination)
        mambo.smart_sleep(1)
        mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=0.5)
        detected=True
        return detected

    if markerfpv==89:
        s=s+1
        filenamefpv='picture'+str(markerfpv)+'.png'
        cv2.imwrite(filenamefpv,imgfpv)
        file_source=join(we_are_here(),filenamefpv)
        file_destination=get_path(filenamefpv)
        shutil.move(file_source, file_destination)
        mambo.smart_sleep(1)
        mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=0.5)
        detected=True
        return detected

    if markerfpv==148:
        s=s+1
        filenamefpv='picture'+str(markerfpv)+'.png'
        cv2.imwrite(filenamefpv,imgfpv)
        file_source=join(we_are_here(),filenamefpv)
        file_destination=get_path(filenamefpv)
        shutil.move(file_source, file_destination)
        mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=0.5)
        mambo.smart_sleep(1)
        mambo.turn_degrees(-90)
        mambo.safe_land(5)
        detected=True
        return detected

    if markerfpv==4 and (explored[len(explored)-1]!=4 and explored[len(explored)-1]!=1 and explored[len(explored)-1]!=2 and explored[len(explored)-1]!=16):
        s=s+1
        explored.append(markerfpv)
        filenamefpv='picture'+str(markerfpv)+'.png'
        cv2.imwrite(filenamefpv,imgfpv)
        file_source=join(we_are_here(),filenamefpv)
        file_destination=get_path(filenamefpv)
        shutil.move(file_source, file_destination)
        mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=0.5)
        mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=0, duration=0.4)
        mambo.smart_sleep(1)
        mambo.turn_degrees(-90)
        detected=True
        return detected

    if detected==False:
        mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=0.3)
        return("No relevant markers")

def do_action_gc(mambo_vision,s,explored):
    detected=False
    dico=cv2.aruco.DICT_6X6_250
    picture_names_old = mambo.groundcam.get_groundcam_pictures_names()
    pic_success = mambo.take_picture()
    print("picture")
    mambo.smart_sleep(0.5)
    picture_names_new = mambo.groundcam.get_groundcam_pictures_names()
    picture_name=is_in_the_list(picture_names_old,picture_names_new)[1]
    filenamegc='picture'+str(s)+'.png'
    imggc = mambo.groundcam.get_groundcam_picture(picture_name,True)
    markergc=marker_id(dico,imggc)
    draw_markers(dico,imggc)

    if markergc==0 or markergc==135:
        s=s+1
        filenamegc='picture'+str(markergc)+'.png'
        cv2.imwrite(filenamegc,imggc)
        file_source=join(we_are_here(),filenamegc)
        file_destination=get_path(filenamegc)
        shutil.move(file_source, file_destination)
        mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=0, duration=0.5)
        detected=True
        return detected

    if markergc==7 :
        s=s+1
        explored.append(markergc)
        filenamegc='picture'+str(markergc)+'.png'
        cv2.imwrite(filenamegc,imggc)
        file_source=join(we_are_here(),filenamegc)
        file_destination=get_path(filenamegc)
        shutil.move(file_source, file_destination)
        mambo.fly_direct(roll=0, pitch=-50, yaw=0, vertical_movement=0, duration=0.4)

        detected=True
        return detected

    if (markergc==1 or markergc==2 or markergc==16) and (explored[len(explored)-1]!=4 and explored[len(explored)-1]!=1 and explored[len(explored)-1]!=2 and explored[len(explored)-1]!=16):
        s=s+1
        explored.append(markergc)
        filenamefpv='picture'+str(markergc)+'.png'
        cv2.imwrite(filenamegc,imggc)
        file_source=join(we_are_here(),filenamegc)
        file_destination=get_path(filenamegc)
        shutil.move(file_source, file_destination)
        mambo.smart_sleep(1)
        mambo.turn_degrees(-90)
        mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=0.5)
        if markergc==16:
            mambo.safe_land(5)

        detected=True
        return detected

    # if markergc==148:
    #     s=s+1
    #     filenamegc='picture'+str(markergc)+'.png'
    #     cv2.imwrite(filenamegc,imggc)
    #     file_source=join(we_are_here(),filenamegc)
    #     file_destination=get_path(filenamegc)
    #     shutil.move(file_source, file_destination)
    #     mambo.safe_land(5)
    #     detected=True
    #     return detected

    return False



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
            c=0
            s=0
            explored=[-1]
            #type exit to land
            while c<20:
                c=c+1
                print("Etape",c)
                do_action_fpv(mamboVision,s,explored)
                do_action_gc(mamboVision,s,explored)
                if do_action_fpv(mamboVision,s,explored) is True:
                    s=s+1
                print(s)
                print("explored is",explored)
                mambo.smart_sleep(2)



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