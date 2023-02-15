from evdev import InputDevice, categorize, ecodes
gamepad = InputDevice('/dev/input/event5')
 
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY and event.value == 1:
        try:
            keyevent = categorize(event)
            print (keyevent) # comment to remove key messages
 
        except:
            print ("Problem key pressed...")
