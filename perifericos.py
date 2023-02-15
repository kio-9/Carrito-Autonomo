import cv2
import numpy as np
import serial
from threading import Thread
from queue import Queue
from time import time, sleep

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

if __name__ == '__main__':
    opt = input('Opciones:\n\t1->camara+motores\n\t2->detector de lineas\nIngrese una opcion: ')
    if opt=='1':
        ard = Arduino()
        cam = Camara(remote=True).start().showFrames()
        while True:
            comando = input('Ingrese comando: ')
            print(f'Comando ingresado: {comando}')
            ard.sendCommand(comando)
            if comando == 'q':
                print('Saliendo...')
                cam.stop()
                sleep(1)
                break
    else:
        opt = input('1->Local, 2->remoto : ')
        cam = Camara(remote=True if opt=='2' else False).start().detectLines()
        while True:
            command = input('Params: ')
            if command == 'i':
                print(cam.houghParams)
                continue
            try:
                key = int(command[0])
            except:
                cam.stop()
                sleep(1)
                break
            cam.houghParams[key]=int(command[1:]) if key!=1 else int(command[1:])/100
