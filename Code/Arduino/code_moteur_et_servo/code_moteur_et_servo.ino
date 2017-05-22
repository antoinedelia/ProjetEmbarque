#include <Servo.h>
#include <SharpIR.h>

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
 
void setup()
{
  Serial.begin(9600);
  //on initialise les pins du moteur 1
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
 
void loop()
{
  /*digitalWrite(electroaimant,HIGH);
  delay(3000);
  digitalWrite(electroaimant,LOW);*/
  int distance = sensor.getDistance(); //Calculate the distance in centimeters and store the value in a variable
  /*val = 600;            // reads the value of the potentiometer (value between 0 and 1023)
  val = map(val, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
  myservo.write(val);                  // sets the servo position according to the scaled value
  val = map(0, 0, 1023, 0, 180);
  myservo.write(val);*/
  if(distance >= 5){
    moveRobot(500,200,true,true);
  }
  else if(distance <= 5){
      moveRobot(0,0,true,true);
 }

}
 
//Fonction qui set le moteur1
void SetMotor1(int speed, boolean reverse)
{
  analogWrite(motor1_enablePin, speed);
  digitalWrite(motor1_in1Pin, reverse);
  digitalWrite(motor1_in2Pin, reverse);
}

void moveRobot(int speedMotor1, int speedMotor2, boolean reverseMotor1, boolean reverseMotor2 ){
  SetMotor1(speedMotor1, reverseMotor1);
  SetMotor2(speedMotor2, reverseMotor2);
}


 
//Fonction qui set le moteur2
void SetMotor2(int speed, boolean reverse)
{
  analogWrite(motor2_enablePin, speed);
  digitalWrite(motor2_in1Pin, reverse);
  digitalWrite(motor2_in2Pin, reverse);
}
