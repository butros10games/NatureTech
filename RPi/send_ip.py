import socket
import sys  # Import sys module for exit()

import requests


# Function to check internet connectivity
def check_internet_connection():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return True
    except requests.RequestException:
        return False


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


# Check internet connectivity
if not check_internet_connection():
    print("Unable to connect to the internet. Exiting.")
    sys.exit()

# Get the local WLAN IP address
local_ip = get_local_ip()
pi_name = socket.gethostname()

# Check if local_ip is obtained successfully
if local_ip:
    # Define the server URL where you want to send the IP
    server_url = f"https://boer.butrosgroot.com/api/bt/{local_ip}"

    try:
        # Send the HTTP GET request to the server
        response = requests.get(server_url)

        # Print the server's response
        print("Name:", pi_name)
        print("IP sent:", local_ip)
        print("Server response:", response.text)

    except requests.RequestException as e:
        print("Error sending request:", e)
        sys.exit("Exiting due to an error.")
else:
    print("Unable to retrieve local IP address.")
