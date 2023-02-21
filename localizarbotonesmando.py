#Importamos evdev
from evdev import InputDevice, categorize, ecodes

#Creamos el objecto gamepad
gamepad = InputDevice('/dev/input/event2')

#Muestra la info del gamepad
print(gamepad)

#Muestra los codigos
for event in gamepad.read_loop():
    #Botones 
    if event.type == ecodes.EV_KEY:
        print(event)
    #Joystick
    elif event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        print(ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)
