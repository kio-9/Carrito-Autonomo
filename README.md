# Carrito-Autonomo
Proyecto del curso de vehículos autónomos
## Materiales
## Conexiones
![](https://github.com/kio-9/Carrito-Autonomo/blob/main/imagenes/conexiones.jfif)
Utilizar la siguiente definición de pines para la conexión entre driver, servomotor y arduino
#define MOTOR1_IN1 2
#define MOTOR1_IN2 3
#define MOTOR2_IN3 4
#define MOTOR2_IN4 5
#define PWM_MOTOR1 6
#define PWM_MOTOR2 7
#define PWM_SERVO 9
## Diseño Mecánico
## Algoritmos de navegación
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
