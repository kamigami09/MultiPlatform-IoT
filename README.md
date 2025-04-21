# MultiPlatform-IoT
# IoT Multi‑Sensor Platform

Collect environmental data (temperature, humidity, distance) from an **Arduino**, transmit it to a **Raspberry Pi** via I²C, merge it with live **web‑camera frames** from a PC, and publish everything over **MQTT** to a Node.js back‑end that powers a real‑time web dashboard.

---

## Table of Contents
1. [Features](#features)
2. [System Architecture](#system-architecture)
3. [Hardware](#hardware)
4. [Software Stack](#software-stack)
5. [Quick Start](#quick-start)
6. [MQTT Topics](#mqtt-topics)
7. [Project Structure](#project-structure)
8. [Roadmap](#roadmap)
9. [Contributing](#contributing)
10. [License](#license)

---

## Features
- **Multi‑sensor data collection** – temperature & humidity (DHT22) and distance (HC‑SR04) on Arduino.
- **I²C bridge** – reliable, low‑latency transfer from Arduino to Raspberry Pi.
- **Unified MQTT backbone** – Raspberry Pi Node.js server publishes/receives all data.
- **Camera streaming** – PC webcam frames sent to the same broker, enabling a single data pipeline.
- **Live dashboard** – responsive website shows sensor readings & camera feed in real‑time.
- **Modular** – each component runs independently; swap sensors, change brokers, or move UI to another host with minimal edits.

---

## System Architecture
```text
┌──────────┐      I²C       ┌────────────┐        MQTT         ┌───────────────┐
│ Arduino  │──────────────▶│ Raspberry Pi│────────────────────▶│ Node.js Server│
│  DHT22   │               │  Mosquitto  │◀────────────────────┤  (on Pi)      │
│  HC‑SR04 │               └────────────┘        WebSocket     └──────┬────────┘
└──────────┘                                               ┌──────────▼──────────┐
                                                          │   Web Dashboard     │
PC Webcam ──MQTT──────────────────────────────────────────▶│  (React/Vite)       │
                                                          └──────────────────────┘
```

---

## Hardware
| Component | Purpose | Notes |
|-----------|---------|-------|
| **Arduino Uno/Nano** | Sensor acquisition | Connect sensors, run `arduino/IoTPlatform.ino` |
| **DHT22** | Temperature & humidity | 3.3 V or 5 V with pull‑up resistor |
| **HC‑SR04** | Ultrasonic distance | 5 V, voltage divider if Pi uses 3.3 V logic |
| **Raspberry Pi 4 B** | MQTT broker & Node.js server | Enable I²C via `raspi‑config` |
| **PC / Laptop** | Webcam source & camera publisher | Python or Node script |

### Wiring (Arduino → Pi)
```
Arduino SDA (A4) ─── SDA (Pi GPIO 2)
Arduino SCL (A5) ─── SCL (Pi GPIO 3)
GND ─────────────── GND
```

> **Tip:** keep wires under 20 cm for clean I²C signals.

---

## Software Stack
| Layer | Tech | Directory |
|-------|------|-----------|
| Device FW | Arduino (C/C++) | `/arduino` |
| Broker | Mosquitto | installed on Pi |
| Back‑end | Node.js + `mqtt`, `express`, `socket.io` | `/server` |
| Camera Client | Python (OpenCV, paho‑mqtt) **or** Node.js | `/pc-client` |
| Front‑end | React + Vite + Socket.IO client | `/web-dashboard` |

---

## Quick Start
1. **Clone & install**
   ```bash
   git clone https://github.com/your‑user/iot‑platform.git
   cd iot‑platform
   ./scripts/install.sh   # installs server & dashboard deps
   ```
2. **Flash Arduino**
   ```bash
   cd arduino
   open IoTPlatform.ino in Arduino IDE
   upload to board
   ```
3. **Prepare Raspberry Pi**
   ```bash
   sudo raspi‑config      # enable I²C
   sudo apt install mosquitto mosquitto‑clients
   cd server && npm i && npm start
   ```
4. **Run PC camera publisher**
   ```bash
   cd pc-client
   python cam_publisher.py --broker tcp://<pi_ip>:1883
   ```
5. **Open the dashboard**
   ```bash
   cd web-dashboard
   npm i && npm run dev   # or npm run build && serve
   ```
   Navigate to `http://<pi_ip>:5173` (dev) or `http://<pi_ip>` (prod).

---

## MQTT Topics
| Topic | Payload | Publisher |
|-------|---------|-----------|
| `sensors/temperature` | `{ "value": 23.4, "unit": "°C" }` | Arduino → Pi |
| `sensors/humidity` | `{ "value": 56.2, "unit": "%" }` | Arduino → Pi |
| `sensors/distance` | `{ "value": 78.1, "unit": "cm" }` | Arduino → Pi |
| `camera/frame` | JPEG/PNG binary or base64 | PC → Broker |

---

## Project Structure
```
📦iot‑platform
 ├─ arduino/            # Arduino sketch & libs
 ├─ server/             # Node.js REST + MQTT bridge
 ├─ pc-client/          # Webcam publisher
 ├─ web-dashboard/      # React front‑end
 ├─ scripts/            # helper scripts (install, deploy, etc.)
 └─ docs/               # architecture diagrams & notes
```

---

## Roadmap
- [ ] TLS‑secured MQTT & WebSocket
- [ ] Docker compose for one‑command deployment
- [ ] InfluxDB + Grafana for historical data
- [ ] Add more sensors (light, air‑quality)

---

## Contributing
Pull requests are welcome! Please open an issue first to discuss major changes.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## License
Distributed under the MIT License. See `LICENSE` for more information.

---

## Acknowledgements
- [Node‑RED](https://nodered.org/) – inspiration for flow‑based IoT
- [Mosquitto](https://mosquitto.org/) – lightweight broker
- [OpenCV](https://opencv.org/) – camera capture

