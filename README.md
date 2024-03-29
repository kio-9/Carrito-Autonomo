# Carrito-Autonomo
Proyecto del curso de vehículos autónomos
## Materiales
- Arduino Nano
- Wireless Halion GamePad
- Seeed Studio reComputer J1020 (basado en Jetson Nano)
- Antena Wifi
- Cámara (V-CAM PRO SX350)
- ServoMotor MG996R
- Motor Driver L298N
- Motores DC
- Reguladores Step Down: L2596s y XL4015
- Baterías (4) Li-Ion 18650 de 3.7 VDC
- Batería LiPo 3S de 2200 mAh
- Cables AWG 22 (datos) y AWG 16 (Alimentación)
- Borneras aéreas PVC
- Conector Jack
## Conexiones
![](https://github.com/kio-9/Carrito-Autonomo/blob/main/imagenes/conexiones.jfif)

Utilizar la siguiente definición de pines para la conexión entre driver, servomotor y arduino
- MOTOR1_IN1: PIN2
- MOTOR1_IN2: PIN3
- MOTOR2_IN3: PIN4
- MOTOR2_IN4: PIN5
- PWM_MOTOR1: PIN6
- PWM_MOTOR2: PIN7
- PWM_SERVO:  PIN9

## Manual de uso 
Conexión por ssh desde una computadora hacia la jetson
```
ssh nvidia@10.100.248.67
```
Comandos de activación en la jetson:
```
cd Carrito-Autonomo/
sudo chmod 666 /dev/ttyUSB0
python3 main.py
```
Uso del server:
- Conectar un puerto local a una IP pública
```
ngrok tcp 8490
```
- Correr el código de server.py
- Ingresar la IP pública generada en ngrok al programa de la jetson
