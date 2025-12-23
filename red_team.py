import sqlite3
import time

DB_NAME = "surveillance_log.db"

def inject_threat():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    current_time = int(time.time())
    
    print("Injecting GHOST signal...")
    
    # 1. Insert "Ghost" plane at London (Time 0)
    cursor.execute('''
        INSERT INTO flight_data (timestamp, icao24, lat, lon, velocity, heading)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (current_time - 10, "BADACTOR1", 51.5, -0.12, 250, 90))
    
    # 2. Insert same "Ghost" plane at New York (Time +1s) -> TELEPORTATION!
    cursor.execute('''
        INSERT INTO flight_data (timestamp, icao24, lat, lon, velocity, heading)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (current_time, "BADACTOR1", 40.7, -74.0, 250, 90))
    
    conn.commit()
    conn.close()
    print("Injection complete. Run 'detective.py' to catch the anomaly.")

if __name__ == "__main__":
    inject_threat()