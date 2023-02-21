from perifericos import Camara, Arduino
import cv2
import pickle
import socket
import struct
from threading import Thread
from time import time, sleep
import time
from prueba2_controlre import *
from keras.models import load_model

VEL_LIMIT = 300
ANG_LIMIT_SUP = 54
ANG_LIMIT_INF = 15

#Autonomo
ANG_LIMIT_SUP_aut = 50 # IZQUIERDA
ANG_SUP = 34 # LEVE IZQUIERDA (LIMITE SUPERIOR - RECTO)/2
ANG_RECTO = 30
ANG_INF = 25 # LEVE DERECHA (LIMITE INFERIOR - RECTO)/2
ANG_LIMIT_INF_aut = 18 # DERECHA 

class Carrito:

    def __init__(self, remote=False, segmentateCam = False, training = 0):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        try:
            self.camara = Camara(segmentate=segmentateCam)
        except ConnectionError:
            self.camara = None
        self.training = training
        try:
            self.arduino = Arduino()
        except:
            self.arduino = None
            print('Puerto de arduino no encontrado')
        self.remote = remote
        if remote:
            self.connect2Server()
        self.ang = 30
        self.vel = 0
        self.img_counter = 0
        self.change = None
        self.stopped = False
        print(self)

    def __str__(self):
        msg = '_'*50
        msg += '\nEstado del Carrito:\n'
        msg += "Cámara no conectada\n" if not self.camara else "Cámara conectada\n"
        msg += "Arduino no conectado\n" if not self.arduino else "Arduino conectado\n"
        msg += '_'*50
        return msg

    def config(self, remote=False, segmentateCam = False, training = 0):
        self.training = training
        self.remote = remote
        if remote:
            self.connect2Server()

    def TecladoLogic(self,comm,valor):
        if comm == 'd' and valor < ANG_LIMIT_INF:
            valor = ANG_LIMIT_INF



    def move(self, comm,valor):
        if not comm:
            return
        ## Modificado - Verificamos que el mando está conectado
        if (mando.connected):
            TecladoLogic(comm,valor)
        else
            MandoLogic()
        
        
        
        # Saturadores
        if comm == 'd' and valor < ANG_LIMIT_INF:
            valor = ANG_LIMIT_INF
        if self.vel == 0 and valor == 999 and comm in 'xw':
            self.vel = 3 if comm == 'w' else -3
        if comm == 'w' and (valor <= VEL_LIMIT or (valor == 999 and self.vel <= VEL_LIMIT)):
            self.vel = valor if valor != 999 else self.vel+0.05
            self.change = 'v'
        elif comm == 'a' and (valor <= ANG_LIMIT_SUP or (valor == 999 and self.ang <= ANG_LIMIT)):
            self.ang = valor if valor != 999 else self.ang+5
            self.change = 'a'
        elif comm == 's':
            self.vel = 0
            self.change = 'v'
        elif comm == 'd' and (valor >= ANG_LIMIT_INF or (valor == 999 and self.ang >= ANG_LIMIT_INF )):
            self.ang = valor if valor != 999 else self.ang-5
            self.change = 'a'
        elif comm == 'x' and (valor >= -VEL_LIMIT or (valor ==999 and self.vel >= -VEL_LIMIT)):
            self.vel =valor if valor != 999 else self.vel-0.05
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
                valor = 999
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

    def img_preprocess(self, img):
        p_img = cv2.resize(img, (64, 60))
        p_img = cv2.cvtColor(p_img, cv2.COLOR_BGR2GRAY)
        p_img = p_img/255.
        return p_img.reshape(1, 60, 64, 1)
   
    def Ang_Select(prediccion): 
        max_prob = prediccion.max()
        max_prob_pos = None
        for pos,i in enumerate(prediccion):
            if max_prob == i:
                max_prob_pos = pos
                break
        return max_prob_pos
    
   def GiveAngleAuto(self, posicion_prob):
        if posicion_prob == 0: 
            self.ang = ANG_LIMIT_INF_aut
            self.vel = 3.3
            self.change = 'a'
            print("Movimiento brusco a la derecha")
        elif posicion_prob == 1:
            self.ang = ANG_INF
            self.vel = 4.2
            self.change = 'a'
            print("Movimiento a la derecha")
        elif posicion_prob == 2:
            self.ang = ANG_RECTO
            self.vel = 5
            print("Movimiento defrente")
        elif posicion_prob == 3:
            self.ang = ANG_SUP
            self.vel = 4.2
            self.change = 'a'
            print("Movimiento a la izquierda")
        else:
            self.ang = ANG_LIMIT_SUP_aut
            self.vel = 3.3
            self.change = 'a'
            print("Movimiento brusco a la izquierda")
    
    def Mode_Autonomo(self):
        t = Thread(target=self.autonomo, args=())
        t.daemon = True
        t.start()
        return self
        
    def autonomo(self):
        modelo = load_model('modelo_alvinn.h5')
        modelo.summary()
        while True:
            t = time.time()
            img = self.camara.get_rtImg()
            img = self.img_preprocess(img)
            prediccion = modelo.predict(img)
            print(prediccion)
            print(f'Tiempo transcurrido: {time.time()-t}')
            pos_prediccion = Ang_Select(prediccion[0])
            self.GiveAngleAuto(pos_prediccion)
            self.encodeArduino()
            if self.stopped:
                self.camara.stop()
                print('Saliendo del modo autonomo')
                sleep(1)
                return

if __name__ == '__main__':
    opt = input('1->Local, 2->remoto : ')
    car = Carrito(remote=True if opt=='2' else False).showInfo()
