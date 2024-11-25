#!/usr/bin/env python3

# To test with button, Connect 1 pin with the +5V and the other on the PIR pin (14 in this case)

import socket
import sys  # Import sys module for exit()
from datetime import datetime
from signal import pause

import requests
from gpiozero import MotionSensor

pir = MotionSensor(14)


def motion_function():  # if motion detected print
    print("Motion Detected")


def no_motion_function():  # if stopped detecting motion print
    print("Motion stopped")


pir.when_motion = motion_function
pir.when_no_motion = no_motion_function

pause()
