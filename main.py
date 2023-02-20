from carrito import Carrito
from prueba2_controlre import *

def menu(mando, description):
    if mando.connected:
        print(description)
        opt, _ = mando.obtener_comando()
    else:
        opt = input(description)
    return opt

if __name__ == '__main__':
    print('G1 - Carrito')
    description = '\tTeleoperado -> 1\n\tEntrenamiento -> 2\n\tDetección de líneas -> 3\nIngrese una de las opciones: '
    car = Carrito()
    mando = Controller(debug=True)
    while True:
        option = menu(mando, description)
        if option == '1':
            ind = 'Mostrar datos:\n\tLocal -> 1\n\tRemoto -> 2\nIngrese una de las opciones: '
            remoto = menu(mando, ind)
            remoto = False if remoto=='1' else True
            car.config(remote=remoto)
            car.teleop()
        elif option == '2': # servidor - guardar data
            car.config(remote=True, training=1)
            car.teleop()
        elif option == '3': # Corregir
            car.config(remote=True, segmentateCam=True)
            car.configDeteccion()
        else:
            print('Opción no válida')
