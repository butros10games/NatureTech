#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from datetime import datetime

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the button
button_pin = 4

# Setup the button pin as an input with a pull-up resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize the variable to store the previous state of the button
prev_button_state = GPIO.input(button_pin)

try:
    while True:
        # Read the current state of the button
        button_state = GPIO.input(button_pin)

        # Check if the button state has changed
        if button_state != prev_button_state:
            if button_state == GPIO.LOW:
                print("Button is pressed (closed)")
                print(f"{button_state}")
                server_url = f"https://boer.butrosgroot.com/api/btn/{button_state}"
                # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Can be removed later because backend will do time
                # print(f"Button is pressed (closed) at {current_time}")
                
            else:
                print("Button is released (open)")
                print(f"{button_state}")
                server_url = f"https://boer.butrosgroot.com/api/btn/{button_state}"
                # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Can be removed later because backend will do time
                # print(f"Button is released (open) at {current_time}")

            # Update the previous button state
            prev_button_state = button_state

        # Add a small delay to debounce the button
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    # Cleanup GPIO settings
    GPIO.cleanup()
