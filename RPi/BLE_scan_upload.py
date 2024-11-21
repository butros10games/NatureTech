#!/usr/bin/env python3

from bluepy.btle import Scanner

while True:
    try:
        # 10.0 sec scanning
        ble_list = Scanner().scan(10.0)
        for dev in ble_list:
            # print(dir(dev))
            name = str(dev.rawData).split("\\t")
            if len(name) > 1:
                name = name[1][:-1]
                if "\\" in name:
                    name = None
            else:
                name = None
            print(f"rssi: {dev.rssi} ; mac: {dev.addr} ; Name: {name}")
    except Exception as e:
        raise Exception("Error occured in BLE scan: ", e)
