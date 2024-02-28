from pyparrot.Minidrone import Mambo

mamboAddr = None

mambo = Mambo(mamboAddr, use_wifi = True)

print("Trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s")

if(success):
    print("sleeping")
    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)

    print("taking off")
    mambo.safe_takeoff(5)

    if(mambo.sensors.flying_state!= "emergency"):

        success = mambo.flip(direction="left")
        mambo.smart_sleep(5)
        mambo.fly_direct(roll = 0, pitch = 0, yaw = 0, vertical_movement= 50, duration = 0.1)
        print("landing")
        print("flying state is %s")
        mambo.safe_land(5)
        mambo.smart_sleep(5)


print("disconnect")
mambo.disconnect()