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
    Serial.println(newDist);
    if (newDist > 150){
      digitalWrite(yellowPin,LOW);
      digitalWrite(redPin,HIGH);
    }else if(newDist > 50){
      digitalWrite(yellowPin,HIGH);
      digitalWrite(redPin,LOW);
    }
    analogWrite(greenPin, newDist);
    
  }
}
