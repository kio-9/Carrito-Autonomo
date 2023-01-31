import cv2

class Camara:
    cap = None

    def __init__(self):
        if self.__class__.cap is None:
            self.__class__.cap = cv2.VideoCapture(0)
        self.camara = self.__class__.cap

    def leer_camara(self):
        _, frame = self.camara.read()
        cv2.imshow('Frame', frame)
        cv2.waitKey(0)

