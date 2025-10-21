#!/usr/bin/env python3
"""
Live Google Maps Tracker - Computer Side
Monitors phone location and generates live Google Maps links
"""

import requests
import time
import webbrowser
import os
import json
from datetime import datetime
from pathlib import Path

class LiveMapsTracker:
    def __init__(self):
        self.FIREBASE_URL = "https://robottracker-85a47-default-rtdb.asia-southeast1.firebasedatabase.app/robot_location.json"
        self.maps_dir = Path("maps")
        self.current_map_file = self.maps_dir / "current_location.html"
        self.dashboard_file = self.maps_dir / "maps_dashboard.html"
        self.maps_dir.mkdir(exist_ok=True)
        
        self.update_count = 0
        self.start_time = datetime.now()
        self.last_location = None
        
    def clear_console(self):
        """Clear console for clean display"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║               LIVE GOOGLE MAPS TRACKER                      ║
║                🗺️ Real-time Location Maps                  ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_status(self, message, message_type="info"):
        """Print colored status messages"""
        colors = {
            "info": "\033[94m",
            "success": "\033[92m", 
            "warning": "\033[93m",
            "error": "\033[91m",
            "reset": "\033[0m"
        }
        
        icons = {
            "info": "ℹ️",
            "success": "✅", 
            "warning": "⚠️",
            "error": "❌"
        }
        
        print(f"{colors[message_type]}{icons[message_type]} {message}{colors['reset']}")
    
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
    
    def generate_google_maps_links(self, lat, lon):
        """Generate various Google Maps links"""
        return {
            "standard": f"https://www.google.com/maps?q={lat},{lon}&z=17",
            "search": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}",
            "place": f"https://www.google.com/maps/place/{lat},{lon}",
            "embed": f"https://maps.google.com/maps?q={lat},{lon}&z=17&output=embed",
            "streetview": f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"
        }
    
    def create_current_map(self, lat, lon, location_data):
        """Create HTML file with current location map"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        maps_links = self.generate_google_maps_links(lat, lon)
        
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Current Robot Location</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f172a;
            color: white;
        }}
        .header {{
            background: linear-gradient(135deg, #1e40af, #1e3a8a);
            padding: 20px;
            text-align: center;
            border-bottom: 3px solid #22c55e;
        }}
        .control-panel {{
            position: absolute;
            top: 100px;
            left: 20px;
            background: rgba(15, 23, 42, 0.95);
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #334155;
            max-width: 400px;
            z-index: 1000;
        }}
        .map-link {{
            background: #1e293b;
            color: white;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border-left: 4px solid #4285f4;
            word-break: break-all;
        }}
        .coordinates {{
            font-family: 'Courier New', monospace;
            background: #1e293b;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        .live-badge {{
            background: #dc2626;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            animation: blink 2s infinite;
        }}
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🗺️ Current Robot Location</h1>
        <div class="live-badge">🔴 LIVE - Auto-updates every 10s</div>
    </div>
    
    <div class="control-panel">
        <h3>📍 Location Data</h3>
        <div class="coordinates">
            <div>Latitude: {lat:.6f}</div>
            <div>Longitude: {lon:.6f}</div>
            <div>Last Update: {location_data.get('timestamp', 'Unknown')}</div>
            <div>Map Updated: {timestamp}</div>
        </div>
        
        <h3>🗺️ Google Maps Links</h3>
        <div class="map-link">
            <a href="{maps_links['standard']}" target="_blank" style="color: #60a5fa;">📱 Standard Map</a>
        </div>
        <div class="map-link">
            <a href="{maps_links['search']}" target="_blank" style="color: #60a5fa;">🔍 Search Map</a>
        </div>
        <div class="map-link">
            <a href="{maps_links['place']}" target="_blank" style="color: #60a5fa;">📌 Place Map</a>
        </div>
        <div class="map-link">
            <a href="{maps_links['streetview']}" target="_blank" style="color: #60a5fa;">🏙️ Street View</a>
        </div>
        
        <div style="margin-top: 15px; font-size: 12px; color: #94a3b8;">
            <div>🔄 Auto-refreshes every 10 seconds</div>
            <div>📱 Phone tracking: {location_data.get('updateCount', 0)} updates</div>
        </div>
    </div>

    <iframe 
        width="100%" 
        height="100%" 
        style="position: absolute; top: 0; left: 0; height: 100vh;"
        src="{maps_links['embed']}"
        frameborder="0">
    </iframe>
</body>
</html>
'''
        
        with open(self.current_map_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return self.current_map_file.resolve()
    
    def create_maps_dashboard(self, locations_history):
        """Create a dashboard with multiple map views"""
        # Implementation for dashboard with history
        pass
    
    def get_uptime(self):
        """Calculate and format uptime"""
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m {seconds}s"
    
    def wait_for_initial_location(self):
        """Wait for first location from phone"""
        self.print_status("Waiting for phone location data...", "info")
        self.print_status("Phone URL: https://notsharedwuwa.github.io/robot-tracker/phone_maps.html", "info")
        self.print_status("Make sure phone has opened the link and started tracking", "info")
        print()
        
        attempts = 0
        while attempts < 30:
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
        
        self.print_status("Timeout: No location data received", "error")
        return None
    
    def start_live_tracking(self):
        """Main tracking loop"""
        self.clear_console()
        self.print_banner()
        
        # Wait for initial connection
        first_location = self.wait_for_initial_location()
        if not first_location:
            return
        
        # Create first map
        map_path = self.create_current_map(
            first_location['latitude'],
            first_location['longitude'], 
            first_location
        )
        
        # Open map in browser
        self.print_status("Opening live Google Maps tracker in browser...", "success")
        webbrowser.open(f'file://{map_path}')
        
        # Start main tracking loop
        self.print_status("LIVE GOOGLE MAPS TRACKING ACTIVATED!", "success")
        self.print_status("Map will auto-update every 10 seconds with phone location", "success")
        self.print_status("Press Ctrl+C to stop tracking", "info")
        print("\n" + "="*70)
        
        try:
            while True:
                location = self.get_robot_location()
                if location:
                    lat = location['latitude']
                    lon = location['longitude']
                    
                    # Update map
                    self.update_count += 1
                    self.create_current_map(lat, lon, location)
                    
                    # Print status
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    uptime = self.get_uptime()
                    maps_links = self.generate_google_maps_links(lat, lon)
                    
                    print(f"📍 [{timestamp}] Update #{self.update_count} | Uptime: {uptime}")
                    print(f"   Coordinates: {lat:.6f}, {lon:.6f}")
                    print(f"   Phone Update: {location.get('timestamp', 'Unknown')}")
                    print(f"   📱 Google Maps: {maps_links['standard']}")
                    print("-" * 70)
                
                time.sleep(10)  # Update every 10 seconds
                
        except KeyboardInterrupt:
            self.print_status("\nTracking stopped by user", "warning")
            self.print_status(f"Final stats: {self.update_count} updates over {self.get_uptime()}", "info")
            self.print_status(f"Current map: {self.current_map_file}", "info")
        
        except Exception as e:
            self.print_status(f"Unexpected error: {e}", "error")
            time.sleep(5)
            self.start_live_tracking()  # Auto-restart

def main():
    """Main entry point"""
    tracker = LiveMapsTracker()
    tracker.start_live_tracking()

if __name__ == "__main__":
    main()
