import requests
import time
import webbrowser
import os
import sys
from datetime import datetime
from pathlib import Path

class PermanentRobotTracker:
    def __init__(self):
        self.FIREBASE_URL = "https://robottracker-85a47-default-rtdb.asia-southeast1.firebasedatabase.app/robot_location.json"
        self.map_file = "permanent_robot_tracker.html"
        self.start_time = datetime.now()
        self.update_count = 0
        self.last_location = None
        
    def clear_console(self):
        """Clear console for clean display"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                   PERMANENT ROBOT TRACKER                   ║
║                  🤖 24/7 Location Tracking                  ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def print_status(self, message, message_type="info"):
        """Print status message with colors"""
        colors = {
            "info": "\033[94m",      # Blue
            "success": "\033[92m",   # Green
            "warning": "\033[93m",   # Yellow
            "error": "\033[91m",     # Red
            "reset": "\033[0m"       # Reset
        }
        
        icon = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        print(f"{colors[message_type]}{icon[message_type]} {message}{colors['reset']}")
        
    def get_robot_location(self):
        """Get latest location from Firebase"""
        try:
            response = requests.get(self.FIREBASE_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'latitude' in data and data['latitude'] != 0:
                    return data
            return None
        except Exception as e:
            self.print_status(f"Connection error: {e}", "error")
            return None
    
    def create_permanent_map(self, lat, lon, location_data):
        """Create auto-updating permanent map"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uptime = self.get_uptime()
        
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Permanent Robot Tracker</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f172a;
            color: white;
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e40af, #1e3a8a);
            padding: 20px;
            text-align: center;
            border-bottom: 3px solid #22c55e;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            margin: 5px 0 0 0;
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .control-panel {{
            position: absolute;
            top: 120px;
            left: 20px;
            background: rgba(15, 23, 42, 0.95);
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #334155;
            backdrop-filter: blur(10px);
            max-width: 350px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            z-index: 1000;
        }}
        
        .live-badge {{
            background: #dc2626;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 15px;
            animation: blink 2s infinite;
        }}
        
        .data-section {{
            margin-bottom: 15px;
        }}
        
        .data-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding-bottom: 8px;
            border-bottom: 1px solid #334155;
        }}
        
        .data-row:last-child {{
            border-bottom: none;
            margin-bottom: 0;
        }}
        
        .data-label {{
            font-weight: 600;
            color: #94a3b8;
        }}
        
        .data-value {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }}
        
        .stat-box {{
            background: #1e293b;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #334155;
        }}
        
        .stat-number {{
            font-size: 18px;
            font-weight: bold;
            color: #22c55e;
            display: block;
        }}
        
        .stat-label {{
            font-size: 12px;
            color: #94a3b8;
        }}
        
        @keyframes blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
            100% {{ opacity: 1; }}
        }}
        
        #map-frame {{
            width: 100vw;
            height: 100vh;
            border: none;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 PERMANENT ROBOT TRACKER</h1>
        <div class="subtitle">24/7 Real-time Location Monitoring</div>
    </div>
    
    <div class="control-panel">
        <div class="live-badge">🔴 LIVE TRACKING ACTIVE</div>
        
        <div class="data-section">
            <div class="data-row">
                <span class="data-label">📍 Latitude:</span>
                <span class="data-value">{lat:.6f}</span>
            </div>
            <div class="data-row">
                <span class="data-label">📍 Longitude:</span>
                <span class="data-value">{lon:.6f}</span>
            </div>
            <div class="data-row">
                <span class="data-label">🎯 Accuracy:</span>
                <span class="data-value">{location_data.get('accuracy', 'Unknown')}m</span>
            </div>
            <div class="data-row">
                <span class="data-label">🕒 Last Update:</span>
                <span class="data-value">{location_data.get('timestamp', 'Unknown')}</span>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-box">
                <span class="stat-number">{self.update_count}</span>
                <span class="stat-label">Updates</span>
            </div>
            <div class="stat-box">
                <span class="stat-number">{uptime}</span>
                <span class="stat-label">Uptime</span>
            </div>
        </div>
        
        <div style="margin-top: 15px; font-size: 12px; color: #64748b;">
            <div>🔄 Auto-refreshes every 5 seconds</div>
            <div>📱 Phone: Permanent tracking active</div>
            <div>💾 Last map update: {timestamp}</div>
        </div>
    </div>
    
    <iframe 
        id="map-frame"
        src="https://maps.google.com/maps?q={lat},{lon}&z=17&output=embed">
    </iframe>
</body>
</html>
'''
        
        with open(self.map_file, "w", encoding='utf-8') as f:
            f.write(html_content)
        
        return os.path.abspath(self.map_file)
    
    def get_uptime(self):
        """Calculate and format uptime"""
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m {seconds}s"
    
    def wait_for_initial_connection(self):
        """Wait for the first location data from phone"""
        self.print_status("Waiting for robot phone to connect...", "info")
        self.print_status("Phone URL: https://notsharedwuwa.github.io/robot-tracker/tracker.html", "info")
        self.print_status("Make sure the phone has opened the link and tracking is active", "info")
        print()
        
        attempts = 0
        while attempts < 50:  # Wait up to 100 seconds
            location = self.get_robot_location()
            if location:
                lat = location['latitude']
                lon = location['longitude']
                self.print_status(f"First location received: {lat:.6f}, {lon:.6f}", "success")
                return location
            
            attempts += 1
            if attempts % 5 == 0:
                self.print_status(f"Still waiting... ({attempts * 2}s elapsed)", "warning")
            time.sleep(2)
        
        self.print_status("Timeout: No location data received from phone", "error")
        self.print_status("Please check:", "error")
        self.print_status("1. Phone has opened the tracking link", "error")
        self.print_status("2. Location permissions are allowed", "error")
        self.print_status("3. Phone has internet connection", "error")
        return None
    
    def start_permanent_tracking(self):
        """Main permanent tracking loop"""
        self.clear_console()
        self.print_banner()
        
        # Wait for initial connection
        first_location = self.wait_for_initial_connection()
        if not first_location:
            return
        
        # Create first map
        map_path = self.create_permanent_map(
            first_location['latitude'], 
            first_location['longitude'],
            first_location
        )
        
        # Open map in browser
        self.print_status("Opening permanent tracking map in browser...", "success")
        webbrowser.open(f'file://{map_path}')
        
        # Start main tracking loop
        self.print_status("PERMANENT TRACKING ACTIVATED!", "success")
        self.print_status("The robot will be tracked 24/7 until phone battery dies", "success")
        self.print_status("Press Ctrl+C to stop the tracker", "info")
        print("\n" + "="*60)
        
        map_opened = True
        
        try:
            while True:
                location = self.get_robot_location()
                if location:
                    lat = location['latitude']
                    lon = location['longitude']
                    
                    # Update map
                    self.update_count += 1
                    self.create_permanent_map(lat, lon, location)
                    
                    # Print status
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    uptime = self.get_uptime()
                    
                    print(f"📍 [{timestamp}] Update #{self.update_count} | Uptime: {uptime}")
                    print(f"   Coordinates: {lat:.6f}, {lon:.6f}")
                    print(f"   Phone Update: {location.get('timestamp', 'Unknown')}")
                    print(f"   Accuracy: {location.get('accuracy', 'Unknown')}m")
                    print("-" * 60)
                
                time.sleep(5)  # Update every 5 seconds
                
        except KeyboardInterrupt:
            self.print_status("\nPermanent tracking stopped by user", "warning")
            self.print_status(f"Final stats: {self.update_count} updates over {self.get_uptime()}", "info")
            self.print_status("Map file: " + os.path.abspath(self.map_file), "info")
        
        except Exception as e:
            self.print_status(f"Unexpected error: {e}", "error")
            self.print_status("Tracker will attempt to restart in 10 seconds...", "info")
            time.sleep(10)
            self.start_permanent_tracking()  # Auto-restart

def main():
    """Main entry point"""
    tracker = PermanentRobotTracker()
    tracker.start_permanent_tracking()

if __name__ == "__main__":
    main()
