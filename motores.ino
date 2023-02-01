int PinIN1 = 2;
int PinIN2 = 3;
double pwm=0;
int PinIN3 = 4;
int PinIN4 = 5;

int analog1 = 6;
int analog2 = 7;
           
void setup() {
  // inicializar la comunicación serial a 9600 bits por segundo:
  Serial.begin(9600);
  // configuramos los pines como salida
  pinMode(analog1, OUTPUT);
  pinMode(analog2, OUTPUT);
  
  //MOTOR TRASERO
  pinMode(PinIN1, OUTPUT);
  pinMode(PinIN2, OUTPUT);
  
  //MOTOR DELANTERO
 pinMode(PinIN3, OUTPUT);
  pinMode(PinIN4, OUTPUT);
}

void loop() {

 if (Serial.available() > 0) {
    pwm = Serial.parseFloat(); 
    Serial.print("Se ingresa: ");
    Serial.println(pwm);    
  analogWrite(analog1, pwm*255/6.0);
  analogWrite(analog2, pwm*255/6.0);
  MotorHorario();
  Serial.println("Giro del Motor en sentido horario");
  delay(100);
  
 }
  //MotorAntihorario();
  //Serial.println("Giro del Motor en sentido antihorario");
  //delay(1000);
  
  //MotorStop();
  //Serial.println("Motor Detenido");
  //delay(1000);
  
}

void MotorHorario()
{
  digitalWrite (PinIN1, HIGH);
  digitalWrite (PinIN3, HIGH);
  digitalWrite (PinIN2, LOW);
  digitalWrite (PinIN4, LOW);
}
void MotorAntihorario()
{
  digitalWrite (PinIN1, LOW);
  digitalWrite (PinIN2, HIGH);
}

void MotorStop()
{
  digitalWrite (PinIN1, LOW);
  digitalWrite (PinIN2, LOW);
}