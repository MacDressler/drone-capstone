from pyparrot.Minidrone import Mambo

mamboAddr = None

mambo = Mambo(mamboAddr, use_wifi = True)

print("Trying to connect")
success = mambo.connect(num_retries = 3)
print("connected: %s" %success)

if (success):
    print("sleeping")
    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)
    print("disconnect")
    mambo.disconnect()