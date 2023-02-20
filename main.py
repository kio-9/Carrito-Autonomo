from carrito import Carrito
from prueba2_controlre import *

def menu(mando, description):
    print('-'*50)
    if mando.connected:
        print(description)
        opt, _ = mando.obtener_comando()
    else:
        opt = input(description)
    return opt

if __name__ == '__main__':
    print('G1 - Carrito')
    description = """Main menu
      1.  Teleoperado
      2.  Entrenamiento
      3.  Detección de líneas 
      4.  End to end autonomy 
Ingrese una de las opciones: """
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
        elif option == '4':
            # car.config(remote=True)
            car.autonomo()
        elif option == 'q':
            break
        else:
            print('Opción no válida')
