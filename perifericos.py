import cv2
import serial
# Cámara
class Camara:
    cap = None

    def __init__(self):
        if self.__class__.cap is None:
            self.__class__.cap = cv2.VideoCapture(0)
        self.camara = self.__class__.cap

    def read(self):
        _, frame = self.camara.read()
        cv2.imshow('Frame', frame)

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
