##This is test code that is broken

#!/usr/bin/env python3

import bluetooth
from bluepy.btle import Scanner, DefaultDelegate
import psycopg2
from datetime import datetime

# PostgreSQL database configuration
DB_HOST = "your_remote_host"
DB_PORT = 5432
DB_NAME = "your_database_name"
DB_USER = "your_database_user"
DB_PASSWORD = "your_database_password"

def scan_bluetooth_devices():
    print("Scanning for Bluetooth devices:")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_oui=True, device_id=-1, device_name='hci0')
    print("Bluetooth devices found:")
    for addr, name, _ in nearby_devices:
        print(f"  {name} ({addr})")

def scan_ble_devices_and_upload_to_database():
    print("Scanning for BLE devices:")
    scanner = Scanner().withDelegate(MyDelegate())
    devices = scanner.scan(10.0)  # Scan for 10 seconds
    print("BLE devices found:")
    
    # Connect to the remote PostgreSQL database
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    for dev in devices:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        device_name = dev.getValueText(9)
        device_address = dev.addr
        rssi = dev.rssi

        print(f"  {device_name} ({device_address}) - RSSI: {rssi}")

        # Insert data into the remote PostgreSQL database
        cursor.execute("INSERT INTO bluetooth_data (timestamp, device_name, device_address, rssi) VALUES (%s, %s, %s, %s)",
                       (timestamp, device_name, device_address, rssi))
    
    # Commit changes and close the database connection
    conn.commit()
    cursor.close()
    conn.close()

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Discovered device: {dev.addr} (name: {dev.getValueText(9)}) - RSSI: {dev.rssi}")

if __name__ == "__main__":
    scan_bluetooth_devices()
    print("\n")
    scan_ble_devices_and_upload_to_database()
