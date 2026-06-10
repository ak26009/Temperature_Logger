🌡️ 7 Sensor Temperature Monitoring System

A real-time temperature monitoring and data logging system using ESP32 and 7 DS18B20 Temperature Sensors. The system continuously acquires temperature data from multiple sensors, transmits it via serial communication, and visualizes the readings through a Python-based GUI dashboard with live graphs, status monitoring, and CSV logging.

🚀 Features
* Real-time monitoring of 7 DS18B20 temperature sensors
* ESP32-based data acquisition
* Live temperature dashboard using PyQt5
* Real-time graphical visualization using PyQtGraph
* Automatic CSV data logging
* Temperature alarm indication (outside 20°C–25°C range)
* Serial communication with ESP32
* Secure login screen
* Export logged data to CSV

## 🛠️ Hardware Requirements

* ESP32 Development Board
* 7 × DS18B20 Temperature Sensors
* USB Cable
* Breadboard / Wiring Setup
* Jumper Wires

---
## ⚙️ Installation
## 1. Clone the repository

git clone https://github.com/yourusername/7-Sensor-Temperature-Monitoring-System.git
cd 7-Sensor-Temperature-Monitoring-System

## 2. Install dependencies
pip install -r requirements.txt

## 3. Run the application
python temperature_logger.py
## 4. Upload the Arduino code to ESP32 and connect the board via USB.

## 📌 Sensor Connections

| Sensor   | ESP32 GPIO |
| -------- | ---------- |
| Sensor 1 | GPIO32     |
| Sensor 2 | GPIO33     |
| Sensor 3 | GPIO15     |
| Sensor 4 | GPIO5      |
| Sensor 5 | GPIO4      |
| Sensor 6 | GPIO14     |
| Sensor 7 | GPIO12     |

### Wiring

Each DS18B20 sensor is connected directly to an ESP32 GPIO pin and powered using the ESP32's 3.3V supply.

```text
DS18B20      ESP32
---------------------
VCC    --->  3.3V
GND    --->  GND
DATA   --->  GPIO Pin
```

### Pull-Up Configuration

This project uses the ESP32's internal pull-up resistors through the following configuration:

```cpp
pinMode(PINx, INPUT_PULLUP);
```

No external pull-up resistors are required for the current implementation.

## 🔐 Authentication

The login credentials can be configured directly in the Python source code if authentication is required.
In this section 
  
##  if (
##    username == "admin"
##    and password == "admin123"
## ):
