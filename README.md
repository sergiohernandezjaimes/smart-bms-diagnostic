# 🔋 Smart BMS Diagnostic

A simple simulation of a Battery Management System (BMS) that generates and logs real-time data - include SOC, voltage, current, and temperature. Usefule for prototyping embedded systems, data pipelines, or AI-powered diagnostic tools.

## 📦 Features


- Simulates BMS metrics using realistic value ranges
- Streams data to the console
- Logs output to a timestamped CSV file
- Modular for future extensions: fault injection, dashboards, diagnostics, etc.

- ## 📁 Files

- `bms_simulator.py` – Core simulation + CSV logger
- `bms_log.csv` – Auto-generated log of real-time sensor data

- ## 🚀 How to Run

```bash
python bms_simulator.py
