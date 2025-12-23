import sqlite3

DB_NAME = "surveillance_log.db"

def init_db():
    """Initializes the SQLite database with the necessary table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flight_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            icao24 TEXT,
            lat REAL,
            lon REAL,
            velocity REAL,
            heading REAL,
            is_anomaly BOOLEAN DEFAULT 0,
            anomaly_reason TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized successfully.")

if __name__ == "__main__":
    init_db()