 void forwardRobot(){
  Serial.println("Move forward");
  moveRobot(255, 255, 255, 255, false, true, false, false);
  Serial.print("Millis : ");
  Serial.println(millis());
  delay(2000);
  Serial.print("Millis 2 : ");
  Serial.println(millis());
  Serial.println("Stop robot");
  stopRobot();
}

void backwardRobot(){
  moveRobot(255, 255, 255, 255, true, false, true, true);
  delay(2000);
  stopRobot();
}

void leftRobot(){
  moveRobot(255, 255, 255, 255, false, false, true, false);
  delay(1000);
  stopRobot();
}

void rightRobot(int turns){
  for(int i = 0; i < turns; i++)
  {
    moveRobot(255, 255, 255, 255, true, true, false, true);
    delay(1000);
    stopRobot();
  }
}

void stopRobot()
{
  moveRobot(0, 0, 0, 0, true, true, false, true);
  delay(1000);
}

void moveRobot(int speedMotorFrontRight, int speedMotorFrontLeft, int speedMotorBackLeft, int speedMotorBackRight, boolean reverseMotorFrontRight, boolean reverseMotorFrontLeft, boolean reverseMotorBackLeft, boolean reverseMotorBackRight){
  SetMotor1(speedMotorFrontRight, reverseMotorFrontRight);
  SetMotor2(speedMotorFrontLeft, reverseMotorFrontLeft);
  SetMotor3(speedMotorBackLeft, reverseMotorBackLeft);
  SetMotor4(speedMotorBackRight, reverseMotorBackRight);
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
