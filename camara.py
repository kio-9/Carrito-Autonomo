import cv2

class Camara:
    cap = None

    def __init__(self):
        if self.__class__.cap is None:
            self.__class__.cap = cv2.VideoCapture(0)
        self.camara = self.__class__.cap

    def read(self):
        _, frame = self.camara.read()
        cv2.imshow('Frame', frame)

if __name__ == '__main__':
    camara = Camara()
    while True:
        camara.read()
        if(cv2.waitKey(10) & 0xFF == ord('b')):
            break
