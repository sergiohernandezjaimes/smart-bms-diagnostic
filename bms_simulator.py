# bms_simulator.py
# Simulates a basic Battery Management System with dummy data generation

import random
import time
import csv
from datetime import datetime

def simulate_bms_data():
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'soc': round(random.uniform(20.0, 100.0), 2),  # State of Charge
        'voltage': round(random.uniform(320.0, 400.0), 2),
        'current': round(random.uniform(-100.0, 100.0), 2),
        'temperature': round(random.uniform(15.0, 45.0), 2)
    }

def log_to_csv(data, filename='bms_log.csv'):
    file_exists = False
    try:
        with open(filename, 'r') as f:
            file_exists = True
            excpet FileNotFoundError:
            pass

with open(filename, mode= 'a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data.keys())
    if not file_exists:
        writer.writeheader()
        writer.writerow(data)
        
def stream_data(interval=1):
    while True:
        data = simulate_bms_data()
        print(f"{data['timestamp']} | SOC: {data['soc']}%, Voltage: {data['voltage']}V, Current: {data['current']}A, Temp: {data['temperature']}C")
        log_to_csv(data)
        time.sleep(interval)

if __name__ == "__main__":
    stream_data()
