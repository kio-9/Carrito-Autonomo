from carrito import Carrito
from prueba2_controlre import *

def menu():
    description = '\tTeleoperado -> 1\n\tEntrenamiento -> 2\n\tDetección de líneas -> 3\nIngrese una de las opciones: '
    print(description)
    opt = None
    while not opt:
        opt, _ = mando.leer_mando()
    return opt

if __name__ == '__main__':
    mando = Controller(debug=True)
    print('G1 - Carrito')
    while True:
        option = menu()
        print('Mostrar datos:\n\tLocal -> 1\n\tRemoto -> 2\nIngrese una de las opciones: ')
        remoto = None
        while not remoto:
            remoto, _ = mando.leer_mando() 
        remoto = False if remoto=='1' else True
        if option == '1':
            car = Carrito(remote=remoto)
            car.teleop()
        elif option == '2': # servidor - guardar data
            pass
        elif option == '3':
            car = Carrito(remote=remoto, segmentateCam = True)
            car.configDeteccion()
        else:
            print('Opción no válida')
