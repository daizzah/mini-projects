from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import paho.mqtt.client as mqtt
import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sensor_data = ""
        self.parking_data = {}
        self.setupUi(self)

        self.off_button.clicked.connect(self.off_button_click)
        self.on_button.clicked.connect(self.on_button_click)
        self.send_button.clicked.connect(self.send_button_click)
        self.checkboxes = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5]

        for checkbox in self.checkboxes:
            checkbox.setEnabled(False)

        self.setStyleSheet("""
            QWidget {
                background-color: #ffe6e9;
                font-family: 'Poppins';
            }
            QPushButton {
                background-color: #ff7e95;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff5e7a;
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #d6a4b2;
                border-radius: 10px;
                padding: 8px;
            }
            QCheckBox {
                width: 20px;
                height: 20px;
            }
            QLabel {
                color: #3c3648;
                font-size: 18pt;
                font-weight: bold;
            }
            QFrame {
                background-color: white;
                border: 2px solid #3c3648;
                border-radius: 4px;
            }
        """)

        # Create a QTimer to update the text at regular intervals
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_sensor_text)
        self.update_timer.start(1000)  # Set the interval in milliseconds (e.g., 1000 milliseconds = 1 second)
        self.mqttBroker = "broker.hivemq.com"

        # Subscribe to sensor and parking data
        self.subscribe_sensor_mqtt()
        self.subscribe_parking_mqtt()

        self.light_data = "OFF"
        self.client = mqtt.Client("ui_client")  
        self.client.connect(self.mqttBroker)

    def on_sensor_message(self, client, userdata, message):
        self.sensor_data = message.payload.decode("utf-8")

    def subscribe_sensor_mqtt(self):
        sensor_client = mqtt.Client("sensor_client")
        sensor_client.connect(self.mqttBroker)

        sensor_client.on_message = self.on_sensor_message
        sensor_client.subscribe("sensor_dcb772")  # Subscribe to sensor data
        sensor_client.loop_start()

    def update_sensor_text(self):
        # Update the text in the QTextEdit widget
        self.sensor_textbox.setText(self.sensor_data)

    def update_checkboxes(self):
        for checkbox, (space, availability) in zip(self.checkboxes, self.parking_data.items()):
            checkbox.setChecked(availability == 0)

    def on_parking_message(self, client, userdata, message):
        self.parking_data = json.loads(message.payload.decode("utf-8"))
        self.update_checkboxes()

    def subscribe_parking_mqtt(self):
        parking_client = mqtt.Client("parking_client")
        parking_client.connect(self.mqttBroker)

        parking_client.on_message = self.on_parking_message
        parking_client.subscribe("parking_dcb772")  # Replace with your actual parking topic
        parking_client.loop_start()

    def send_button_click(self):
        # Sends the text input from the GUI to RPi terminal
        text_from_display = self.display_textbox.toPlainText()
        self.client.publish("display_dcb772", text_from_display)

    def off_button_click(self):
        # When clicked, the warning light/LED turns off
        # print("Off Button Clicked!")
        self.light_data = "OFF"
        self.client.publish("light_dcb772", self.light_data)

    def on_button_click(self): 
        # When clicked, the warning light/LED should flash continuously 
        # print("On Button Clicked!")
        self.light_data = "ON"
        self.client.publish("light_dcb772", self.light_data)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(500, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.parking_label = QtWidgets.QLabel(self.centralwidget)
        self.parking_label.setGeometry(QtCore.QRect(100, 20, 300, 40))
        self.parking_label.setAlignment(QtCore.Qt.AlignCenter)
        self.parking_label.setText("Parking System")

        # checkboxes
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(70, 80, 16, 20))
        self.checkBox.setObjectName("checkBox")

        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(110, 80, 16, 20))
        self.checkBox_2.setObjectName("checkBox_2")

        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(150, 80, 16, 20))
        self.checkBox_3.setObjectName("checkBox_3")

        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(190, 80, 16, 20))
        self.checkBox_4.setObjectName("checkBox_4")

        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(230, 80, 16, 20))
        self.checkBox_5.setObjectName("checkBox_5")

        # frames (optional visuals under checkboxes)
        self.frames = []
        x_positions = [70, 110, 150, 190, 230]
        for x in x_positions:
            frame = QtWidgets.QFrame(self.centralwidget)
            frame.setGeometry(QtCore.QRect(x - 8, 105, 30, 50))
            frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Plain)
            self.frames.append(frame)

        self.on_button = QtWidgets.QPushButton("ON", self.centralwidget)
        self.on_button.setGeometry(QtCore.QRect(350, 80, 100, 40))

        self.off_button = QtWidgets.QPushButton("OFF", self.centralwidget)
        self.off_button.setGeometry(QtCore.QRect(350, 130, 100, 40))

        self.sensor_label = QtWidgets.QLabel("Sensor Data", self.centralwidget)
        self.sensor_label.setGeometry(QtCore.QRect(50, 180, 170, 30))
        self.sensor_label.setAlignment(QtCore.Qt.AlignCenter)

        self.display_label = QtWidgets.QLabel("Display Board", self.centralwidget)
        self.display_label.setGeometry(QtCore.QRect(260, 180, 170, 30))
        self.display_label.setAlignment(QtCore.Qt.AlignCenter)

        self.sensor_textbox = QtWidgets.QTextEdit(self.centralwidget)
        self.sensor_textbox.setGeometry(QtCore.QRect(50, 220, 170, 90))
        self.sensor_textbox.setReadOnly(True)
        self.sensor_textbox.setObjectName("sensor_textbox")

        self.display_textbox = QtWidgets.QTextEdit(self.centralwidget)
        self.display_textbox.setGeometry(QtCore.QRect(260, 220, 170, 90))
        self.display_textbox.setObjectName("display_textbox")

        self.send_button = QtWidgets.QPushButton("Send", self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(200, 320, 100, 35))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.on_button.setText(_translate("MainWindow", "ON"))
        self.off_button.setText(_translate("MainWindow", "OFF"))
        self.sensor_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#3c3648;\">Sensor Data</span></p></body></html>"))
        self.display_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#3c3648;\">Display Board</span></p><p align=\"center\"><br/></p></body></html>"))
        self.parking_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:pt; font-weight:600; color:#3c3648;\">Parking System</span></p></body></html>"))
        self.send_button.setText(_translate("MainWindow", "Send"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
