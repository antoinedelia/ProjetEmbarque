#include <SPI.h>
#include <Wire.h>
#include <Servo.h>
#include <SharpIR.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

SharpIR sensor(GP2YA41SK0F, A3);

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
  pinMode(electroaimant,OUTPUT);
  
  //on initialise les pins du moteur 1
  pinMode(motor1_in1Pin, OUTPUT);
  pinMode(motor1_in2Pin, OUTPUT);
  pinMode(motor1_enablePin, OUTPUT);
 
  //on initialise les pins du moteur 2
  pinMode(motor2_in1Pin, OUTPUT);
  pinMode(motor2_in2Pin, OUTPUT);
  pinMode(motor2_enablePin, OUTPUT);
  
  //on initialise les pins du moteur 3
  pinMode(motor3_in1Pin, OUTPUT);
  pinMode(motor3_in2Pin, OUTPUT);
  pinMode(motor3_enablePin, OUTPUT);
 
  //on initialise les pins du moteur 4
  pinMode(motor4_in1Pin, OUTPUT);
  pinMode(motor4_in2Pin, OUTPUT);
  pinMode(motor4_enablePin, OUTPUT);
  
  myservo.attach(4);
}

void loop() {
  Serial.println("Bonjour !");
  delay(100);
  int distance = sensor.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  distance = 10;
  if(distance > 5){
    Serial.println("Ici !");
    moveRobot(175, 175, 175, 175, false, true, false, true);
    delay(1000);
    turn90DegreesRight(4);
  }
  else if(distance <= 5){
    Serial.println("Là !");
      turn90DegreesRight(1);
  }
}

void turn90DegreesRight(int numberOfRotations){
  Serial.println("Bonsoir !");
  for(int i=0; i<numberOfRotations; i++)
  {
    moveRobot(100, 175, 175, 100, true, true, false, false);
    delay(1000);
  }
}

// callback for received data
void receiveData(int byteCount){
  Serial.print("Coucou !");
  while(Wire.available()) {
    number = Wire.read();
    Serial.print("data received:");
    Serial.println(number);

    switch (number) {
      case forward:
        moveRobot(175, 175, 175, 175, false, true, false, true);
        break;
      case backward:
        moveRobot(175, 175, 175, 175, true, false, true, false);
        break;
      case left:
        moveRobot(175, 100, 100, 175, false, false, true, true);
        break;
      case right:
        moveRobot(100, 175, 175, 100, true, true, false, false);
        break;
      case stopping:
        moveRobot(0, 0, 0, 0, true, true, true, true);
        break;
      default:
        
        break;
    }
  }
}


void moveRobot(int speedMotorFrontRight, int speedMotorFrontLeft, int speedMotorBackLeft, int speedMotorBackRight, boolean reverseMotorFrontRight, boolean reverseMotorFrontLeft, boolean reverseMotorBackLeft, boolean reverseMotorBackRight){
  SetMotor1(speedMotor1, reverseMotor1);
  SetMotor2(speedMotor2, reverseMotor2);
  SetMotor3(speedMotor3, reverseMotor3);
  SetMotor4(speedMotor4, reverseMotor4);
}

//Fonction qui set le moteur1
void SetMotor1(int speed, boolean reverse)
{
  analogWrite(motor1_enablePin, speed);
  digitalWrite(motor1_in1Pin, ! reverse);
  digitalWrite(motor1_in2Pin, reverse);
}
 
//Fonction qui set le moteur2
void SetMotor2(int speed, boolean reverse)
{
  analogWrite(motor2_enablePin, speed);
  digitalWrite(motor2_in1Pin, ! reverse);
  digitalWrite(motor2_in2Pin, reverse);
}

//Fonction qui set le moteur3
void SetMotor3(int speed, boolean reverse)
{
  analogWrite(motor3_enablePin, speed);
  digitalWrite(motor3_in1Pin, ! reverse);
  digitalWrite(motor3_in2Pin, reverse);
}
 
//Fonction qui set le moteur4
void SetMotor4(int speed, boolean reverse)
{
  analogWrite(motor4_enablePin, speed);
  digitalWrite(motor4_in1Pin, ! reverse);
  digitalWrite(motor4_in2Pin, reverse);
}


// callback for sending data
void sendData(){
  Wire.write(number);
}
