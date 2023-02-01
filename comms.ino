#define LED 7

int frec = 1000;

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  static char message[5];
  static uint8_t message_pos = 0;
  while (Serial.available()>0){
   char inByte = Serial.read();
   if ( inByte != '\n' && (message_pos < 4) )   {
     //Add the incoming byte to our message
     message[message_pos] = inByte;
     message_pos++;
   }
   else{
    Serial.println(message);
    if(message[0]=='G'){
      frec = 500;
    }
    else if(message[0]=='S'){
      frec = 100;
    }
    else{
      frec = 1000;
    }
    message_pos = 0;
   }
  }
  digitalWrite(LED, HIGH);
  delay(frec);
  digitalWrite(LED, LOW);
  delay(frec);
}