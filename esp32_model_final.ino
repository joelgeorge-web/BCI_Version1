#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled!
#endif

int in1 = 27; 
int in2 = 26; 

BluetoothSerial SerialBT;

void setup() {
  Serial.flush();
  Serial.begin(9600);
  SerialBT.begin("ESP32test"); //Bluetooth device name
  Serial.println("Ready to pair");
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);


}

void loop() {
  if (SerialBT.available() > 0) {
    String str = SerialBT.readString();
    int a = str.toInt();
    Serial.println(a);
    switch (a) {
      case 0:
        break;
      case 1:  // Move forward
        moveForward();
        Serial.flush();
        break;
      case 2:  // Turn left
        Serial.flush();
        break;
      case 3:  // Turn right 
        Serial.flush();
        break;
      case 4:  // Move backward
        moveBackward();
        Serial.flush(); 
        break;
      //default: 
        //stopcar();
        //Serial.flush();
        //delay(2000); 
        //break;
    }
  }

  else {
    Serial.flush();
  }
  Serial.flush();
}




void moveForward() { 
  digitalWrite(in1, HIGH);  // Motor A forward
  digitalWrite(in2, LOW);
  delay(800);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  delay(3000); 
  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH);
  delay(800);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);

}

void moveBackward() {
  digitalWrite(in1, LOW);  // Motor A reverse
  digitalWrite(in2, HIGH);
  delay(800);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  delay(3000);
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, LOW);
  delay(800);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}





