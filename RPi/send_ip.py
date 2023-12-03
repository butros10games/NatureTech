import requests
import socket

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

# Check if local_ip is obtained successfully
if local_ip:
    # Define the server URL where you want to send the IP
    server_url = f"https://boer.butrosgroot.com/api/bt/{local_ip}"

    try:
        # Send the HTTP GET request to the server
        response = requests.get(server_url)

        # Print the server's response
        print("IP send:", local_ip)
        print("Server response:", response.text)

    except requests.RequestException as e:
        print("Error sending request:", e)
else:
    print("Unable to retrieve local IP address.")
