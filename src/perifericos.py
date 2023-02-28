import cv2
import numpy as np
import serial
from threading import Thread
from queue import Queue
import time
import asyncio
from evdev import InputDevice, categorize, ecodes
import numpy as np

class Camara:
    cap = None

    def __init__(self, queueSize=128, size=(640, 480), segmentate=False):
        self.size = size
        self.segmentate = segmentate
        if self.__class__.cap is None:
            self.__class__.cap = cv2.VideoCapture(0)
            self.__class__.cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
            self.__class__.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
        self.camara = self.__class__.cap
        self.stopped = False
        self.flag_detec = None
        self.Q = Queue(maxsize=queueSize)
        self.Q_show = Queue(maxsize=queueSize)
        self.houghParams = [6,0.15,258]
        if self.camara is None or not self.camara.isOpened():
            raise ConnectionError

    def conectarCamara(self):
        for i in range(2):
            try:
                self.__class__.cap = cv2.VideoCapture(f'/dev/video{i}')
                print(f'Cámara conectada en el puerto {i}')
                break
            except:
                if i==1:
                    print('Cámara no conectada')
                    return False
        return True

    def getImgSize(self):
        return self.size

    def get_rtImg(self):
        _, frame = self.camara.read()
        return frame
    
    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                break
            if self.Q.full():
                continue
            _, frame = self.camara.read()
            if self.segmentate:
                frame= frame[int(frame.shape[0]*1/4):int(frame.shape[0]*3/4),:,:]
            self.Q.put(frame)
        self.camara.release()

    def read(self):
        return self.Q.get()

    def getFrames(self):
        if self.flag_detec is None:
           return self.read()
        else:
           return self.Q_show.get()

    def detectLines(self):
        t = Thread(target=self.detect, args=())
        self.flag_detec = True
        t.daemon = True
        t.start()
        return self

    def detect(self):
        while True:
            if self.stopped:
                break
            img = self.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Apply edge detection method on the image
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
            # This returns an array of r and theta values
            lines = cv2.HoughLines(edges, *self.houghParams)
            if lines is None:
                self.Q_show.put(img)
                continue
        
            # The below for loop runs till r and theta values
            # are in the range of the 2d array
            for r_theta in lines:
                r, theta = np.array(r_theta[0], dtype=np.float64)
                # Stores the value of cos(theta) in a
                a = np.cos(theta)
                # Stores the value of sin(theta) in b
                b = np.sin(theta)
                # x0, y0
                x0 = a*r
                y0 = b*r
                # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
                x1 = int(x0 + 1000*(-b))
                # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
                y1 = int(y0 + 1000*(a))
                # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
                x2 = int(x0 - 1000*(-b))
                # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
                y2 = int(y0 - 1000*(a))
        
                # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
                # (0,0,255) denotes the colour of the line to be
                # drawn. In this case, it is red.
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
            # All the changes made in the input image are finally
            # written on a new image houghlines.jpg
            self.Q_show.put(img)

    def stop(self):
        self.stopped = True

class Arduino:
    ser = None

    def __init__(self):
        if self.__class__.ser is None:
            self.__class__.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
        self.ser = self.__class__.ser


    def conectarArduino(self):
        for i in range(2):
            try:
                self.__class__.cap = serial.Serial(f'/dev/ttyUSB{i}', baudrate=115200)
                print(f'Arduino conectado en el puerto {i}')
                break
            except:
                if i==1:
                    print('Arduino no conectado')
                    return False
        return True

    def sendCommand(self, command):
        command = command+"\n"
        self.ser.write(command.encode('utf_8'))
        print(self.ser.readline().decode())

class Controller:

    def __init__(self, debug):     
        # Set buttons
        with open('botones.txt', 'r') as f:
            self.botones = {l.split(',')[1].rstrip():l.split(',')[0] for l in f}
        # Connect to controller
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
        self.connected = True
        self.stopped = False
        # Controller options
        self.debug = debug
        self.config = 'analog'
        self.ANGLES = [20, 30, 40, 50, 60]
        self.index = 2
        
    def obtener_comando(self):
        com = None
        while not com:
            com, val = self.leer_mando()
        return com, val

    def leer_mando(self):
        comando = ''
        vel = 0
        event = None
        t = time.time()
        # Read event
        while not event:
            event = self.gamepad.read_one()
            if time.time()-t > 2:
                return None, None
        # Parse event
        if event.type == ecodes.EV_KEY: # Buttons
            if event.value == 0: # Button released
                return None, None
            boton = self.botones.get(str(event.code), 'no c') 
            #print(boton)
            
            return self.__parseButton(boton)
        elif event.type == ecodes.EV_ABS: # Directional sticks
            absevent = categorize(event)
            return self.__parseJoystick(absevent)
        else:
            return None, None

    def __parseButton(self, boton):
        com = None
        
        if boton == 'x_Btn':
            com = '4'
        elif boton == 'cuadrado_Btn':
            com = '1'
        elif boton == 'triangulo_Btn':
            com = '2'
        elif boton == 'circulo_Btn':
            com = '3'
        elif boton == 'l1_Btn':
            com = 'q'
        elif boton == 'r1_Btn':
            self.index = 2
            return 'd', self.ANGLES[self.index]
        elif boton == 'back_Btn': 
            com = None
            self.index = 2
            self.config = 'incremental' if self.config=='analog' else 'analog'
            print(f'Configuración cambiada a {self.config}')
        elif boton == 'start_Btn':
            com = '1'
        else:
            print('Botón no mapeado')
            print(f'boton = {boton}')
        if self.debug:
            print(f'{boton}: {com}')
        return com, None

    def __parseJoystick(self, absevent):
        valor = absevent.event.value 
        evento = ecodes.bytype[absevent.event.type][absevent.event.code] 
        if evento == 'ABS_Z' and self.config == 'analog':
            return self.__angMapping(valor)
        elif evento == 'ABS_RZ' and self.config == 'incremental':
            return self.__velMapping(valor)
        elif evento == 'ABS_Y' and self.config == 'analog':
            return self.__velMapping(valor)
        elif evento == 'ABS_HAT0X' and self.config == 'incremental':
            return self.__angIncremental(valor)
        else:
            print('Comando no mapeado')
            return None, None

    def __angIncremental(self, valor):
        if valor == 0 or self.index-valor not in range(len(self.ANGLES)):
            return None, None
        self.index -= valor
        d = 'a' if valor<0 else 'd'
        if self.debug:
            print(f'{d}: {self.ANGLES[self.index]}')
        return d, self.ANGLES[self.index]

    def __angMapping(self, valor):
        if valor <= 128:
            ang = round(-valor*35/128+70)
            d = ('Izq', 'a')
        else:
            ang = round(-(valor-128)*35/127+35)
            d = ('Der', 'd')
        if self.debug:
            print(f'{d[0]}: {ang}')
        return d[1], ang

    def __velMapping(self, valor):
        if valor <= 122:
            vel = round(-valor*3.6/122+6.6, 2)
            d = ('Avanza', 'w')
        elif valor >= 132:
            vel = round(-3+(-valor+132)*3.6/123, 2)
            d = ('Retrocede', 'x')
        else:
            vel = 0
            d = ('Nada', 'w')
        if self.debug:
            print(f'{d[0]}: {vel}')
        return d[1], vel

    def test(self):
        c,v =self.obtener_comando()
        print(f'Comando a enviar: {c}, {v}')

    # Código no testeado
    def localizar_botones(self):
        t = Thread(target=self.__buttons, args=())
        t.start()
        salir = False
        while not salir:
            salir = True if input('Ingrese q para salir: ') == 'q' else False
        self.stopped = True

    def __buttons(self):
        for event in self.gamepad.read_loop():
            if self.stopped:
                break
            #Botones 
            if event.type == ecodes.EV_KEY:
                print(event)
            #Joystick
            elif event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                print(ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)


if __name__ == '__main__':
    mando = Controller(debug=True)
    while True:
        mando.test()
