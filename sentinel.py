import time
from datetime import datetime
import interceptor
import detective
import war_room
import database 

def main():
    print("Initializing SENTINEL System...")
    
    # 1. SETUP: Create the table if it doesn't exist
    print("--- Checking Database Structure ---")
    database.init_db()  # <--- This creates the table
    
    print("Press Ctrl+C to stop surveillance.")

    while True:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{timestamp}] BEGINNING SCAN CYCLE")
        
        # 2. INTERCEPT
        try:
            # Note: You might want to remove the "Press Ctrl+C" print inside interceptor.py 
            # later to keep these logs cleaner, but it works fine as is.
            interceptor.run_interceptor()
        except Exception as e:
            print(f"Interceptor Error: {e}")
        
        # 3. DETECT
        try:
            detective.detect_anomalies()
        except Exception as e:
            print(f"Detective Error: {e}")
        
        # 4. VISUALIZE
        try:
            war_room.generate_map()
        except Exception as e:
            print(f"Visualization Error: {e}")
        
        print(f"[{timestamp}] CYCLE COMPLETE.")
        
        # Wait 30 seconds
        time.sleep(30)

if __name__ == "__main__":
    main()