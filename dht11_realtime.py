#!/usr/bin/env python3
"""
DHT11 Temperature and Humidity Sensor Real-time Monitor
For Raspberry Pi 4B

Hardware Setup:
- DHT11 VCC -> 3.3V (Pin 1)
- DHT11 GND -> Ground (Pin 6) 
- DHT11 DATA -> GPIO4 (Pin 7)

Requirements:
- Adafruit CircuitPython DHT library
- board library (comes with CircuitPython)

Install dependencies:
pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2
"""

import time
import board
import adafruit_dht
from datetime import datetime
import sys

# Initialize DHT11 sensor on GPIO4 (Pin 7)
dht = adafruit_dht.DHT11(board.D4)

def clear_screen():
    """Clear the terminal screen"""
    print("\033[2J\033[H", end="")

def display_header():
    """Display the header information"""
    print("=" * 60)
    print("         DHT11 Temperature & Humidity Monitor")
    print("                  Raspberry Pi 4B")
    print("=" * 60)
    print("GPIO Pin: 4 (Physical Pin 7)")
    print("Press Ctrl+C to exit")
    print("=" * 60)
    print()

def format_temperature(temp_c):
    """Format temperature with both Celsius and Fahrenheit"""
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return f"{temp_c:.1f}°C ({temp_f:.1f}°F)"

def format_humidity(humidity):
    """Format humidity percentage"""
    return f"{humidity:.1f}%"

def get_comfort_level(temp_c, humidity):
    """Determine comfort level based on temperature and humidity"""
    if 20 <= temp_c <= 26 and 40 <= humidity <= 60:
        return "🟢 Comfortable"
    elif temp_c < 16:
        return "🔵 Too Cold"
    elif temp_c > 30:
        return "🔴 Too Hot"
    elif humidity < 30:
        return "🟡 Too Dry"
    elif humidity > 70:
        return "🟠 Too Humid"
    else:
        return "🟡 Moderate"

def main():
    """Main function to continuously read and display sensor data"""
    print("Initializing DHT11 sensor...")
    time.sleep(2)
    
    error_count = 0
    reading_count = 0
    
    try:
        while True:
            clear_screen()
            display_header()
            
            try:
                # Read temperature and humidity
                temperature = dht.temperature
                humidity = dht.humidity
                
                if temperature is not None and humidity is not None:
                    reading_count += 1
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Display current readings
                    print(f"📅 Time: {current_time}")
                    print(f"🌡️  Temperature: {format_temperature(temperature)}")
                    print(f"💧 Humidity: {format_humidity(humidity)}")
                    print(f"🏠 Comfort Level: {get_comfort_level(temperature, humidity)}")
                    print()
                    
                    # Display statistics
                    print(f"📊 Statistics:")
                    print(f"   Total Readings: {reading_count}")
                    print(f"   Error Count: {error_count}")
                    if reading_count > 0:
                        success_rate = ((reading_count - error_count) / reading_count) * 100
                        print(f"   Success Rate: {success_rate:.1f}%")
                    
                    # Reset error count on successful reading
                    if error_count > 0:
                        error_count = 0
                        
                else:
                    error_count += 1
                    print("❌ Failed to read sensor data!")
                    print(f"   Error count: {error_count}")
                    if error_count > 5:
                        print("⚠️  Multiple consecutive errors detected.")
                        print("   Check sensor connections and wiring.")
                    
            except RuntimeError as e:
                error_count += 1
                error_msg = str(e)
                print(f"❌ Sensor Error: {error_msg}")
                print(f"   Error count: {error_count}")
                
                # Provide helpful error messages
                if "timeout" in error_msg.lower():
                    print("💡 Tip: Check if the sensor is properly connected to GPIO4")
                elif "checksum" in error_msg.lower():
                    print("💡 Tip: This is normal occasionally, sensor will retry")
                    
            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")
                error_count += 1
            
            print()
            print("Next reading in 2 seconds...")
            print("Press Ctrl+C to exit")
            
            # Wait 2 seconds before next reading
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Program stopped by user")
        print("Cleaning up...")
        dht.exit()
        print("✅ Cleanup complete. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        dht.exit()
        sys.exit(1)

if __name__ == "__main__":
    main()
