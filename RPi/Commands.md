Scan for BT devices:
```bash
hcitool scan
```
https://raspberry-projects.com/pi/pi-operating-systems/raspbian/bluetooth/bluetooth-commands


Scan for BLE devices:
```bash
sudo hcitool lescan            
```
https://elinux.org/RPi_Bluetooth_LE


Showing the hex code of all the scanned signals:
``` bash
sudo hcidump
```
If name is unkown it will say "unknown type"
If the name is known/transmitted it will say "Complete local name: 'The name'"


Showing the hex code of all the scanned signals:
``` bash
sudo hcidump --raw
```
This includes the RSSI