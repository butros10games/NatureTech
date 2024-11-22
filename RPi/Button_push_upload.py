#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from datetime import datetime
import requests
import socket
import sys  # Import sys module for exit()


# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the button
button_pin = 4

# Setup the button pin as an input with a pull-up resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize the variable to store the previous state of the button
prev_button_state = GPIO.input(button_pin)


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


try:
    while True:
        # Read the current state of the button
        button_state = GPIO.input(button_pin)

        # Check if the button state has changed
        if button_state != prev_button_state:
            if button_state == GPIO.LOW:
                print("Button is pressed (closed)")
                print(f"{button_state}")
                server_url = (
                    f"https://boer.butrosgroot.com/api/btn/{local_ip}/{button_state}"
                )

            else:
                print("Button is released (open)")
                print(f"{button_state}")
                server_url = (
                    f"https://boer.butrosgroot.com/api/btn/{local_ip}/{button_state}"
                )

            # Update the previous button state
            prev_button_state = button_state

        # Add a small delay to debounce the button
        time.sleep(0.1)


except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    # Cleanup GPIO settings
    GPIO.cleanup()
