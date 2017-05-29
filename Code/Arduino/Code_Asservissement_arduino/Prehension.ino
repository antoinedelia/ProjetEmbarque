void ActivateMagnet()
{
  Serial.println("Activate magnet");
  digitalWrite(electroaimant, HIGH);
  delay(1000);
  servoMagnet.write(0);
}

void DisableMagnet()
{
  Serial.println("Deactivate magnet");
  digitalWrite(electroaimant, LOW);
  delay(1000);
  servoMagnet.write(90);
}
