import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the button
button_pin = 17  # Change this to the GPIO pin you have connected the button to

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
            else:
                print("Button is released (open)")

            # Update the previous button state
            prev_button_state = button_state

        # Add a small delay to debounce the button
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    # Cleanup GPIO settings
    GPIO.cleanup()
