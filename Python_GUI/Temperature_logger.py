# 7 SENSOR TEMPERATURE MONITORING SYSTEM
# rewrite the code removing the retearn details

import sys
import csv
import shutil
import serial
import serial.tools.list_ports
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGridLayout, QFileDialog,
    QMessageBox, QFrame, QLineEdit
)

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

import pyqtgraph as pg


# =========================================================
# SENSOR CARD
# =========================================================
class SensorCard(QFrame):

    def __init__(self, name, color):
        super().__init__()

        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1E293B;
                border: 2px solid {color};
                border-radius: 15px;
            }}
        """)

        layout = QVBoxLayout()

        # SENSOR NAME
        self.title = QLabel(name)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 13, QFont.Bold))
        self.title.setStyleSheet(f"""
            color:{color};
        """)

        # TEMPERATURE VALUE
        self.value = QLabel("-- Â°C")
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setFont(QFont("Arial", 22, QFont.Bold))
        self.value.setStyleSheet("""
            color:white;
        """)

        # STATUS
        self.status = QLabel("â— WAITING")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("""
            color:#00FF99;
            font-size:12px;
            font-weight:bold;
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.value)
        layout.addWidget(self.status)

        self.setLayout(layout)

    # =====================================================
    # UPDATE VALUE
    # =====================================================
    def update_value(self, temp):

        self.value.setText(f"{temp:.2f} Â°C")

        # ALARM RANGE
        if temp < 20 or temp > 25:

            self.status.setText("â— ALARM")

            self.status.setStyleSheet("""
                color:red;
                font-size:12px;
                font-weight:bold;
            """)

        else:

            self.status.setText("â— NORMAL")

            self.status.setStyleSheet("""
                color:#00FF99;
                font-size:12px;
                font-weight:bold;
            """)


# =========================================================
# MAIN DATA LOGGER
# =========================================================
class DataLogger(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "7 Sensor Temperature Monitoring System"
        )

        self.resize(1600, 950)

        # =================================================
        # SENSOR NAMES
        # =================================================
        self.sensor_names = [
    "Sensor 1",
    "Sensor 2",
    "Sensor 3",
    "Sensor 4",
    "Sensor 5",
    "Sensor 6",
    "Sensor 7"
]

        # =================================================
        # STYLE
        # =================================================
        self.setStyleSheet("""

            QWidget {
                background-color: #0F172A;
                color: white;
                font-family: Arial;
            }

            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3B82F6;
            }

            QComboBox {
                background-color: #1E293B;
                border: 1px solid #334155;
                padding: 8px;
                border-radius: 8px;
                color: white;
            }
        """)

        main_layout = QVBoxLayout()

        # =================================================
        # HEADER
        # =================================================
        header = QLabel(
            "TEMPERATURE DATA LOGGER"
        )

        header.setAlignment(Qt.AlignCenter)

        header.setFont(
            QFont("Arial", 24, QFont.Bold)
        )

        header.setStyleSheet("""
            color:#38BDF8;
            background:#111827;
            padding:15px;
            border-radius:15px;
        """)

        main_layout.addWidget(header)

        # =================================================
        # SYSTEM STATUS
        # =================================================
        self.system_status = QLabel(
            "SYSTEM READY"
        )

        self.system_status.setAlignment(Qt.AlignCenter)

        self.system_status.setStyleSheet("""
            background:#111827;
            color:#00FF99;
            padding:10px;
            border-radius:10px;
            font-size:14px;
            font-weight:bold;
        """)

        main_layout.addWidget(self.system_status)

        # =================================================
        # TOP CONTROLS
        # =================================================
        top_layout = QHBoxLayout()

        self.port_box = QComboBox()

        self.refresh_ports()

        self.refresh_btn = QPushButton("ðŸ”„ Refresh")
        self.connect_btn = QPushButton("ðŸ”Œ Connect")
        self.start_btn = QPushButton("â–¶ Start")
        self.stop_btn = QPushButton("â¹ Stop")
        self.export_btn = QPushButton("ðŸ“¥ Export CSV")

        self.refresh_btn.clicked.connect(
            self.refresh_ports
        )

        self.connect_btn.clicked.connect(
            self.connect_serial
        )

        self.start_btn.clicked.connect(
            self.start_logging
        )

        self.stop_btn.clicked.connect(
            self.stop_logging
        )

        self.export_btn.clicked.connect(
            self.export_csv
        )

        top_layout.addWidget(self.port_box)
        top_layout.addWidget(self.refresh_btn)
        top_layout.addWidget(self.connect_btn)
        top_layout.addWidget(self.start_btn)
        top_layout.addWidget(self.stop_btn)
        top_layout.addWidget(self.export_btn)

        main_layout.addLayout(top_layout)

        # =================================================
        # SENSOR GRID
        # =================================================
        grid = QGridLayout()

        colors = [
            "#EF4444",
            "#22C55E",
            "#3B82F6",
            "#FACC15",
            "#A855F7",
            "#14B8A6",
            "#F97316"
        ]

        self.sensors = []

        for i in range(7):

            sensor = SensorCard(
                self.sensor_names[i],
                colors[i]
            )

            self.sensors.append(sensor)

        positions = [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (1, 1),
            (1, 2)
        ]

        for sensor, pos in zip(
                self.sensors,
                positions):

            grid.addWidget(sensor, *pos)

        main_layout.addLayout(grid)

        # =================================================
        # GRAPH
        # =================================================
        self.graph = pg.PlotWidget()

        self.graph.setBackground("#111827")

        self.graph.showGrid(
            x=True,
            y=True
        )

        self.graph.setTitle(
            "REAL-TIME TEMPERATURE MONITORING",
            color="w",
            size="16pt"
        )

        self.graph.setLabel(
            "left",
            "Temperature (Â°C)"
        )

        self.graph.setLabel(
            "bottom",
            "Samples"
        )

        self.graph.addLegend()

        graph_colors = [
            (255, 80, 80),
            (0, 255, 140),
            (0, 170, 255),
            (255, 220, 0),
            (200, 0, 255),
            (0, 255, 255),
            (255, 120, 0)
        ]

        self.curves = []

        for i, c in enumerate(graph_colors):

            curve = self.graph.plot(
                pen=pg.mkPen(
                    color=c,
                    width=3
                ),
                name=self.sensor_names[i]
            )

            self.curves.append(curve)

        main_layout.addWidget(self.graph)

        self.setLayout(main_layout)

        # =================================================
        # SERIAL
        # =================================================
        self.ser = None

        # =================================================
        # TIMER
        # =================================================
        self.timer = QTimer()

        self.timer.timeout.connect(
            self.read_serial
        )

        # =================================================
        # DATA STORAGE
        # =================================================
        self.history = [[] for _ in range(7)]

        self.max_points = 100

        self.current_temps = [0] * 7

        # =================================================
        # CSV
        # =================================================
        self.filename = "temperature_log.csv"

        self.file = open(
            self.filename,
            "a",
            newline=""
        )

        self.writer = csv.writer(self.file)

        if self.file.tell() == 0:

            self.writer.writerow(
                ["Timestamp"] +
                self.sensor_names
            )

    # =====================================================
    # REFRESH PORTS
    # =====================================================
    def refresh_ports(self):

        self.port_box.clear()

        ports = serial.tools.list_ports.comports()

        for port in ports:

            self.port_box.addItem(
                port.device
            )

    # =====================================================
    # CONNECT SERIAL
    # =====================================================
    def connect_serial(self):

        port = self.port_box.currentText()

        try:

            self.ser = serial.Serial(
                port,
                115200,
                timeout=1
            )

            self.system_status.setText(
                f"CONNECTED TO {port}"
            )

            QMessageBox.information(
                self,
                "CONNECTED",
                f"Connected to {port}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "ERROR",
                str(e)
            )

    # =====================================================
    # START LOGGING
    # =====================================================
    def start_logging(self):

        if not self.ser:

            QMessageBox.warning(
                self,
                "WARNING",
                "Connect device first"
            )

            return

        self.timer.start(300)

        self.system_status.setText(
            "DATA LOGGING STARTED"
        )

    # =====================================================
    # STOP LOGGING
    # =====================================================
    def stop_logging(self):

        self.timer.stop()

        self.system_status.setText(
            "DATA LOGGING STOPPED"
        )

    # =====================================================
    # EXPORT CSV
    # =====================================================
    def export_csv(self):

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV",
            "",
            "CSV Files (*.csv)"
        )

        if path:

            shutil.copy(
                self.filename,
                path
            )

            QMessageBox.information(
                self,
                "SUCCESS",
                "CSV EXPORTED"
            )

    # =====================================================
    # READ SERIAL
    # =====================================================
    def read_serial(self):

        try:

            if self.ser and self.ser.in_waiting:

                line = self.ser.readline() \
                    .decode(errors="ignore") \
                    .strip()

                print(line)

                # CHECK SENSOR DATA
                if "Sensor" in line and ":" in line:

                    try:

                        # SENSOR NUMBER
                        sensor_part = line.split(":")[0]

                        sensor_num = int(
                            sensor_part.split("(")[0]
                            .replace("Sensor", "")
                        ) - 1

                        # TEMPERATURE
                        value_part = line.split(":")[1]

                        value = value_part \
                            .replace("Â°C", "") \
                            .strip()

                        if "ERROR" in value:
                            return

                        temp = float(value)

                        # UPDATE SENSOR CARD
                        self.sensors[sensor_num] \
                            .update_value(temp)

                        # STORE TEMP
                        self.current_temps[
                            sensor_num
                        ] = temp

                        # UPDATE HISTORY
                        self.history[sensor_num] \
                            .append(temp)

                        # LIMIT GRAPH
                        if len(
                            self.history[sensor_num]
                        ) > self.max_points:

                            self.history[
                                sensor_num
                            ].pop(0)

                        # UPDATE GRAPH
                        self.curves[sensor_num] \
                            .setData(
                                self.history[
                                    sensor_num
                                ]
                            )

                        # SAVE CSV AFTER SENSOR 7
                        if sensor_num == 6:

                            timestamp = datetime.now() \
                                .strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                )

                            self.writer.writerow(
                                [timestamp] +
                                self.current_temps
                            )

                            self.file.flush()

                    except Exception as e:

                        print(
                            "PARSE ERROR:",
                            e
                        )

        except Exception as e:

            self.system_status.setText(
                f"ERROR : {str(e)}"
            )

            self.stop_logging()

    # =====================================================
    # CLOSE EVENT
    # =====================================================
    def closeEvent(self, event):

        if self.ser:
            self.ser.close()

        self.file.close()

        event.accept()


# =========================================================
# LOGIN WINDOW
# =========================================================
class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Secure Login"
        )

        self.setFixedSize(450, 320)

        self.setStyleSheet("""

            QWidget {
                background-color: #0F172A;
                color: white;
                font-family: Arial;
            }

            QLineEdit {
                background-color: #1E293B;
                border: 2px solid #334155;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }

            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3B82F6;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel(
            "LOGIN SYSTEM"
        )

        title.setAlignment(Qt.AlignCenter)

        title.setFont(
            QFont("Arial", 22, QFont.Bold)
        )

        title.setStyleSheet("""
            color:#38BDF8;
            padding:20px;
        """)

        # USERNAME
        self.username = QLineEdit()

        self.username.setPlaceholderText(
            "Enter Username"
        )

        # PASSWORD
        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Enter Password"
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )

        # LOGIN BUTTON
        self.login_btn = QPushButton(
            "ðŸ” LOGIN"
        )

        self.login_btn.clicked.connect(
            self.check_login
        )

        # STATUS
        self.status = QLabel("")

        self.status.setAlignment(Qt.AlignCenter)

        layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.status)

        layout.addStretch()

        self.setLayout(layout)

    # =====================================================
    # LOGIN CHECK
    # =====================================================
    def check_login(self):

        username = self.username.text()

        password = self.password.text()

        if (
            username == "admin"
            and password == "admin123"
        ):

            self.status.setText(
                "LOGIN SUCCESS"
            )

            self.status.setStyleSheet("""
                color:#00FF99;
                font-size:14px;
                font-weight:bold;
            """)

            self.main_window = DataLogger()

            self.main_window.show()

            self.close()

        else:

            self.status.setText(
                "INVALID USERNAME OR PASSWORD"
            )

            self.status.setStyleSheet("""
                color:red;
                font-size:14px;
                font-weight:bold;
            """)


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":

    app = QApplication(sys.argv)

    pg.setConfigOptions(
        antialias=True
    )

    login = LoginWindow()

    login.show()

    sys.exit(app.exec_())
