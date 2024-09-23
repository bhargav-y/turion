import struct 
import socket
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

PACKET_FORMAT = 'IfB'
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

UDP_IP = '0.0.0.0'
UDP_PORT = 5000

DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_NAME = os.getenv('POSTGRES_DB', 'telemetry')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

if not all([DB_USER, DB_PASSWORD]):
    raise ValueError('Database credentials are not set')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)

cursor = conn.cursor()
# Create telemetry table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS telemetry (
    id SERIAL PRIMARY KEY,
    timestamp INTEGER,
    value REAL,
    status SMALLINT
);
'''
cursor.execute(create_table_query)
conn.commit()

print("UDP server is up and listening for telemetry packets...")

try:
    while True:
        data, addr = sock.recvfrom(PACKET_SIZE)
        if len(data) != PACKET_SIZE:
            print(f"Received packet of incorrect size from {addr}")
            continue

        # Unpack the data
        timestamp, value, status = struct.unpack(PACKET_FORMAT, data)

        # Insert the data into the database
        insert_query = '''
        INSERT INTO telemetry (timestamp, value, status)
        VALUES (%s, %s, %s);
        '''
        cursor.execute(insert_query, (timestamp, value, status))
        conn.commit()

        print(f"Inserted data from {addr}: timestamp={timestamp}, value={value}, status={status}")

except KeyboardInterrupt:
    print("Shutting down the server...")

finally:
    cursor.close()
    conn.close()
    sock.close()