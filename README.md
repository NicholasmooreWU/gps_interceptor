# GPS Interceptor - Aircraft Surveillance System

A real-time aircraft tracking and anomaly detection system that monitors flight data from the OpenSky Network API, detects suspicious behavior, and visualizes threats on an interactive dashboard.

## 🎯 Features

- **Real-time Flight Tracking**: Intercepts live aircraft data from OpenSky Network API
- **Anomaly Detection**: Identifies impossible flight patterns (teleportation, supersonic speeds)
- **Interactive Dashboard**: Visual threat map using Folium with automatic zoom and color-coded markers
- **SQLite Database**: Persistent storage of flight data and anomaly records
- **Red Team Testing**: Built-in threat injection for testing detection capabilities
- **Standalone Executable**: Compiled with PyInstaller for easy deployment

## 📁 Project Structure

```
gps_interceptor/
│
├── sentinel.py              # Main orchestration system (runs continuous surveillance cycles)
├── database.py              # Database initialization and schema management
├── interceptor.py           # Flight data collection from OpenSky Network API
├── detective.py             # Anomaly detection engine (teleportation analysis)
├── war_room.py              # Dashboard generation (Folium map visualization)
├── red_team.py              # Threat injection tool for testing
├── war_room_dashboard.html  # Generated interactive map (refreshed automatically)
├── surveillance_log.db      # SQLite database (auto-created)
│
└── build/sentinel/          # PyInstaller build artifacts
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Internet connection (for OpenSky Network API)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```powershell
   pip install requests folium
   ```

3. **Initialize the database**:
   ```powershell
   python database.py
   ```

### Running the System

#### Option 1: Python Script (Recommended for Development)

```powershell
python sentinel.py
```

This starts continuous surveillance with 30-second scan cycles.

#### Option 2: Standalone Executable

```powershell
.\dist\sentinel.exe
```

### Testing Anomaly Detection

To inject a test threat (aircraft that "teleports" from London to New York):

```powershell
python red_team.py
python detective.py
python war_room.py
```

Then open `war_room_dashboard.html` in your browser to see the red threat markers.

## 🔍 How It Works

### 1. **Interceptor** ([interceptor.py](interceptor.py))
- Queries the OpenSky Network API for aircraft within defined geographic bounds
- Default bounds: London area (configurable via `BOUNDS` variable)
- Saves aircraft position, velocity, heading, and ICAO24 identifier to database

### 2. **Detective** ([detective.py](detective.py))
- Analyzes consecutive position reports for each aircraft
- Detects "teleportation" by calculating:
  - Distance between consecutive positions (Haversine formula)
  - Implied speed based on time difference
  - Flags aircraft moving faster than 2000 km/h as anomalies
- Updates database with anomaly flags and reasons

### 3. **War Room** ([war_room.py](war_room.py))
- Generates interactive Folium map with latest aircraft positions
- **Green markers**: Normal aircraft
- **Red markers**: Detected threats (larger radius)
- Auto-fits bounds to show all tracked aircraft
- Popups display: ICAO24 ID, speed, status, and anomaly details

### 4. **Sentinel** ([sentinel.py](sentinel.py))
- Main orchestration loop that runs every 30 seconds:
  1. Initialize database (if needed)
  2. Intercept flight data
  3. Detect anomalies
  4. Generate updated dashboard
- Press `Ctrl+C` to stop

## ⚙️ Configuration

### Changing the Surveillance Area

Edit [interceptor.py](interceptor.py) line 14:

```python
BOUNDS = {'lamin': 51.0, 'lomin': -1.0, 'lamax': 52.0, 'lomax': 1.0}
```

Examples:
- **Black Sea**: `{'lamin': 40.0, 'lomin': 27.0, 'lamax': 47.0, 'lomax': 42.0}`
- **New York**: `{'lamin': 40.0, 'lomin': -75.0, 'lamax': 41.5, 'lomax': -73.0}`

### Adjusting Detection Sensitivity

Edit [detective.py](detective.py) line 62:

```python
if implied_speed_kmh > 2000:  # Change threshold here
```

### Scan Interval

Edit [sentinel.py](sentinel.py) line 41:

```python
time.sleep(30)  # Change from 30 seconds to desired interval
```

## 📊 Database Schema

Table: `flight_data`

| Column          | Type    | Description                                    |
|-----------------|---------|------------------------------------------------|
| id              | INTEGER | Primary key (auto-increment)                   |
| timestamp       | INTEGER | Unix timestamp                                 |
| icao24          | TEXT    | Aircraft identifier                            |
| lat             | REAL    | Latitude                                       |
| lon             | REAL    | Longitude                                      |
| velocity        | REAL    | Speed in m/s                                   |
| heading         | REAL    | Direction in degrees                           |
| is_anomaly      | BOOLEAN | 0 = normal, 1 = threat detected                |
| anomaly_reason  | TEXT    | Description of detected anomaly                |

## 🛠️ Building the Executable

The project includes a `sentinel.spec` file for PyInstaller. To rebuild:

```powershell
pyinstaller sentinel.spec
```

The executable will be created in `dist/sentinel.exe`.

## 🔐 Security Considerations

- **API Rate Limits**: OpenSky Network has rate limits for anonymous users. Consider registering for higher limits.
- **Data Privacy**: This tool tracks publicly available ADS-B data only.
- **Educational Purpose**: This project is for educational and research purposes.

## 🐛 Troubleshooting

### Import Errors
If you see "Import 'folium' could not be resolved":
1. Ensure folium is installed: `pip install folium`
2. Select correct Python interpreter in VS Code (`Ctrl+Shift+P` → "Python: Select Interpreter")
3. Restart VS Code

### No Data Found
- Check internet connection
- Verify that aircraft are present in your configured `BOUNDS`
- Try expanding the geographic area
- Check OpenSky Network API status

### Database Locked
- Close any other programs accessing `surveillance_log.db`
- Stop any running sentinel.py instances

## 📝 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Feel free to fork and improve! Key areas for enhancement:
- Add more anomaly detection algorithms
- Implement historical playback
- Add email/SMS alerts for threats
- Support multiple map tile providers
- Add aircraft metadata lookup

## 📞 Support

For issues or questions, create an issue in the repository.

---

**⚠️ Disclaimer**: This tool is for educational and research purposes only. Always respect aviation regulations and data privacy laws.
