
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

    #acces to the pictures files

    picture_names = mambo.groundcam.get_groundcam_pictures_names() #get list of availible files
    print(picture_names)
    print(len(picture_names))

    #reset the memory of the mambo
    if picture_names!=[]:
        for i in range(len(picture_names)):
            filename=picture_names[i]
            mambo.groundcam._delete_file(filename)

    #chek if the pictures were deleted
    picture_names = mambo.groundcam.get_groundcam_pictures_names() #get list of availible files
    print(picture_names)
    print(len(picture_names))

    mambo.smart_sleep(1)

    # take the photo
    pic_success = mambo.take_picture()
    print("picture")


    # need to wait a bit for the photo to show up
    mambo.smart_sleep(2)


    #display the picture on the screen
    picture_names = mambo.groundcam.get_groundcam_pictures_names() #get list of availible files
    print(picture_names)
    print(len(picture_names))
    frame = mambo.groundcam.get_groundcam_picture(picture_names[0],True) #get frame which is the first in the array



    if frame is not None:
        if frame is not False:
            cv2.imshow("Groundcam", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()



    mambo.disconnect()
