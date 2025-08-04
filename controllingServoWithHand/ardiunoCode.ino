#include <Servo.h>

Servo myServo;

int servoPin = 9;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  myServo.attach(servoPin);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    String dist = Serial.readStringUntil('\n');
    int newDist = dist.toInt();
    myServo.write(newDist);
  }

  
}
