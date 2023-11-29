import bluetooth
from bluepy.btle import Scanner, DefaultDelegate

def scan_bluetooth_devices():
    print("Scanning for Bluetooth devices:")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_oui=True, device_id=-1, device_name='hci0')
    print("Bluetooth devices found:")
    for addr, name, _ in nearby_devices:
        print(f"  {name} ({addr})")

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Discovered device: {dev.addr} (name: {dev.getValueText(9)})")

def scan_ble_devices():
    print("Scanning for BLE devices:")
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)  # Scan for 10 seconds
    print("BLE devices found:")
    for dev in devices:
        print(f"  {dev.addr} (name: {dev.getValueText(9)})")

if __name__ == "__main__":
    scan_bluetooth_devices()
    print("\n")
    scan_ble_devices()
