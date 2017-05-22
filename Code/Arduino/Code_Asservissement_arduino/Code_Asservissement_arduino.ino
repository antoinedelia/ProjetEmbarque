#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

enum actions {
  forward = 1,
  backward = 2,
  left = 3,
  right = 4,
  stopping = 5
};

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
}

void loop() {
  delay(100);
}

// callback for received data
void receiveData(int byteCount){

  while(Wire.available()) {
    number = Wire.read();
    Serial.print("data received:");
    Serial.println(number);

    switch (number) {
      case forward:
        //GO FORWARD
        break;
      case backward:
        //GO FORWARD
        break;
      case left:
        //GO LEFT
        break;
      case right:
        //GO RIGHT
        break;
      case stopping:
        //STOP
        break;
      default:
        //Error value
        break;
    }
  }
}

// callback for sending data
void sendData(){
  Wire.write(number);
}
