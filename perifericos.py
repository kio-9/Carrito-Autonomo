import cv2
import serial
from threading import Thread
from queue import Queue
from time import time, sleep
# Cámara
class Camara:
    cap = None

    def __init__(self, queueSize=128):
        if self.__class__.cap is None:
            self.__class__.cap = cv2.VideoCapture(0)
            self.__class__.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.__class__.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camara = self.__class__.cap
        self.stopped = False
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            if self.Q.full():
                continue
            _, frame = self.camara.read()
            self.Q.put(frame)

    def read(self):
        return self.Q.get()

    def showFrames(self):
        t = Thread(target=self.show, args=())
        t.daemon = True
        t.start()
        return self

    def show(self):
        t_ant = time()
        while True:
            if self.stopped:
                break
            frame = self.read()
            fps = 1/(time()-t_ant)
            cv2.putText(frame, f"FPS: {30 if fps>30 else fps:.1f}",(520, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)
            t_ant = time()
        self.camara.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.stopped = True

# Arduino
class Arduino:
    ser = None

    def __init__(self):
        if self.__class__.ser is None:
            self.__class__.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
        self.ser = self.__class__.ser

    def sendCommand(self, command):
        command = command+"\n"
        self.ser.write(command.encode('utf_8'))
        print(self.ser.readline().decode())
        print(self.ser.readline().decode())

if __name__ == '__main__':
    opt = input('Opciones:\n\t1->camara\n\t2->motores\nIngrese una opcion: ')
    if opt=='1':
        cam = Camara().start().showFrames()
        while True:
            comando = input('Ingrese comando: ')
            print(f'Comando ingresado: {comando}')
            if comando == 'q':
                print('Saliendo...')
                cam.stop()
                sleep(1)
                break
    else:
        ard = Arduino()
        while True:
            comando = input('Ingrese comando: ')
            ard.sendCommand(comando)

