import serial

class Arduino:
    ser = None

    def __init__(self):
        if self.__class__.ser is None:
            self.__class__.ser = serial.Serial('/dev/ttyACM0')
        self.ser = self.__class__.ser

    def sendCommand(self, command):
        self.ser.write(command.encode('utf_8'))
        print(self.ser.readline())
        
if __name__ == '__main__':
    arduino = Arduino()
    while True:
        comand = input('Ingrese comando: ')
        arduino.sendCommand(comand)
