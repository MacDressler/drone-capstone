from pyparrot.Minidrone import Mambo
import cv2
import inspect
from os.path import join

mambo = Mambo(None, use_wifi=True) #address is None since it only works with WiFi anyway
print("trying to connect to mambo now")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

def how_many_files_in_mambo(drone):
    picture_names = drone.groundcam.get_groundcam_pictures_names()
    return len(picture_names)


def save_picture(mambo_object,i,folderName,pictureName):

    # pic_success = mambo.take_picture()
    # print("picture",i)
    # picture_names = mambo_object.groundcam.get_groundcam_pictures_names()

    fullPath = inspect.getfile(save_picture)
    shortPathIndex = fullPath.rfind("/")
    if (shortPathIndex == -1):
        # handle Windows paths
        shortPathIndex = fullPath.rfind("\\")
    print(shortPathIndex)
    shortPath = fullPath[0:shortPathIndex]
    picturesPath = join(shortPath, folderName)
    filename_i="saved_file_"+str(i)+".jpg"
    storageFile_i = join(picturesPath, filename_i)
    print('Your Mambo groundcam files will be stored here',storageFile_i)

    if (mambo_object.groundcam.ftp is None):
        print("No ftp connection")

    # otherwise return the photos
    mambo_object.groundcam.ftp.cwd(mambo.groundcam.MEDIA_PATH)
    try:
        mambo_object.groundcam.ftp.retrbinary('RETR ' + pictureName, open(storageFile_i, "wb").write) #download


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

if (success):
    # get the state information
    print("sleeping")
    mambo.smart_sleep(1)
    mambo.ask_for_state_update()
    mambo.smart_sleep(1)
    mambo.safe_takeoff(5)

    for i in range(2):
        mambo.smart_sleep(1)

        #getting info inthe list
        picture_names_old = mambo.groundcam.get_groundcam_pictures_names()
        print("old pictures_names",picture_names_old)

        #doing one side of the squares
        print("Flying direct: roll")
        mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=1)
        print("Showing turning (in place) using turn_degrees")
        mambo.turn_degrees(90)

        #taking a picture
        pic_success = mambo.take_picture()
        print("picture",i)
        mambo.smart_sleep(0.5)

        picture_names = mambo.groundcam.get_groundcam_pictures_names()
        print(picture_names)

        #choosing the right frame and saving it

        picture_name_i=is_in_the_list(picture_names_old,picture_names)[1]
        print(picture_name_i)
        save_picture(mambo,i,"saved_pictures",picture_name_i)

    mambo.safe_land(5)

    print("disconnect")
    mambo.disconnect()

