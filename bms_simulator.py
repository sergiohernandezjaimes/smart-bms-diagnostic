# bms_simulator.py
# Simulates a basic Battery Management System with dummy data generation

import random
import time

def simulate_bms_data():
    return {
        'soc': round(random.uniform(20.0, 100.0), 2),  # State of Charge
        'voltage': round(random.uniform(320.0, 400.0), 2),
        'current': round(random.uniform(-100.0, 100.0), 2),
        'temperature': round(random.uniform(15.0, 45.0), 2)
    }

def stream_data(interval=1):
    while True:
        data = simulate_bms_data()
        print(f"SOC: {data['soc']}%, Voltage: {data['voltage']}V, Current: {data['current']}A, Temp: {data['temperature']}C")
        time.sleep(interval)

if __name__ == "__main__":
    stream_data()
