# sudo chmod 666 /dev/ttyUSB1
import serial

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
    arduino = Arduino()
    while True:
        command = input('Ingrese comando: ')
        arduino.sendCommand(command)
