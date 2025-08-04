int greenPin = 11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(greenPin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    String dist = Serial.readStringUntil('\n');
    int newDist = dist.toInt();
    analogWrite(greenPin, newDist);
  }
}
