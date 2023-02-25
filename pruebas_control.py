from prueba2_controlre import *

# Print menu
def selector():
    opt=None
    MENU = "Opciones:\n\tBack \tModo teleoperado\n\tStart \tModo autónomo\n\tL1 \tControles"
    CONTROLES = "\nJoystick izq. \tMovimiento lineal\nX\t\tMover Izquierda\nB\t\tMover Derecha"
    CONTROLES += "\nA\t\tStatus\nY\t\tSafe Stop\nCruceta izq.\tCámara\nCruceta der.\tGPS"
    CONTROLES += "\nCruceta abajo\tIMU\nR1\t\tSalir\n" 
    print(MENU)
    while not (opt == 't' or opt =='y'): 
        opt,_ = mando.leer_mando()
        if opt == 'q':
            print(CONTROLES)
            print(MENU)
    if opt=='t':
        print("Modo Teleoperado")
        enable=1
    else:
        print("Modo Autonomo. PDM 2023-1")
        enable=2
    return enable
mando = Controller(debug=True)
while True:
    enable=selector()
    print(enable)
    if enable == 1:
        print("holaaaaaaaaAA")
    if enable == 2:
        print("holi")
