import requests
import time
import webbrowser
import os
from datetime import datetime

FIREBASE_URL = "https://robottracker-85a47-default-rtdb.asia-southeast1.firebasedatabase.app/robot_location.json"

def get_robot_location():
    try:
        response = requests.get(FIREBASE_URL)
        if response.status_code == 200:
            data = response.json()
            if data and 'latitude' in data:
                return data
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_map(lat, lon):
    timestamp = datetime.now().strftime("%H:%M:%S")
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Robot Live Tracker</title>
        <meta http-equiv="refresh" content="3">
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
            }}
            #info {{
                position: absolute;
                top: 10px;
                left: 10px;
                background: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                z-index: 1000;
            }}
        </style>
    </head>
    <body>
        <div id="info">
            <h3>🤖 Robot Live Tracker</h3>
            <p>📍 {lat:.6f}, {lon:.6f}</p>
            <p>🕒 {timestamp}</p>
            <p style="color: green;">✅ LIVE - Updating every 3s</p>
        </div>
        <iframe 
            width="100%" 
            height="100%" 
            frameborder="0"
            src="https://maps.google.com/maps?q={lat},{lon}&z=18&output=embed">
        </iframe>
    </body>
    </html>
    '''
    with open("map.html", "w") as f:
        f.write(html)
    return os.path.abspath("map.html")

def main():
    print("🤖 Starting Robot Tracker...")
    print("📍 Waiting for robot phone to connect...")
    print("   Send this link to your phone:")
    print("   [Your GitHub Pages URL will go here]")
    print("──────────────────────────────────────────")
    
    map_opened = False
    
    while True:
        try:
            location = get_robot_location()
            if location and location.get('latitude'):
                lat = location['latitude']
                lon = location['longitude']
                
                map_path = create_map(lat, lon)
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                if not map_opened:
                    print("✅ Robot connected! Opening live map...")
                    webbrowser.open(f'file://{map_path}')
                    map_opened = True
                    print("🎯 Live tracking started! Press Ctrl+C to stop")
                    print("──────────────────────────────────────────")
                
                print(f"📍 {timestamp}: {lat:.6f}, {lon:.6f}")
            else:
                if not map_opened:
                    print("⏳ Waiting for location data...", end='\r')
                time.sleep(2)
                continue
                
            time.sleep(3)
            
        except KeyboardInterrupt:
            print("\n🛑 Tracking stopped.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
