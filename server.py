# Import the required modules
from IPython.display import clear_output
import socket
import os
import cv2
import matplotlib.pyplot as plt
import pickle
import numpy as np
import struct
from PIL import Image, ImageOps
from time import time
import sqlite3

HOST=''
PORT=8000

class DataBase:
    dbName = 'datos.sqlite'
    dbConn = None
    cur = None

    def __init__(self):
        classAtt = self.__class__
        if not classAtt.dbConn:
            classAtt.dbConn = sqlite3.connect(classAtt.dbName, timeout=20)
            classAtt.cur = classAtt.dbConn.cursor()
        self.dbName = classAtt.dbName
        self.dbConn = classAtt.dbConn
        self.cur = classAtt.cur

    def createDB(self):
        self.cur.executescript('''
        CREATE TABLE IF NOT EXISTS Datos (
            video_id    INT,
            frame       INT,
            vel         FLOAT,
            dir         INT,
            PRIMARY KEY (video_id, frame)
        );
        CREATE TABLE IF NOT EXISTS Videos (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name        TEXT,
            path        TEXT
        );
        ''')
        self.dbConn.commit()

class VideoReception(DataBase):

    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((HOST,PORT))
        self.s.listen(10)
        self.host = input('Ingrese la dirección IP: ')
        print('Socket ready and listening')
        self.conn = None 
        self.addr = None
        self.data = b""
        self.result = None
        self.nFrame = 0
        self.video_id = None
        # Rangos de la estructura esperada
        data = ">hfhL"
        self.FRAME_NUMBER = slice(struct.calcsize(data[:2]))
        self.VEL = slice(struct.calcsize(data[:2]), struct.calcsize(data[:3]))
        self.DIR = slice(struct.calcsize(data[:3]), struct.calcsize(data[:4]))
        self.IMG_LEN = slice(struct.calcsize(data[:4]), struct.calcsize(data))
        self.payload_size= struct.calcsize(data)

    def showMenu(self):
        print(f'Intrucciones: \n\t1. Conectarse al servidor {self.host}\n\t2. Enviar tamaño de imágenes (width, height)\n\t3. Enviar datos (vel,dir,img)\n')

    def connect(self):
        self.showMenu()
        self.conn, self.addr = self.s.accept()
        print('Conectado')
        self.videoName = input('Nombre del video a grabar (Enter para no grabar): ')
        self.videoName += '.avi'
        size = self.getImgSize()
        if self.videoName:
            self.result = cv2.VideoWriter(self.videoName, cv2.VideoWriter_fourcc(*"MJPG"), 20, size)
            super().__init__()
            self.createDB()
            self.saveVideo()

    def saveVideo(self):
        path = os.path.join(os.getcwd(), self.videoName)
        self.cur.execute('INSERT INTO Videos (name, path) VALUES (?, ?)', (self.videoName, path))
        self.dbConn.commit()
        self.video_id = self.cur.lastrowid

    def getImgSize(self):
        msg_size = struct.calcsize(">hh")
        self.read(msg_size)
        width = struct.unpack(">h", self.data[:struct.calcsize(">h")])[0]
        height = struct.unpack(">h", self.data[struct.calcsize(">h"):struct.calcsize(">hh")])[0]
        self.data = self.data[msg_size:]
        print(f'Tamaño de la imagen a recibir: {width}x{height}')
        return width, height
        
    def read(self, payload_size):
        t = time()
        while len(self.data) < payload_size:
            self.data += self.conn.recv(4096)
            if time()-t>5:
                return False
        return True

    def parse_data(self):
        if not self.read(self.payload_size):
            return
        nframe = struct.unpack(">h", self.data[self.FRAME_NUMBER])[0]
        vel = struct.unpack(">f", self.data[self.VEL])[0]
        dir = struct.unpack(">h", self.data[self.DIR])[0]
        msg_size = struct.unpack(">L", self.data[self.IMG_LEN])[0]
        self.data = self.data[self.payload_size:]
        print(f'Frame: {nframe}\tVel: {vel:.2f}\tSteering: {dir}\tImg len: {msg_size}')
        if not self.read(msg_size):
            return
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        self.nFrame += 1
        print('done')
        return vel, dir, frame_data

    def saveData(self, frame, vel, dir):
        if not self.videoName:
            return
        self.result.write(frame)
        self.cur.execute('INSERT INTO Datos (video_id, frame, vel, dir) VALUES (?, ?, ?, ?)', (self.video_id, self.nFrame, vel, dir))
        self.dbConn.commit()
             
    def closeVideo(self):
        self.result.release()

receptor = VideoReception()
while True:
    receptor.connect()
    # video = SaveData('video.avi', receptor.getImgSize())
    while True:
        try:
            vel, dir, frame_data = receptor.parse_data()
        except:
            print('Comunicación finalizada')
            break
        # unpack image using pickle 
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Guardar info
        receptor.saveData(frame, vel, dir)

        # Mostrar imagen
        cv2.putText(frame, f"Velocidad: {vel:.1f}\tDirección: {dir}°",(30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow('server',frame)
        cv2.waitKey(1)
    receptor.closeVideo()
    cv2.destroyAllWindows()
    print('Esperando nueva conexión...')