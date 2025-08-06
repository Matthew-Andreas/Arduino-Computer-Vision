#include "LedControl.h"

LedControl lc = LedControl(12,10,11,1);

int timeDelay = 100;
int col0 = 8;
int col1 = 8;
int col2 = 8;
int col3 = 8;
int col4 = 8;
int col5 = 8;
int col6 = 8;
int col7 = 8;

void dropBall(int slot);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  lc.shutdown(0,false);
  lc.setIntensity(0,3);
  lc.clearDisplay(0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    String dist = Serial.readStringUntil('\n');
    size_t pos = dist.indexOf(",");
    int slot;
    bool drop;
    if(pos != -1){
      slot = dist.substring(0,pos).toInt();
      if(!dist.substring(pos+1,dist.length()).toInt()){
        dropBall(slot);
      }
    }
    //int newDist = dist.toInt();
    for(int i = 0; i < 8;i++){
      lc.setLed(0, i, 0, false);
    }
    lc.setLed(0, slot/10, 0, true);
    //delay(timeDelay);
    //lc.setLed(0, slot/10, 0, false);
    //delay(timeDelay);
    //lc.setLed(0, slot/10, 0, true);
  }
}

void dropBall(int slot){
  for(int i = 1; i<8; i++){
    lc.setLed(0, slot/10, i-1, false);
    lc.setLed(0, slot/10, i, true);
    delay(200);
  }
}
