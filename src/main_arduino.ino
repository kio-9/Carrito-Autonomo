#include <Servo.h>

#define MOTOR1_IN1 2
#define MOTOR1_IN2 3
#define MOTOR2_IN3 4
#define MOTOR2_IN4 5
#define PWM_MOTOR1 6
#define PWM_MOTOR2 7
#define PWM_SERVO 9

Servo Servo_1;
int ref_ang = 0;
int ang = 0;
int inc = 1;
float vel=0;

void setup() {
  Serial.begin(115200);
  
  //MOTOR TRASERO
  pinMode(PWM_MOTOR1, OUTPUT);
  pinMode(MOTOR1_IN1, OUTPUT);
  pinMode(MOTOR1_IN2, OUTPUT);
  
  //MOTOR DELANTERO
  pinMode(PWM_MOTOR2, OUTPUT);
  pinMode(MOTOR2_IN3, OUTPUT);
  pinMode(MOTOR2_IN4, OUTPUT);

  //SERVOMOTOR
  Servo_1.attach(PWM_SERVO);
}

void loop() {
  // Lectura de comando
  while (Serial.available()>0){
   static char message[6];
   static uint8_t message_pos = 0;
   char inByte = Serial.read();
   char settings_data[5];
   if ( inByte != '\n' && (message_pos < 5) )   {
     //Add the incoming byte to our message
     message[message_pos] = inByte;
     message_pos++;
   }
   else{
    message[message_pos] = '\0';
    Serial.println(message); // Eco
    // Decodificación
    if(message[0]=='G'){ // Control de velocidad
      //Serial.println(&message[2]);
      vel = atof(&message[2]);
      ControlMotor(message[1], vel);
      //Serial.println(vel);
    }
    else if(message[0]=='S'){ // Control de dirección
      ref_ang = atoi(&message[1]);
      CambiarSentidoServo();
      //Serial.println(inc);
      //Serial.println(ref_ang);
    }
    else{
      Serial.println("Error");
    }
    message_pos = 0;
   }
  }
  // Cambio progresivo de dirección
  IncrementarServo();
}

void CambiarSentidoServo(){
  if(ref_ang>=ang){
    inc = 1;
  }
  else{
    inc = -1;
  }
}

void IncrementarServo(){
  if(ang!=ref_ang){
    ang += inc;
    Servo_1.write(ang);
  }
}

void ControlMotor(char sentido, float vel){
  if(sentido=='+'){
    MotorAntihorario();
  }
  else{
    MotorHorario();
  }
  analogWrite(PWM_MOTOR1, vel*255/6.0);
  analogWrite(PWM_MOTOR2, vel*255/6.0);
}

void MotorHorario(){
  digitalWrite (MOTOR1_IN1, HIGH);
  digitalWrite (MOTOR1_IN2, LOW);
  digitalWrite (MOTOR2_IN3, HIGH);
  digitalWrite (MOTOR2_IN4, LOW);
}
void MotorAntihorario(){
  digitalWrite (MOTOR1_IN1, LOW);
  digitalWrite (MOTOR1_IN2, HIGH);
  digitalWrite (MOTOR2_IN3, LOW);
  digitalWrite (MOTOR2_IN4, HIGH);
}
void MotorStop(){
  digitalWrite (MOTOR1_IN1, LOW);
  digitalWrite (MOTOR1_IN2, LOW);
  digitalWrite (MOTOR2_IN3, LOW);
  digitalWrite (MOTOR2_IN4, LOW);
}