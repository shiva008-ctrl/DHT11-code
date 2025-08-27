#!/usr/bin/env python3
"""
DHT11 Quick Fix Script
This script tries different methods to read DHT11 sensor
Use this if the main script shows header but no data
"""

import time
import sys
from datetime import datetime

def method1_circuitpython():
    """Try Adafruit CircuitPython method"""
    print("🔄 Trying Method 1: Adafruit CircuitPython...")
    try:
        import board
        import adafruit_dht
        
        dht = adafruit_dht.DHT11(board.D4)
        print("✅ Sensor initialized with CircuitPython")
        
        for i in range(3):
            try:
                temperature = dht.temperature
                humidity = dht.humidity
                
                if temperature is not None and humidity is not None:
                    print(f"✅ Reading {i+1}: {temperature:.1f}°C, {humidity:.1f}%")
                    return True
                else:
                    print(f"❌ Reading {i+1}: Failed (None values)")
            except RuntimeError as e:
                print(f"❌ Reading {i+1}: {str(e)}")
            
            time.sleep(2)
        
        dht.exit()
        return False
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def method2_legacy():
    """Try Adafruit legacy DHT method"""
    print("\n🔄 Trying Method 2: Adafruit Legacy...")
    try:
        import Adafruit_DHT
        
        sensor = Adafruit_DHT.DHT11
        pin = 4
        
        print("✅ Sensor initialized with Legacy library")
        
        for i in range(3):
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            
            if temperature is not None and humidity is not None:
                print(f"✅ Reading {i+1}: {temperature:.1f}°C, {humidity:.1f}%")
                return True
            else:
                print(f"❌ Reading {i+1}: Failed (None values)")
            
            time.sleep(2)
        
        return False
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def method3_rpi_gpio():
    """Try basic RPi.GPIO method"""
    print("\n🔄 Trying Method 3: RPi.GPIO (basic)...")
    try:
        import RPi.GPIO as GPIO
        
        GPIO.setmode(GPIO.BCM)
        pin = 4
        
        print("✅ GPIO initialized")
        
        # Simple test - just check if GPIO is accessible
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()
        
        print("✅ Basic GPIO operations successful")
        print("💡 DHT11 data reading requires specialized timing")
        print("💡 Use Adafruit libraries for actual sensor reading")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ GPIO error: {e}")
        print("💡 Try running with sudo: sudo python3 dht11_quickfix.py")
        return False

def test_different_pins():
    """Test sensor on different GPIO pins"""
    print("\n🔄 Testing different GPIO pins...")
    
    pins_to_test = [4, 17, 18, 22, 27]
    
    try:
        import board
        import adafruit_dht
        
        for pin in pins_to_test:
            print(f"\n📍 Testing GPIO{pin}...")
            try:
                if pin == 4:
                    dht = adafruit_dht.DHT11(board.D4)
                elif pin == 17:
                    dht = adafruit_dht.DHT11(board.D17)
                elif pin == 18:
                    dht = adafruit_dht.DHT11(board.D18)
                elif pin == 22:
                    dht = adafruit_dht.DHT11(board.D22)
                elif pin == 27:
                    dht = adafruit_dht.DHT11(board.D27)
                
                time.sleep(1)
                temperature = dht.temperature
                humidity = dht.humidity
                
                if temperature is not None and humidity is not None:
                    print(f"✅ GPIO{pin} works: {temperature:.1f}°C, {humidity:.1f}%")
                    dht.exit()
                    return pin
                else:
                    print(f"❌ GPIO{pin}: No data")
                
                dht.exit()
                
            except Exception as e:
                print(f"❌ GPIO{pin}: {str(e)}")
        
        return None
        
    except ImportError:
        print("❌ CircuitPython libraries not available")
        return None

def main():
    """Main function to test different methods"""
    print("=" * 50)
    print("      DHT11 Quick Fix & Test Script")
    print("=" * 50)
    print()
    
    success = False
    
    # Test Method 1: CircuitPython
    if method1_circuitpython():
        success = True
        print("\n🎉 Success! Use: python3 dht11_realtime.py")
    
    # Test Method 2: Legacy Adafruit
    if not success and method2_legacy():
        success = True
        print("\n🎉 Success! Use: python3 dht11_alternative.py")
    
    # Test Method 3: Basic GPIO
    if not success:
        method3_rpi_gpio()
    
    # Test different pins if main pin doesn't work
    if not success:
        working_pin = test_different_pins()
        if working_pin:
            print(f"\n🎉 Sensor works on GPIO{working_pin}!")
            print(f"💡 Modify your scripts to use GPIO{working_pin} instead of GPIO4")
    
    if not success:
        print("\n" + "=" * 50)
        print("🔧 TROUBLESHOOTING STEPS:")
        print("=" * 50)
        print("1. Check wiring:")
        print("   DHT11 VCC  → Pi Pin 1 (3.3V)")
        print("   DHT11 GND  → Pi Pin 6 (Ground)")
        print("   DHT11 DATA → Pi Pin 7 (GPIO4)")
        print()
        print("2. Install libraries:")
        print("   pip3 install adafruit-circuitpython-dht")
        print("   sudo apt-get install libgpiod2")
        print()
        print("3. Try with sudo:")
        print("   sudo python3 dht11_quickfix.py")
        print()
        print("4. Run diagnostic:")
        print("   python3 dht11_diagnostic.py")
        print()
        print("5. Check sensor:")
        print("   - Ensure it's a genuine DHT11 (not DHT22)")
        print("   - Try a different sensor if available")
        print("   - Check for loose connections")

if __name__ == "__main__":
    main()
