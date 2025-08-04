int greenPin = 11;
int yellowPin = 10;
int redPin = 9;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(greenPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(redPin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    String dist = Serial.readStringUntil('\n');
    int newDist = dist.toInt();
    if (newDist >= 75){
      digitalWrite(yellowPin,LOW);
      digitalWrite(greenPin,LOW);
      digitalWrite(redPin,HIGH);
    }else if (newDist > 25){
      digitalWrite(yellowPin,HIGH);
      digitalWrite(redPin,LOW);
      digitalWrite(greenPin,LOW);
    }else if(newDist >= 0){
      digitalWrite(greenPin,HIGH);
      digitalWrite(yellowPin,LOW);
      digitalWrite(redPin,LOW);
    }  
  }
}
