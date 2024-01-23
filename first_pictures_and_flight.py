#just take off, acess the list of pictures inside the mambo, take a picture, re access to the picture list and then display a random picture. No selected picture no saved picture
from pyparrot.Minidrone import Mambo
import cv2

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

    #acces to the picture

    picture_names = mambo.groundcam.get_groundcam_pictures_names() #get list of availible files
    #print(picture_names)
    print("There were",len(picture_names),"pictures in the list")


    mambo.smart_sleep(1)

    # take the photo
    pic_success = mambo.take_picture()

    # need to wait a bit for the photo to show up
    mambo.smart_sleep(0.5)


    picture_names = mambo.groundcam.get_groundcam_pictures_names()
    print(picture_names)
    print("Now there are",len(picture_names), "pictures in the list")

    #display the last picture on the screen
    if picture_names==[]:
        print("There is no picture now")

    else:
        frame = mambo.groundcam.get_groundcam_picture(picture_names[len(picture_names)-1],True) #get frame which is the first in the array



    if frame is not None:
        if frame is not False:
            cv2.imshow("Groundcam", frame)
            cv2.waitKey(100)

    print(mambo.sensors.altitude)
    mambo.smart_sleep(1)

    mambo.safe_land(5)
    mambo.disconnect()