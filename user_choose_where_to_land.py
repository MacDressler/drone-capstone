#this program take photo and display it to the user (display the ritgh one) ant then ask to the user if he wants to land or not. Does it 5 times and then land. Does not save the pictures taken.
from pyparrot.Minidrone import Mambo
import cv2

#student can code this function as an exercise
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
    #mambo.safe_takeoff(5)
    c=0
    ans='n'
    potential_landing_places=[]

    while c<5 and ans!='y':
        #upload the list before the photo has been taken
        picture_names = mambo.groundcam.get_groundcam_pictures_names()
        print('Old lenght is',len(picture_names))

        # take the photo
        pic_success = mambo.take_picture()

        # need to wait a bit for the photo to show up
        mambo.smart_sleep(0.5)


        #upload the new list after the picture
        picture_names_new = mambo.groundcam.get_groundcam_pictures_names()#essential to reload it each time; does not update automaticaly
        print("New lenght is",len(picture_names_new))

        #finding the new picture in the list
        index=is_in_the_list(picture_names, picture_names_new)
        potential_landing_places.append(index[1])


        frame = mambo.groundcam.get_groundcam_picture(potential_landing_places[c],True)
        #print(picture_names)
        #print("last on the list is", picture_names[len(picture_names)-1])


        if frame is not None:
            if frame is not False:
                cv2.imshow("Groundcam", frame)
                cv2.waitKey(4000)
                cv2.destroyAllWindows()

        #mambo.smart_sleep(1)

        ans=input("Would you like to land ? Type y or n : ")
        c=c+1
        print(c,ans)


    #mambo.safe_land(5)
    print("landed")
    mambo.disconnect()