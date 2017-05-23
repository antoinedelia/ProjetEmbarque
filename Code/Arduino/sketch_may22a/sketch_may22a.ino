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
 
void setup()
{
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
 
void loop()
{
 // ARDUINO MUST BE ON THE BACK
  SetMotor2(175, true); // Devant gauche
  SetMotor1(255, false); // Devant droit
  SetMotor4(175, true); // Derrière droit
  SetMotor3(255, false); // Derrière gauche
 
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
