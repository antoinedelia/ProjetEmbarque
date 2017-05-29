#include <SPI.h>
#include <Wire.h>
#include <Servo.h>
#include <SharpIR.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

int periode=20000;// période entre chaque début d'impulsion en microsecondes


//pin motor : 
int motor1_enablePin = 11; //pwm
int motor1_in1Pin = 13;
int motor1_in2Pin = 12;

int motor2_enablePin = 10; //pwm
int motor2_in1Pin = 8;
int motor2_in2Pin = 7;

int motor3_enablePin = 9; //pwm
int motor3_in1Pin = 3;
int motor3_in2Pin = 2;
 
int motor4_enablePin = 6; //pwm
int motor4_in1Pin = 5;
int motor4_in2Pin = 4;

enum actions {
  forward = 1,
  backward = 2,
  left = 3,
  right = 4,
  stopping = 5,
  enableMagnet = 6,
  disableMagnet = 7
};

SharpIR sensor(GP2YA41SK0F, A3);

int electroaimant = 0;

int servoMagnetPin = 1;

Servo servoMagnet;  // create servo object to control a servo
int servoAngle = 0;

int val;    // variable to read the value from the analog pin

void setup() {
  servoMagnet.attach(servoMagnetPin);
  
  //Serial.begin(9600); //Disable serial begins, otherwise pin 0 & 1 ALWAYS HIGH
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
  pinMode(electroaimant, OUTPUT);
  
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
  
}

void loop() {
  delay(100);
  if (number != 0)
  {
    switch (number) {
      case forward:
        Serial.println("Go forward");
        forwardRobot();
        break;
      case backward:
        backwardRobot();
        break;
      case left:
        leftRobot();
        break;
      case right:
        rightRobot(1);
        break;
      case stopping:
        stopRobot();
        break;
      case enableMagnet:
        ActivateMagnet();
        break;
      case disableMagnet:
        DisableMagnet();
        break;
      default:
        //int distance = sensor.getDistance(); //Calculate the distance in centimeters and store the value in a variable
        int distance = 10;
        if(distance > 5){
          forwardRobot(); 
          //ActivateMagnet();
        }
        else if(distance <= 5){
            rightRobot(2);
        }
        break;
    }
    number = 0;
  }
    
}

// callback for received data
void receiveData(int byteCount){
  // Clear buffer ?
  while(Wire.available()) {
    number = Wire.read();
    Serial.print("Received data : ");
    Serial.println(number);
  }
}

// callback for sending data
void sendData(){
  Wire.write(number);
}
