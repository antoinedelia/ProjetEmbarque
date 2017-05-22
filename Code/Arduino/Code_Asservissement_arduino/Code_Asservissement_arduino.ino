#include <SPI.h>
#include <Wire.h>
#include <Servo.h>
#include <SharpIR.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

SharpIR sensor(GP2YA41SK0F, A3);

int motor1_enablePin = 11; //pwm
int motor1_in1Pin = 13;
int motor1_in2Pin = 12;
 
int motor2_enablePin = 3; //pwm
int motor2_in1Pin = 8;
int motor2_in2Pin = 7;
int electroaimant = 6;

Servo myservo;  // create servo object to control a servo
int val;    // variable to read the value from the analog pin

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

  pinMode(motor1_in1Pin, OUTPUT);
  pinMode(motor1_in2Pin, OUTPUT);
  pinMode(motor1_enablePin, OUTPUT);
  pinMode(electroaimant,OUTPUT);
 
  //on initialise les pins du moteur 2
  pinMode(motor2_in1Pin, OUTPUT);
  pinMode(motor2_in2Pin, OUTPUT);
  pinMode(motor2_enablePin, OUTPUT);
  
  myservo.attach(4);
}

void loop() {
  delay(100);
  int distance = sensor.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  if(distance >= 5){
    moveRobot(500,200,true,true);
  }
  else if(distance <= 5){
      moveRobot(0,0,true,true);
  }
}

// callback for received data
void receiveData(int byteCount){

  while(Wire.available()) {
    number = Wire.read();
    Serial.print("data received:");
    Serial.println(number);

    switch (number) {
      case forward:
        moveRobot(200, 200, true, true);
        break;
      case backward:
        moveRobot(200, 200, false, false);
        break;
      case left:
        moveRobot(100, 100, false, true);
        break;
      case right:
        moveRobot(100, 100, true, false);
        break;
      case stopping:
        moveRobot(0, 0, true, true);
        break;
      default:
        moveRobot(0, 0, true, true);
        break;
    }
  }
}


void moveRobot(int speedMotor1, int speedMotor2, boolean reverseMotor1, boolean reverseMotor2 ){
  SetMotor1(speedMotor1, reverseMotor1);
  SetMotor2(speedMotor2, reverseMotor2);
}

//Fonction qui set le moteur1
void SetMotor1(int speed, boolean reverse)
{
  analogWrite(motor1_enablePin, speed);
  digitalWrite(motor1_in1Pin, reverse);
  digitalWrite(motor1_in2Pin, reverse);
}

//Fonction qui set le moteur2
void SetMotor2(int speed, boolean reverse)
{
  analogWrite(motor2_enablePin, speed);
  digitalWrite(motor2_in1Pin, reverse);
  digitalWrite(motor2_in2Pin, reverse);
}


// callback for sending data
void sendData(){
  Wire.write(number);
}
