#include <Servo.h>

  int servoPin = 1;
  Servo servo;
  int servoAngle = 0;
  int electroaimant = 0;
  
void setup() {
  //Serial.begin(9600);
  servo.attach(servoPin);
  pinMode(electroaimant,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(electroaimant, HIGH);
  servo.write(0);
  delay(1000);
  servo.write(90);
  delay(3000);
  digitalWrite(electroaimant, LOW);
  delay(5000);

}
