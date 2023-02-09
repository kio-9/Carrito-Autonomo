from carrito import Carrito

def menu():
    description = 'G1 - Carrito'
    print(description)
    opt = input('\tTeleoperado -> 1\n\tEntrenamiento -> 2\nIntgrese una de las siguientes opciones: ')
    return opt

if __name__ == '__main__':
    car = Carrito()
    while True:
        option = menu()
        if option == '1':
            car.teleop()
        elif option == '2':
            pass
        else:
            print('Opción no válida')

