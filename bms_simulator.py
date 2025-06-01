# bms_simulator.py
# Simulates a basic Battery Management System with dummy data generation and fault injection

import random
import time
import csv
from datetime import datetime

def simulate_bms_data():
    voltage = round(random.uniform(320.0, 400.0), 2)
    current = round(random.uniform(-100.0, 100.0), 2)
    temperature = round(random.uniform(15.0, 45.0), 2)
    soc = round(random.uniform(20.0, 100.0), 2)

    status = "OK"
    if voltage > 390.0:
        status = "FAULT: Overvoltage"
    elif voltage < 330.0:
        status = "FAULT: Undervoltage"
    elif abs(current) > 90.0:
        status = "FAULT: Overcurrent"
    elif temperature > 40.0:
        status = "FAULT: Overtemperature"
    
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'soc': soc,
        'voltage': voltage,
        'current': current,
        'temperature': temperature,
        'status': status
    }
    
def log_to_csv(data, filename='bms_log.csv'):
    file_exists = False
    try:
        with open(filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
       pass

    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
        
def stream_data(interval=1, iterations=10):
    for _ in range(iterations):
        data = simulate_bms_data()
        print(f"{data['timestamp']} | SOC: {data['soc']}%, Voltage: {data['voltage']}V, Current: {data['current']}A, Temp: {data['temperature']}C | STATUS: {data['status']}")
        log_to_csv(data)
        time.sleep(interval)

if __name__ == "__main__":
    stream_data()
