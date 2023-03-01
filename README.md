# Carrito-Autonomo
Proyecto del curso de vehículos autónomos
## Materiales
## Conexiones
![](https://github.com/kio-9/Carrito-Autonomo/blob/main/imagenes/conexiones.jfif)
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
