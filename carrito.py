from perifericos import Camara, Arduino

VEL_LIMIT = 3004
ANG_LIMIT = 70

class Carrito:

    def __init__(self):
        self.camara = Camara()
        self.arduino = Arduino()
        self.ang = 20
        self.vel = 0
        self.change = None

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
        self.camara.start().transmitFrames()
        while True:
            self.move(input('Ingrese comando: '))
            self.encodeArduino()
