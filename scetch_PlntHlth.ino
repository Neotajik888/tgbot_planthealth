const int moistureSensorPin = A0;    // Датчик влажности почвы
const int lightSensorPin = A1;       // Датчик освещенности

const int airValue = 520;    // Значение в воздухе (сухой датчик)
const int waterValue = 260;  // Значение в воде (полностью влажный)
const int moistureMin = 0;   // Минимальный процент влажности
const int moistureMax = 100; // Максимальный процент влажности

const int darkValue = 800;     // Значение в полной темноте
const int brightValue = 50; // Значение при ярком свете

const bool invertLightScale = true;

const unsigned long readInterval = 2000;
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(9600);
  
  pinMode(moistureSensorPin, INPUT);
  pinMode(lightSensorPin, INPUT);
  
  delay(100);
  
  Serial.println("====================================");
  Serial.println("Монитор почвы и освещенности");
  Serial.println("Версия 1.5");
  Serial.println("====================================");
  Serial.println("Ожидание данных...");
  Serial.println();
  //calibrateMoistureSensor();
  Serial.println("НАСТРОЙКИ ДАТЧИКА ОСВЕЩЕННОСТИ:");
  Serial.print("Темнота (0%): ");
  Serial.println(darkValue);
  Serial.print("Ярко (100%): ");
  Serial.println(brightValue);
  Serial.print("Инвертированная шкала: ");
  Serial.println(invertLightScale ? "ДА" : "НЕТ");
  Serial.println("====================================");
  Serial.println("Ожидание данных...");
  Serial.println();
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= readInterval) {
    previousMillis = currentMillis;
    
    int moistureRaw = analogRead(moistureSensorPin);
    int moisturePercentage = map(moistureRaw, airValue, waterValue, moistureMin, moistureMax);
    
    moisturePercentage = constrain(moisturePercentage, 0, 100);
    
    int lightRaw = analogRead(lightSensorPin);
    int lightPercentage;
    if (invertLightScale) {
      lightPercentage = map(lightRaw, brightValue, darkValue, 100, 0);
    } else {
      lightPercentage = map(lightRaw, darkValue, brightValue, 0, 100);
    }
    lightPercentage = constrain(lightPercentage, 0, 100);
    
    printSensorData(moistureRaw, moisturePercentage, lightRaw, lightPercentage);
  }
}

void printSensorData(int moistureRaw, int moisturePercent, int lightRaw, int lightPercent) {
  Serial.println("====================================");
  Serial.print("Время: ");
  Serial.print(millis() / 1000);
  Serial.println(" сек");
  Serial.println("------------------------------------");
  
  Serial.println("ДАТЧИК ВЛАЖНОСТИ ПОЧВЫ:");
  Serial.print("Сырое значение: ");
  Serial.println(moistureRaw);
  Serial.print("Влажность: ");
  Serial.print(moisturePercent);
  Serial.println("%");
  
  Serial.print("[");
  for (int i = 0; i < 20; i++) {
    if (i < moisturePercent / 5) {
      Serial.print("█");
    } else {
      Serial.print("░");
    }
  }
  Serial.println("]");
  
  Serial.print("Состояние: ");
  if (moisturePercent >= 80) {
    Serial.println("ОЧЕНЬ ВЛАЖНАЯ");
  } else if (moisturePercent >= 60) {
    Serial.println("ВЛАЖНАЯ");
  } else if (moisturePercent >= 40) {
    Serial.println("НОРМАЛЬНАЯ");
  } else if (moisturePercent >= 20) {
    Serial.println("СУХАЯ");
  } else {
    Serial.println("ОЧЕНЬ СУХАЯ");
  }
  
  Serial.println("------------------------------------");
  
  Serial.println("ДАТЧИК ОСВЕЩЕННОСТИ:");
  Serial.print("Сырое значение: ");
  Serial.println(lightRaw);
  Serial.print("Освещенность: ");
  Serial.print(lightPercent);
  Serial.println("%");
  Serial.print("[");
  for (int i = 0; i < 20; i++) {
    if (i < lightPercent / 5) {
      Serial.print("☀");
    } else {
      Serial.print(" ");
    }
  }
  Serial.println("]");
  Serial.print("Уровень света: ");
  if (lightPercent >= 80) {
    Serial.println("ОЧЕНЬ ЯРКО");
  } else if (lightPercent >= 60) {
    Serial.println("ЯРКО");
  } else if (lightPercent >= 40) {
    Serial.println("СРЕДНЕ");
  } else if (lightPercent >= 20) {
    Serial.println("ТЕМНО");
  } else {
    Serial.println("ОЧЕНЬ ТЕМНО");
  }
  
  Serial.println("====================================");
  Serial.println();
}
void calibrateMoistureSensor() {
  Serial.println("КАЛИБРОВКА ДАТЧИКА ВЛАЖНОСТИ");
  Serial.println("============================");
  Serial.println("1. Поместите датчик в воздух (сухой)");
  Serial.println("2. Нажмите любую клавишу...");
  while (!Serial.available());
  Serial.read();
  int dryValue = analogRead(moistureSensorPin);
  Serial.print("Значение в воздухе: ");
  Serial.println(dryValue);
  
  Serial.println("\n3. Поместите датчик в воду");
  Serial.println("4. Нажмите любую клавишу...");
  while (!Serial.available());
  Serial.read();
  int wetValue = analogRead(moistureSensorPin);
  Serial.print("Значение в воде: ");
  Serial.println(wetValue);
  
  Serial.println("\nКАЛИБРОВКА ЗАВЕРШЕНА!");
  Serial.print("Рекомендуемые значения: airValue = ");
  Serial.print(dryValue);
  Serial.print(", waterValue = ");
  Serial.println(wetValue);
}