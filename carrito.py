from perifericos import Camara, Arduino
import cv2
import pickle
import socket
import struct
from threading import Thread
from time import time, sleep
from prueba2_controlre import *

VEL_LIMIT = 300
ANG_LIMIT = 70

class Carrito:

    def __init__(self, remote=False, segmentateCam = False, training = 0):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        self.camara = Camara(segmentate=segmentateCam)
        self.training = training
        try:
            self.arduino = Arduino()
        except:
            print("arduino no conectado")
            self.arduino = None
        self.remote = remote
        if remote:
            self.connect2Server()
        self.ang = 0
        self.vel = 0
        self.img_counter = 0
        self.change = None
        self.stopped = False

    def config(self, remote=False, segmentateCam = False, training = 0):
        self.training = training
        self.remote = remote
        if remote:
            self.connect2Server()

    def move(self, comm,valor):
        if not comm:
            return
        if comm == 'w' and valor < VEL_LIMIT:
            self.vel = valor
            self.change = 'v'
        elif comm == 'a' and valor < ANG_LIMIT:
            self.ang = valor
            self.change = 'a'
        elif comm == 's':
            self.vel = 0
            self.change = 'v'
        elif comm == 'd' and valor > 0:
            self.ang = valor
            self.change = 'a'
        elif comm == 'x' and valor > -VEL_LIMIT:
            self.vel =valor
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
            comm = f'G{sign}{self.vel:.2f}'
        print(comm)
        if self.arduino is not None:
            self.arduino.sendCommand(comm)
        self.change = None

    def teleop(self):
        mando = Controller(debug=True)
        self.showControls()
        self.showInfo()
        while True:
            if mando.connected:
                com,valor=mando.leer_mando()
            else: # Falta adaptar valor
                com = input('Ingrese comando: ')
            if com =='q':
                self.stopped=True
                self.camara.stop()
                print('Saliendo del modo teleoperado')
                sleep(1)
                return
            self.move(com,valor)
            self.encodeArduino()

    def connect2Server(self):
        fh=open("ip.txt", 'r')
        ip=[line.rstrip() for line in fh]
        url = input(f'Ingrese dirección IP ({ip[0]}): ') #'4.tcp.ngrok.io'
        if not url:
            url=ip[0]
        port =input(f'Ingrese puerto ({ip[1]}): ')
        if not port:
            port=ip[1]
        if url != ip[0] or port != ip[1]:
            with open("ip.txt", 'w') as f:
                f.write('\n'.join([url, port]))
        self.client_socket.connect((url, int(port)))
        self.sendInit2Server()

    def sendInit2Server(self):
        self.client_socket.sendall(struct.pack(">hh", *self.camara.getImgSize()))
        self.client_socket.sendall(struct.pack(">h", self.training))
        if self.training:
            name = input('Ingrese nombre de entrenamiento: ')
            self.client_socket.sendall(struct.pack(">h", len(name) ))
            self.client_socket.sendall(struct.pack(f">{len(name)}s", name.encode() ))
            print(struct.pack(f">h{len(name)}s",len(name), name.encode()))

    def showInfo(self):
        t = Thread(target=self.show, args=())
        t.daemon = True
        t.start()
        return self

    def show(self):
        self.camara.start()
        #t_ant = time()
        while True:
            if self.stopped:
                break
            frame = self.camara.getFrames()
            curr_vel=self.vel
            curr_ang=self.ang
            #fps = 1/(time()-t_ant)
            #cv2.putText(frame, f"FPS: {30 if fps>30 else fps:.1f}",(520, 30), 
                        #cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            #t_ant = time()
            if not self.remote:
                cv2.imshow('Frame', frame)
                cv2.waitKey(1)
                continue
            self.img_counter += 1
            # Transmit data
            if self.img_counter % 5 != 0:
               continue
            #t_ant1 = time()
            _, image = cv2.imencode('.jpg', frame, self.encode_param)  
            data = pickle.dumps(image, 0)
            size = len(data)
            self.client_socket.sendall(struct.pack(">hfhL", self.img_counter, curr_vel, curr_ang, size) + data)
            #print(time()-t_ant1)
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
