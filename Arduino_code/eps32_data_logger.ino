#include <OneWire.h>

#define PIN1 32
#define PIN2 33
#define PIN3 15
#define PIN4 5
#define PIN5 4
#define PIN6 14
#define PIN7 12

#define LOW_ALARM 20
#define HIGH_ALARM 25

OneWire ds1(PIN1);
OneWire ds2(PIN2);
OneWire ds3(PIN3);
OneWire ds4(PIN4);
OneWire ds5(PIN5);
OneWire ds6(PIN6);
OneWire ds7(PIN7);

void setup() {
    Serial.begin(115200);

    pinMode(PIN1, INPUT_PULLUP);
    pinMode(PIN2, INPUT_PULLUP);
    pinMode(PIN3, INPUT_PULLUP);
    pinMode(PIN4, INPUT_PULLUP);
    pinMode(PIN5, INPUT_PULLUP);
    pinMode(PIN6, INPUT_PULLUP);
    pinMode(PIN7, INPUT_PULLUP);

    Serial.println("===== 7x DS18B20 System Started =====");
}

// Read DS18B20 Temperature
float readDS18B20(OneWire &ds) {

    byte data[9];
    byte addr[8];

    if (!ds.search(addr)) {
        ds.reset_search();
        return -1000;
    }

    if (OneWire::crc8(addr, 7) != addr[7]) {
        return -2000;
    }

    // Start temperature conversion
    ds.reset();
    ds.select(addr);
    ds.write(0x44, 1);

    delay(750);

    // Read scratchpad
    ds.reset();
    ds.select(addr);
    ds.write(0xBE);

    for (int i = 0; i < 9; i++) {
        data[i] = ds.read();
    }

    int16_t raw = (data[1] << 8) | data[0];
    float temp = (float)raw / 16.0;

    ds.reset_search();

    return temp;
}

// Print temperature
void printSensor(const char *name, float temp) {

    if (temp < -100) {
        Serial.print(name);
        Serial.println(" : ERROR");
        return;
    }

    Serial.print(name);
    Serial.print(" : ");
    Serial.print(temp);
    Serial.print(" °C");

    if (temp < LOW_ALARM || temp > HIGH_ALARM) {
        // Alarm condition
    }

    Serial.println();
}

void loop() {

    float t1 = readDS18B20(ds1);
    float t2 = readDS18B20(ds2);
    float t3 = readDS18B20(ds3);
    float t4 = readDS18B20(ds4);
    float t5 = readDS18B20(ds5);
    float t6 = readDS18B20(ds6);
    float t7 = readDS18B20(ds7);

    Serial.println("\n----- Temperature Readings -----");

    printSensor("Sensor1(GPIO32)", t1);
    printSensor("Sensor2(GPIO33)", t2);
    printSensor("Sensor3(GPIO15)", t3);
    printSensor("Sensor4(GPIO5)", t4);
    printSensor("Sensor5(GPIO4)", t5);
    printSensor("Sensor6(GPIO14)", t6);
    printSensor("Sensor7(GPIO12)", t7);

    Serial.println("-------------------------------");

    delay(2000);
}
