#!/usr/bin/env python3

#To test with button, Connect 1 pin with the +5V and the other on the PIR pin (14 in this case)

from gpiozero import MotionSensor
from signal import pause
from datetime import datetime

pir = MotionSensor(14)

def motion_function(): #if motion detected print
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print("Motion Detected")
    print(f"Motion Detected at {current_time}")

def no_motion_function(): #if stopped detecting motion print
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print("Motion stopped")
    print(f"Motion stopped at {current_time}")

pir.when_motion = motion_function
pir.when_no_motion = no_motion_function

pause()
