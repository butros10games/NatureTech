#!/usr/bin/env python3
import bluetooth

def scan_bluetooth_devices():
    print("Scanning for Bluetooth devices:")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, device_id=-1)
    print("Bluetooth devices found:")
    for nearby_devices in nearby_devices:
        print(f" nearby_devices {nearby_devices}")

if __name__ == "__main__":
    scan_bluetooth_devices()
