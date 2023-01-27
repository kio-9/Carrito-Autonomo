#include <Servo.h> //Libreria para Servomotores

#define SERVO 9

Servo Servo_1;  

int top_ang = 0;    // Variable que contendra el angulo de giro del servo
int Angulo = 0;
int incre=1;
void setup() 
{ 
  Serial.begin(9600);
  Servo_1.attach(SERVO);  // Definir el pin (9) que se utilizara para el control del servo
  
} 


void loop() 
{ 
 
  if (Serial.available() > 0) {    
    top_ang = Serial.parseInt(); 
    Serial.print("Se ingresa: ");
    Serial.println(top_ang);    
    if(Angulo<=top_ang){
        incre=1;
      }
     else{
      incre=-1;
      }
    for(Angulo;Angulo!=top_ang; Angulo += incre)  //Incrementar de 1 en 1 el angulo que va de 0° hasta 180 
    {
       Servo_1.write(Angulo);
       Serial.println(Angulo);
    }
      delay(500);
      Serial.println(Angulo);
    
  } 
  
 // delay(500);                        //Esperar 500 ms 
}
