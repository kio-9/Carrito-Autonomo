from carrito import Carrito

def menu():
    description = '\tTeleoperado -> 1\n\tEntrenamiento -> 2\n\tDetección de líneas -> 3\nIngrese una de las opciones: '
    opt = input(description)
    return opt

if __name__ == '__main__':
    print('G1 - Carrito')
    while True:
        option = menu()
        remoto = input('Mostrar datos:\n\tLocal -> 1\n\tRemoto -> 2\nIngrese una de las opciones: ')
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
