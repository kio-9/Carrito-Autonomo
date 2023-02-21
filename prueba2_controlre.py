import asyncio
import time
from evdev import InputDevice, categorize, ecodes
import numpy as np
#CENTER_TOLERANCE = 350
#STICK_MAX = 65536

'''
axis = {
    ecodes.ABS_X: 'ls_x', # 0 - 65,536   the middle is 32768
    ecodes.ABS_Y: 'ls_y',
    ecodes.ABS_Z: 'rs_x',
    ecodes.ABS_RZ: 'rs_y',
    ecodes.ABS_BRAKE: 'lt', # 0 - 1023
    ecodes.ABS_GAS: 'rt',

    ecodes.ABS_HAT0X: 'dpad_x', # -1 - 1
    ecodes.ABS_HAT0Y: 'dpad_y'
}

center = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

last = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

for event in dev.read_loop():

    # calibrate zero on Y button
    if event.type == ecodes.EV_KEY:
        if categorize(event).keycode[0] == "BTN_WEST":
            center['ls_x'] = last['ls_x']
            center['ls_y'] = last['ls_y']
            center['rs_x'] = last['rs_x']
            center['rs_y'] = last['rs_y']
            print( 'calibrated' )

    #read stick axis movement
    elif event.type == ecodes.EV_ABS:
        if axis[ event.code ] in [ 'ls_x', 'ls_y', 'rs_x', 'rs_y' ]:
            last[ axis[ event.code ] ] = event.value

            value = event.value - center[ axis[ event.code ] ]

            if abs( value ) <= CENTER_TOLERANCE:
                value = 0

            if axis[ event.code ] == 'rs_x':
                if value < 0:
                    print('left')
                else:
                    print('right')
                print( value )

            elif axis[ event.code ] == 'ls_y':
                if value < 0:
                    print('foreward')
                else:
                    print('backward')
                print( value )
'''
class Controller:
    #Como las variables de python no admiten numeros usamos letras
    xBtn = 304
    cuadrado_Btn = 307
    triangulo_Btn = 308
    circulo_Btn = 305
    l1_Btn=310
    r1_Btn=311
    back_Btn=314
    Start_Btn=315

    def __init__(self, debug=False):
        self.connected = False
        for i in range(20):
            try:
                self.gamepad = InputDevice(f'/dev/input/event{i}')
                print(self.gamepad.name)
                if 'Gamepad' in self.gamepad.name:
                    break
            except:
                if i == 19:
                    print('Mando no conectado')
                    return
        self.debug = debug
        #Muestra la info del gamepad
        print(self.gamepad)
        self.connected = True

    def obtener_comando(self):
       opt = None
       while not opt:
           opt, val = self.leer_mando()
       return opt, val

#while True:
    def leer_mando(self):
       comando=''
       Vel=0
       event= None
       #Muestra los codigos
       t=time.time()
       while event is None:
          event = self.gamepad.read_one()
          if time.time()-t > 2:
             return None, -999 
             break 
   #i+=1
   #time.sleep(0.05)
   #print (i)
       if event is None:
           return None,None
       else:
       #Botones
           if event.type == ecodes.EV_KEY:
               #print(event)
               if event.value == 1:
                   if event.code == self.xBtn:
                       if self.debug:
                           print("X,status")
                       comando='p'
                   elif event.code == self.cuadrado_Btn:
                       if self.debug:
                           print("cuadrado, 1")
                       Vel = 1
                       comando='1'
                   elif event.code == self.triangulo_Btn:
                       if self.debug:
                           print("triangulo, 2")
                       comando='2'
                   elif event.code == self.circulo_Btn:
                       if self.debug:
                           print("circulo, 3")
                       Vel = -1
                       comando='3'
                   elif event.code == self.l1_Btn:
                       if self.debug:
                           print("salir")
                       comando='q'
                   elif event.code == self.r1_Btn:
                       if self.debug:
                           print("DERECHA, fin")
                       comando='f'
                   elif event.code == self.back_Btn:
                       if self.debug:
                           print("teleoperado")
                       comando='t'
                   elif event.code == self.Start_Btn:
                       if self.debug:
                           print("AUTONOMO")
                       comando='y'
               #elif event.value == 0:
                 #print("Suelto")

       #Joystick
           elif event.type == ecodes.EV_ABS:
               absevent = categorize(event)
               #print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
               if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Z":
                    if absevent.event.value <= 128:
                       Vel= round(-1*absevent.event.value*35/128+70)
                       if self.debug:
                           print("Izquierda",Vel)
                       comando='a'
                    elif absevent.event.value > 128:
                       Vel= round((absevent.event.value-128)*-35/127+35)
                       if self.debug:
                           print("Derecha",Vel)
                       comando='d'
               elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
                    if absevent.event.value <=122 :
                       Vel = round(absevent.event.value*-3.6/122+6.6,2)
                       comando='w'
                       if self.debug:
                           print("Avanza",Vel)
                       #print(absevent.event.value)
                    elif absevent.event.value >= 132:
                       Vel = round(-3+(-1*absevent.event.value+132)*3.6/123,2);
                       comando='x'
                       if self.debug:
                           print("RETROCEDE",Vel)
                       #print(absevent.event.value)
                    else:
                       Vel=0
                       comando='x' #no es x pero funciona
                       if self.debug:
                           print("NO HACE NADA",Vel)
                       #print("centrado")

               if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0X":
                    if absevent.event.value == -1:
                       if self.debug:
                           print("Izquierda, cámara")
                       comando='c'
                    elif absevent.event.value == 1:
                       if self.debug:
                           print("Derecha, gps")
                       comando='g'
                    else:
                       comando='' #no deberia ser a pero funciona
                       if self.debug:
                           print("Centrado") 
               elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0Y":
                    if absevent.event.value == -1:
                       if self.debug:
                           print("Arriba")
                    elif absevent.event.value == 1:
                       if self.debug:
                           print("Abajo, imu")
                       comando='i'
                    else:
                       comando='' #no deberia ser a pero funciona
                       if self.debug:
                           print("Centrado") 
       return comando,Vel

   #time.sleep(0.1)

