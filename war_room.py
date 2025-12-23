import folium
import sqlite3

DB_NAME = "surveillance_log.db"

def generate_map():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get the latest position for every aircraft
    # We use a subquery to ensure we get the absolute latest timestamp for each plane
    cursor.execute('''
        SELECT t1.icao24, t1.lat, t1.lon, t1.velocity, t1.is_anomaly, t1.anomaly_reason
        FROM flight_data t1
        JOIN (
            SELECT icao24, MAX(timestamp) as max_time
            FROM flight_data
            GROUP BY icao24
        ) t2 ON t1.icao24 = t2.icao24 AND t1.timestamp = t2.max_time
    ''')
    
    targets = cursor.fetchall()
    conn.close()

    if not targets:
        print("No data found. Run interceptor.py first!")
        return

    # Calculate average center so map starts in the right place
    avg_lat = sum([t[1] for t in targets]) / len(targets)
    avg_lon = sum([t[2] for t in targets]) / len(targets)
    
    # Create Map
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=4, tiles="CartoDB dark_matter")
    
    # List to store coordinates for auto-zooming
    all_coords = []

    threat_count = 0

    for target in targets:
        icao24, lat, lon, velocity, is_anomaly, reason = target
        
        if lat and lon:
            all_coords.append([lat, lon])
            
            # Color logic
            if is_anomaly:
                color = "red"
                radius = 8  # Make threats bigger
                status = "THREAT DETECTED"
                threat_count += 1
            else:
                color = "green"
                radius = 4
                status = "Normal"
            
            # Popup content
            popup_text = f"""
            <b>ID:</b> {icao24}<br>
            <b>Status:</b> {status}<br>
            <b>Speed:</b> {velocity} m/s<br>
            <b>Info:</b> {reason if reason else "No anomalies"}
            """
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(m)
    
    # Auto-fit map to show all points (London AND New York)
    if all_coords:
        m.fit_bounds(all_coords)

    m.save("war_room_dashboard.html")
    print(f"Dashboard updated. Found {threat_count} active threats.")
    print("Refresh 'war_room_dashboard.html' in your browser.")

if __name__ == "__main__":
    generate_map()