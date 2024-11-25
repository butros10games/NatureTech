#!/usr/bin/env python3

import socket

import requests
from bluepy.btle import Scanner


# Function to get the local IP address
def get_local_ip():
    try:
        # Create a socket connection to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to Google's public DNS server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return None


# Get the local WLAN IP address
local_ip = get_local_ip()
hostname = socket.gethostname()

while True:
    try:
        # 10.0 sec scanning
        ble_list = Scanner().scan(10.0)
        BLE_count = len(ble_list)  # count of scanned BLE addresses
        for dev in ble_list:
            name = str(dev.rawData).split("\\t")
            if len(name) > 1:
                name = name[1][:-1]
                if "\\" in name:
                    name = None
            else:
                name = None
                print(f"rssi: {dev.rssi} ; mac: {dev.addr} ; Name: {name}")

            # Send data to the server
            server_url = f"https://boer-admin.butrosgroot.com/api/ble/{local_ip}/{hostname}/{dev.rssi}/{dev.addr}/{name}/{BLE_count}"
            # server_url = f"https://boer-admin.butrosgroot.com/api/ble/{local_ip}/{dev.addr}"

            response = requests.get(server_url)
            print(f"Server Response: {response.text}")
            print(
                f"Number of scanned BLE addresses: {BLE_count}, IP: {local_ip}, Hostname: {hostname}"
            )  # print the count

    except Exception as e:
        print(f"Error occurred: {e}")
