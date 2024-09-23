import socket
import struct
import time

# Define the telemetry packet format (timestamp: uint32, value: float, status: uint8)
PACKET_FORMAT = 'IfB'
SERVER_ADDRESS = ('127.0.0.1', 5000)  # Adjust the server address and port as needed

def send_telemetry():
    timestamp = int(time.time())
    value = 123.45  # Example telemetry value
    status = 0      # OK status

    # Pack the data into a binary format matching the C struct
    packet = struct.pack(PACKET_FORMAT, timestamp, value, status)

    # Create a UDP socket and send the packet
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(packet, SERVER_ADDRESS)

if __name__ == "__main__":
    send_telemetry()