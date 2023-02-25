from perifericos import Camara, Arduino
import cv2
import pickle
import socket
import struct
from threading import Thread
from time import time, sleep

VEL_LIMIT = 300
ANG_LIMIT = 70

class Carrito:

    def __init__(self, remote=False, segmentateCam = False):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        self.camara = Camara(segmentate=segmentateCam)
        try:
            self.arduino = Arduino()
        except:
            print("arduino no conectado")
        self.remote = remote
        if remote:
            self.connect2Server()
        self.ang = 20
        self.vel = 0
        self.img_counter = 0
        self.change = None
        self.stopped = False

    def move(self, comm):
        if comm not in 'wasdx':
            print('Comando no válido')
            return
        if comm == 'w' and self.vel < VEL_LIMIT:
            self.vel += 1
            self.change = 'v'
        elif comm == 'a' and self.ang < ANG_LIMIT:
            self.ang += 5
            self.change = 'a'
        elif comm == 's':
            self.vel = 0
            self.change = 'v'
        elif comm == 'd' and self.ang > 0:
            self.ang -= 5
            self.change = 'a'
        elif comm == 'x' and self.vel > -VEL_LIMIT:
            self.vel -= 1
            self.change = 'v'

    def showControls(self):
        ctrls = "Controles:\n\tw: avanzar\n\ta: izquierda\n\ts: stop\n\td: derecha\n\tx: retroceder"
        print(ctrls)

    def encodeArduino(self):
        if self.change is None:
            return
        if self.change == 'a':
            comm = f'S{self.ang}'
        elif self.vel == 0:
            comm = 'G0'
        else:
            sign = '+' if self.vel >= 0 else ''
            num = 3 if self.vel > 0 else -3
            num += self.vel/100
            comm = f'G{sign}{num:.2f}'
        print(comm)
        self.arduino.sendCommand(comm)
        self.change = None

    def teleop(self):
        self.showControls()
        self.showInfo()
        while True:
            com = input('Ingrese comando: ')
            if com =='q':
                self.stopped=True
                self.camara.stop()
                print('Saliendo del modo teleoperado')
                sleep(1)
                return
            self.move(com)
            self.encodeArduino()

    def connect2Server(self):
        url = input('Ingrese dirección IP: ') #'4.tcp.ngrok.io'
        port = int(input('Ingrese puerto: '))
        self.client_socket.connect((url, port))
        self.client_socket.sendall(struct.pack(">hh", *self.camara.getImgSize()))

    def showInfo(self):
        t = Thread(target=self.show, args=())
        t.daemon = True
        t.start()
        return self

    def show(self):
        self.camara.start()
        t_ant = time()
        while True:
            if self.stopped:
                break
            frame = self.camara.getFrames()
            curr_vel=self.vel
            curr_ang=self.ang
            fps = 1/(time()-t_ant)
            cv2.putText(frame, f"FPS: {30 if fps>30 else fps:.1f}",(520, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            t_ant = time()
            if not self.remote:
                cv2.imshow('Frame', frame)
                cv2.waitKey(1)
                continue
            self.img_counter += 1
            # Transmit data
            if self.img_counter % 20 != 0:
               continue
            t_ant1 = time()
            _, image = cv2.imencode('.jpg', frame, self.encode_param)  
            data = pickle.dumps(image, 0)
            size = len(data)
            self.client_socket.sendall(struct.pack(">hfhL", self.img_counter, curr_vel, curr_ang, size) + data)
            print(time()-t_ant1)
            # print(f'Tamaño de la cola luego de enviar: {self.Q.qsize()}')
            
        cv2.destroyAllWindows()

    def stop(self):
        self.stopped = True

    def configDeteccion(self):
        self.showInfo()
        self.camara.detectLines()
        while True:
            command = input('Params: ')
            if command == 'i':
                print(car.camara.houghParams)
                continue
            try:
                key = int(command[0])
            except:
                self.stop()
                sleep(1)
                break
            self.camara.houghParams[key]=int(command[1:]) if key!=1 else int(command[1:])/100

if __name__ == '__main__':
    opt = input('1->Local, 2->remoto : ')
    car = Carrito(remote=True if opt=='2' else False).showInfo()

    def teleop(self):
        self.showControls()
        while True:
            self.move(input('Ingrese comando: '))
            self.encodeArduino()