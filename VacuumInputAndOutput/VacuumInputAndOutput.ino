int analogReadPin = A0; // Analog pin to read the input voltage
int analogWritePin = 3; // Analog pin to write the output voltage

int oldSetValue=1;

void setup() {
  Serial.begin(9600);
  pinMode(analogReadPin, INPUT);
  pinMode(analogWritePin, OUTPUT);
}

void loop() {
  // Read the input analog value
  int sensorValue = analogRead(analogReadPin);
  
  // Send the analog value to the serial port
  //Serial.println(sensorValue);
  
  Serial.println(sensorValue);
  
  // Wait for a command from the serial port to set the analog output voltage
  if (Serial.available() > 0) {
    // Read the incoming command
    int voltageValue = Serial.parseInt();
    
    // Set the analog output voltage on the specified pin
    if((voltageValue!=oldSetValue) && (voltageValue!=0)){
      analogWrite(analogWritePin, voltageValue);
      oldSetValue=voltageValue;
    }
    
    
  }
  delay(1000);
}