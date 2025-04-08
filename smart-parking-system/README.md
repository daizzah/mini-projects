# Smart Parking System 🚗

This project simulates an IoT-based smart parking system using Python, PyQt5, MQTT, and a Raspberry Pi. It includes a client dashboard application and a Raspberry Pi script to detect and transmit parking slot availability in real-time.

---

## 📁 Folder Structure

```
smart-parking-system/
│
├── parking_dashboard.py       # PyQt5 GUI application with MQTT integration
├── iot_parking_pi.py          # Raspberry Pi script reading sensor data and sending MQTT messages
├── README.md                  # Project description and usage guide
├── assignment.pdf             # Original assignment instructions and requirements
```

---

## 💡 Features

- Live slot detection using simulated sensors (via jumper wires or IR)
- MQTT-based real-time updates between Raspberry Pi and GUI
- Dashboard showing:
  - Occupied/available slots (via checkboxes)
  - Sensor data feed
  - Display board messaging (Send/On/Off)
- Styled interface with PyQt5
- Fully automatic updates — no manual refresh required

---

## 🧠 How It Works

- **Sensor Simulation**: Each parking slot is represented by an IR sensor connected to a Raspberry Pi. In the actual setup, when a jumper wire is connected (or something blocks the IR sensor), it simulates a car occupying the slot.
- **Automatic Updates**: The Raspberry Pi reads these sensor states and publishes the slot data via MQTT in real-time.
- **Dashboard Display**: The PyQt5 dashboard application receives the data through MQTT and automatically updates the checkboxes and status messages (e.g., “Slots occupied: 1, 3”).

---

## 🚀 How to Run

### Requirements

- Python 3
- `paho-mqtt`
- `PyQt5`
- Raspberry Pi (or mock data with dummy script)

### On Raspberry Pi:

```bash
python3 iot_parking_pi.py
```

### On Client Machine:

```bash
python3 parking_dashboard.py
```

Make sure both devices are connected to the internet and using the same MQTT broker (`broker.hivemq.com` is used in the code).

---

## 📄 Assignment Context

This project was completed as part of the CME466 Design Project course. The original assignment PDF has been renamed to `assignment.pdf` and included for reference.

---

## 📬 MQTT Topics Used

- `sensor_dcb772` — for sensor data (occupied slots)
- `parking_dcb772` — for parking space availability
- `light_dcb772` — for ON/OFF commands
- `display_dcb772` — for custom dashboard display messages

---

## 🎨 UI Preview

The dashboard interface shows the system status in real-time:

- ✅ Checkboxes for each slot
- 📋 Text areas for sensor and display board
- 🔘 Buttons to simulate display control

---

## 📌 Notes

- The GUI design intentionally stays simple and readable for demo/interview clarity.
- UI and sensor logic are modular and can be extended to more parking slots.

---

## 👩‍💻 Author

Daizzah Botoy
