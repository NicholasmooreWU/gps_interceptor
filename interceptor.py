import time
import requests
import sqlite3
from datetime import datetime

# Configuration
DB_NAME = "surveillance_log.db"
OPENSKY_URL = "https://opensky-network.org/api/states/all"

# Bounding Box for Black Sea (approximate)
# Format: [min_lat, min_lon, max_lat, max_lon]
# Example: Lat 40-47, Lon 27-42 covers much of the Black Sea

# Example bounding box for London area, can be changed as needed
BOUNDS = {'lamin': 51.0, 'lomin': -1.0, 'lamax': 52.0, 'lomax': 1.0}


def save_to_db(states):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = int(time.time())
    
    count = 0
    for state in states:
        # OpenSky State Vector: index 0=icao24, 5=lon, 6=lat, 9=velocity, 10=heading
        icao24 = state[0]
        lon = state[5]
        lat = state[6]
        velocity = state[9]
        heading = state[10]

        # Only save if we have valid coordinates
        if lat and lon:
            cursor.execute('''
                INSERT INTO flight_data (timestamp, icao24, lat, lon, velocity, heading)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (current_time, icao24, lat, lon, velocity, heading))
            count += 1
            
    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] Intercepted {count} targets.")

def run_interceptor():
    print("Starting Interceptor... Press Ctrl+C to stop.")
    try:
        response = requests.get(OPENSKY_URL, params=BOUNDS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['states']:
                save_to_db(data['states'])
            else:
                print("No targets in zone.")
        else:
            print(f"API Error: {response.status_code}")
                
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    run_interceptor()