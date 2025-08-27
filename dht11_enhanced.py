#!/usr/bin/env python3
"""
DHT11 Temperature and Humidity Sensor Real-time Monitor
Enhanced version with better error handling and multiple library support
For Raspberry Pi 4B
"""

import time
from datetime import datetime
import sys
import os

def check_and_import_libraries():
    """Try different DHT11 libraries in order of preference"""
    
    # Method 1: Try Adafruit CircuitPython DHT
    try:
        import board
        import adafruit_dht
        print("✅ Using Adafruit CircuitPython DHT library")
        return 'adafruit', board, adafruit_dht
    except ImportError:
        print("⚠️  Adafruit CircuitPython DHT not available")
    
    # Method 2: Try Adafruit_DHT (legacy)
    try:
        import Adafruit_DHT
        print("✅ Using Adafruit_DHT legacy library")
        return 'legacy', None, Adafruit_DHT
    except ImportError:
        print("⚠️  Adafruit_DHT legacy library not available")
    
    # Method 3: Try DHT library
    try:
        import dht
        print("✅ Using dht library")
        return 'dht', None, dht
    except ImportError:
        print("⚠️  dht library not available")
    
    print("❌ No DHT11 libraries found!")
    print("Please install one of the following:")
    print("1. pip3 install adafruit-circuitpython-dht")
    print("2. pip3 install Adafruit_DHT")
    print("3. sudo apt-get install python3-dht")
    return None, None, None

def initialize_sensor(method, board_lib, dht_lib, pin=4):
    """Initialize DHT11 sensor based on available library"""
    
    if method == 'adafruit':
        try:
            if pin == 4:
                sensor = dht_lib.DHT11(board_lib.D4)
            elif pin == 17:
                sensor = dht_lib.DHT11(board_lib.D17)
            elif pin == 18:
                sensor = dht_lib.DHT11(board_lib.D18)
            else:
                sensor = dht_lib.DHT11(getattr(board_lib, f'D{pin}'))
            return sensor
        except Exception as e:
            print(f"❌ Failed to initialize Adafruit sensor: {e}")
            return None
            
    elif method == 'legacy':
        # Adafruit_DHT doesn't need initialization, just specify sensor type and pin
        return {'type': dht_lib.DHT11, 'pin': pin}
        
    elif method == 'dht':
        try:
            sensor = dht_lib.DHT11(pin)
            return sensor
        except Exception as e:
            print(f"❌ Failed to initialize DHT sensor: {e}")
            return None
    
    return None

def read_sensor_data(method, sensor, dht_lib):
    """Read temperature and humidity based on sensor method"""
    
    if method == 'adafruit':
        try:
            temperature = sensor.temperature
            humidity = sensor.humidity
            return temperature, humidity
        except RuntimeError as e:
            return None, None, str(e)
        except Exception as e:
            return None, None, f"Unexpected error: {str(e)}"
    
    elif method == 'legacy':
        try:
            humidity, temperature = dht_lib.read_retry(sensor['type'], sensor['pin'])
            return temperature, humidity
        except Exception as e:
            return None, None, str(e)
    
    elif method == 'dht':
        try:
            sensor.measure()
            temperature = sensor.temperature()
            humidity = sensor.humidity()
            return temperature, humidity
        except Exception as e:
            return None, None, str(e)
    
    return None, None, "Unknown method"

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def display_header(pin):
    """Display the header information"""
    print("=" * 60)
    print("         DHT11 Temperature & Humidity Monitor")
    print("                  Raspberry Pi 4B")
    print("=" * 60)
    print(f"GPIO Pin: {pin} (Physical Pin {get_physical_pin(pin)})")
    print("Press Ctrl+C to exit")
    print("=" * 60)
    print()

def get_physical_pin(gpio_pin):
    """Convert GPIO pin to physical pin number"""
    gpio_to_physical = {
        4: 7, 17: 11, 18: 12, 22: 15, 23: 16, 24: 18, 25: 22, 27: 13
    }
    return gpio_to_physical.get(gpio_pin, "Unknown")

def format_temperature(temp_c):
    """Format temperature with both Celsius and Fahrenheit"""
    if temp_c is None:
        return "N/A"
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return f"{temp_c:.1f}°C ({temp_f:.1f}°F)"

def format_humidity(humidity):
    """Format humidity percentage"""
    if humidity is None:
        return "N/A"
    return f"{humidity:.1f}%"

def get_comfort_level(temp_c, humidity):
    """Determine comfort level based on temperature and humidity"""
    if temp_c is None or humidity is None:
        return "❓ Unknown"
    
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
    """Main function"""
    pin = 4  # Default GPIO pin
    
    print("DHT11 Sensor Initialization...")
    print("Checking available libraries...")
    
    # Check and import libraries
    method, board_lib, dht_lib = check_and_import_libraries()
    if method is None:
        return
    
    # Initialize sensor
    print(f"Initializing sensor on GPIO{pin}...")
    sensor = initialize_sensor(method, board_lib, dht_lib, pin)
    if sensor is None:
        print("❌ Failed to initialize sensor")
        print("Try running with sudo: sudo python3 dht11_enhanced.py")
        return
    
    print("✅ Sensor initialized successfully!")
    print("Starting real-time monitoring...")
    time.sleep(2)
    
    error_count = 0
    reading_count = 0
    consecutive_errors = 0
    
    try:
        while True:
            clear_screen()
            display_header(pin)
            
            print("🔄 Reading sensor data...")
            
            # Read sensor data
            result = read_sensor_data(method, sensor, dht_lib)
            
            if len(result) == 2:
                temperature, humidity = result
                error_msg = None
            else:
                temperature, humidity, error_msg = result
            
            if temperature is not None and humidity is not None:
                reading_count += 1
                consecutive_errors = 0
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Display current readings
                print(f"✅ Successfully read sensor data!")
                print()
                print(f"📅 Time: {current_time}")
                print(f"🌡️  Temperature: {format_temperature(temperature)}")
                print(f"💧 Humidity: {format_humidity(humidity)}")
                print(f"🏠 Comfort Level: {get_comfort_level(temperature, humidity)}")
                print()
                
                # Display statistics
                print(f"📊 Statistics:")
                print(f"   Total Readings: {reading_count}")
                print(f"   Error Count: {error_count}")
                total_attempts = reading_count + error_count
                if total_attempts > 0:
                    success_rate = (reading_count / total_attempts) * 100
                    print(f"   Success Rate: {success_rate:.1f}%")
                
            else:
                error_count += 1
                consecutive_errors += 1
                print("❌ Failed to read sensor data!")
                if error_msg:
                    print(f"   Error: {error_msg}")
                print(f"   Error count: {error_count}")
                print(f"   Consecutive errors: {consecutive_errors}")
                
                if consecutive_errors > 5:
                    print("\n⚠️  Multiple consecutive errors detected.")
                    print("   Troubleshooting steps:")
                    print("   1. Check sensor wiring:")
                    print("      VCC  → 3.3V (Pin 1)")
                    print("      GND  → Ground (Pin 6)")
                    print(f"      DATA → GPIO{pin} (Pin {get_physical_pin(pin)})")
                    print("   2. Try running with sudo permissions")
                    print("   3. Check if sensor is working (try different GPIO pin)")
                    print("   4. Ensure stable power supply")
            
            print()
            print("Next reading in 3 seconds...")
            print("Press Ctrl+C to exit")
            
            # DHT11 needs at least 2 seconds between readings
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Program stopped by user")
        print("✅ Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        sys.exit(1)

if __name__ == "__main__":
    main()
