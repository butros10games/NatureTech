#!/usr/bin/env python3

import RPi.GPIO as GPIO  # For contact sensor
import time
import threading
import requests
import socket
from gpiozero import MotionSensor  # For PIR motion
from signal import pause  # For PIR motion
from bluepy.btle import Scanner


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

# Function to handle button presses
def button_handler():
    global prev_button_state  # Declare prev_button_state as global
    try:
        while True:
            # Read the current state of the button
            button_state = GPIO.input(button_pin)

            # Check if the button state has changed
            if button_state != prev_button_state:
                if button_state == GPIO.LOW:
                    print("Button is pressed (closed)")
                    print(f"{button_state}")
                    server_url = f"https://boer.butrosgroot.com/api/btn/{local_ip}/{button_state}"

                else:
                    print("Button is released (open)")
                    print(f"{button_state}")
                    server_url = f"https://boer.butrosgroot.com/api/btn/{local_ip}/{button_state}"

                # Make an HTTP request to the server
                response = requests.get(server_url)

                # Print the server response
                print(f"Server Response: {response.text}")

                # Update the previous button state
                prev_button_state = button_state

            # Add a small delay to debounce the button
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Button handler terminated by user.")
    finally:
        # Cleanup GPIO settings
        GPIO.cleanup()

# Start the button handler in a separate thread
button_thread = threading.Thread(target=button_handler)
button_thread.start()

# Start of PIR section
pir = MotionSensor(14)

def motion_function():  # if motion detected print
    print("Motion Detected")
    PIR_state = 1
    print(f"{PIR_state}")
    server_url = f"https://boer.butrosgroot.com/api/pir/{local_ip}/{PIR_state}"
    # Make an HTTP request to the server
    response = requests.get(server_url)
    # Print the server response
    print(f"Server Response: {response.text}")


def no_motion_function():  # if stopped detecting motion print
    print("Motion stopped")
    PIR_state = 0
    print(f"{PIR_state}")
    server_url = f"https://boer.butrosgroot.com/api/pir/{local_ip}/{PIR_state}"

    # Make an HTTP request to the server
    response = requests.get(server_url)
    # Print the server response
    print(f"Server Response: {response.text}")

pir.when_motion = motion_function
pir.when_no_motion = no_motion_function

pause()
# End of PIR section