# Librerías

# Visi
class Navegacion:

    def __init__(self, modo='CNN'):
        self.modo = modo

    def getDir(self, image):
        ang = None
        if self.modo == 'CNN':
            ang = self.navCNN()
        elif self.mode == 'PID':
            ang = self.navPID()
        else:
            print('Modo inválido')
        return ang

    # Javier
    def navCNN(self):
        ang = None
        return ang

    # Chino
    def navPID(self):
        ang = None
        return ang
