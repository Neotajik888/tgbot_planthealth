#include <Wire.h>
const int soilMoisturePin = A0; 
const int lightSensorPin = A1;   
int soilDryValue = 0; 
int soilWetValue = 1023; 
int lightDarkValue = 1023; 
int lightBrightValue = 0;  
const int moistureThreshold = 500;
const int lightThreshold = 500;
void setup() {
  Serial.begin(9600);
  Serial.println("Калибровка датчиков...");
  Serial.println("1. Поместите датчик влажности в воздух (сухой)");
  delay(3000);
  soilDryValue = analogRead(soilMoisturePin);
  Serial.println("2. Поместите датчик влажности в воду");
  delay(3000);
  soilWetValue = analogRead(soilMoisturePin);
  Serial.println("3. Накройте датчик света (темнота)");
  delay(3000);
  lightDarkValue = analogRead(lightSensorPin);
  Serial.println("4. Осветите датчик света (яркий свет)");
  delay(3000);
  lightBrightValue = analogRead(lightSensorPin);
  Serial.println("Калибровка завершена!");
  Serial.print("Сухая почва: "); Serial.println(soilDryValue);
  Serial.print("Мокрая почва: "); Serial.println(soilWetValue);
  Serial.print("Темнота: "); Serial.println(lightDarkValue);
  Serial.print("Свет: "); Serial.println(lightBrightValue);
  delay(2000);
}
void loop() {
  int soilRaw = analogRead(soilMoisturePin);
  int lightRaw = analogRead(lightSensorPin);
  int soilPercent = map(soilRaw, soilDryValue, soilWetValue, 0, 100);
  soilPercent = constrain(soilPercent, 0, 100); // Ограничение 0-100%
  int lightPercent = map(lightRaw, lightDarkValue, lightBrightValue, 0, 100);
  lightPercent = constrain(lightPercent, 0, 100);
  Serial.print("Soil: ");
  Serial.print(soilRaw);
  Serial.print(" (");
  Serial.print(soilPercent);
  Serial.print("%) | Light: ");
  Serial.print(lightRaw);
  Serial.print(" (");
  Serial.print(lightPercent);
  Serial.println("%)");
  delay(100); 
}