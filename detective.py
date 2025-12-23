import sqlite3
import math

DB_NAME = "surveillance_log.db"
MAX_SPEED_KNOTS = 600  # Threshold for commercial jets (approx)
# Note: 1 m/s approx 1.94 knots. OpenSky gives velocity in m/s. 
# We will convert for the check.

def haversine(lat1, lon1, lat2, lon2):
    """Calculates distance in km between two lat/lon points."""
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def detect_anomalies():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get unique aircraft IDs present in the DB
    cursor.execute("SELECT DISTINCT icao24 FROM flight_data")
    aircraft_ids = [row[0] for row in cursor.fetchall()]
    
    print(f"Scanning {len(aircraft_ids)} targets for anomalies...")

    for aircraft in aircraft_ids:
        # Get last 2 entries for this aircraft, ordered by time
        cursor.execute('''
            SELECT id, timestamp, lat, lon, velocity 
            FROM flight_data WHERE icao24 = ? 
            ORDER BY timestamp DESC LIMIT 2
        ''', (aircraft,))
        
        rows = cursor.fetchall()
        
        if len(rows) == 2:
            latest, previous = rows[0], rows[1]
            
            id_new, time_new, lat_new, lon_new, vel_new = latest
            id_old, time_old, lat_old, lon_old, vel_old = previous
            
            time_diff = time_new - time_old
            
            # Skip if time diff is 0 (duplicate data)
            if time_diff == 0:
                continue

            # 1. THE TELEPORTATION CHECK
            distance_km = haversine(lat_old, lon_old, lat_new, lon_new)
            
            # Calculate implied speed (km/s -> km/h)
            implied_speed_kmh = (distance_km / time_diff) * 3600
            
            # Convert m/s to km/h for the reported velocity
            reported_speed_kmh = (vel_new if vel_new else 0) * 3.6
            
            # Threshold: If implied speed is > 2000 km/h (supersonic/impossible for commercial)
            # OR if implied speed is significantly higher than reported speed
            if implied_speed_kmh > 2000:
                reason = f"TELEPORTATION: Moved {distance_km:.2f}km in {time_diff}s. Implied Speed: {implied_speed_kmh:.0f} km/h"
                print(f"ALERT [{aircraft}]: {reason}")
                cursor.execute("UPDATE flight_data SET is_anomaly=1, anomaly_reason=? WHERE id=?", (reason, id_new))

    conn.commit()
    conn.close()
    print("Scan complete.")

if __name__ == "__main__":
    detect_anomalies()