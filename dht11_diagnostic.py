#!/usr/bin/env python3
"""
DHT11 Diagnostic Script
This script helps identify issues with DHT11 sensor setup
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("🐍 Python Version Check:")
    print(f"   Python version: {sys.version}")
    print(f"   Python executable: {sys.executable}")
    if sys.version_info[0] < 3:
        print("   ⚠️  Warning: Python 2 detected. Use Python 3.")
    else:
        print("   ✅ Python 3 detected")
    print()

def check_libraries():
    """Check for available DHT libraries"""
    print("📚 Library Check:")
    
    libraries = [
        ('adafruit_dht', 'Adafruit CircuitPython DHT'),
        ('board', 'CircuitPython Board'),
        ('Adafruit_DHT', 'Adafruit DHT Legacy'),
        ('RPi.GPIO', 'Raspberry Pi GPIO'),
        ('gpiozero', 'GPIO Zero'),
    ]
    
    available_libs = []
    
    for lib_name, lib_desc in libraries:
        try:
            __import__(lib_name)
            print(f"   ✅ {lib_desc} ({lib_name}) - Available")
            available_libs.append(lib_name)
        except ImportError:
            print(f"   ❌ {lib_desc} ({lib_name}) - Not installed")
    
    print()
    return available_libs

def check_gpio_permissions():
    """Check GPIO file permissions"""
    print("🔐 GPIO Permissions Check:")
    
    gpio_files = [
        '/dev/gpiomem',
        '/dev/mem',
        '/sys/class/gpio'
    ]
    
    for gpio_file in gpio_files:
        if os.path.exists(gpio_file):
            try:
                # Try to access the file
                with open(gpio_file, 'r') as f:
                    pass
                print(f"   ✅ {gpio_file} - Accessible")
            except PermissionError:
                print(f"   ❌ {gpio_file} - Permission denied (try sudo)")
            except Exception as e:
                print(f"   ⚠️  {gpio_file} - {str(e)}")
        else:
            print(f"   ❌ {gpio_file} - Not found")
    
    print()

def check_system_info():
    """Check system information"""
    print("💻 System Information:")
    
    # Check if running on Raspberry Pi
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'Raspberry Pi' in cpuinfo:
                print("   ✅ Running on Raspberry Pi")
                # Extract Pi model
                for line in cpuinfo.split('\n'):
                    if 'Model' in line:
                        print(f"   📱 {line.strip()}")
                        break
            else:
                print("   ⚠️  Not running on Raspberry Pi")
    except FileNotFoundError:
        print("   ❓ Cannot determine if running on Raspberry Pi")
    
    # Check OS
    print(f"   🖥️  Operating System: {os.name}")
    
    # Check if GPIO interface is enabled
    if os.path.exists('/sys/class/gpio'):
        print("   ✅ GPIO interface appears to be available")
    else:
        print("   ❌ GPIO interface not found")
        print("      Run: sudo raspi-config → Interface Options → GPIO → Enable")
    
    print()

def provide_installation_commands():
    """Provide installation commands"""
    print("🛠️  Installation Commands:")
    print("   If libraries are missing, try these commands:")
    print()
    print("   # Update system")
    print("   sudo apt update && sudo apt upgrade -y")
    print()
    print("   # Install Python libraries (choose one method):")
    print("   # Method 1 (Recommended):")
    print("   pip3 install adafruit-circuitpython-dht")
    print("   sudo apt-get install libgpiod2")
    print()
    print("   # Method 2 (Legacy):")
    print("   pip3 install Adafruit_DHT")
    print()
    print("   # Method 3 (Alternative):")
    print("   pip3 install RPi.GPIO")
    print()
    print("   # If permission issues:")
    print("   sudo pip3 install adafruit-circuitpython-dht")
    print()

def test_simple_gpio():
    """Test basic GPIO functionality"""
    print("⚡ GPIO Test:")
    
    try:
        import RPi.GPIO as GPIO
        print("   ✅ RPi.GPIO library available")
        
        # Test basic GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT)
        GPIO.output(4, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW)
        GPIO.cleanup()
        print("   ✅ Basic GPIO operations successful")
        
    except ImportError:
        print("   ❌ RPi.GPIO not available")
    except Exception as e:
        print(f"   ❌ GPIO test failed: {str(e)}")
        print("   💡 Try running with sudo: sudo python3 dht11_diagnostic.py")
    
    print()

def main():
    """Main diagnostic function"""
    print("=" * 60)
    print("         DHT11 Sensor Diagnostic Tool")
    print("         Raspberry Pi 4B")
    print("=" * 60)
    print()
    
    check_python_version()
    available_libs = check_libraries()
    check_gpio_permissions()
    check_system_info()
    test_simple_gpio()
    
    print("🔍 Diagnosis Summary:")
    if 'adafruit_dht' in available_libs and 'board' in available_libs:
        print("   ✅ Adafruit CircuitPython DHT is available")
        print("   💡 You can use: python3 dht11_realtime.py")
    elif 'Adafruit_DHT' in available_libs:
        print("   ✅ Adafruit DHT Legacy is available")
        print("   💡 You can use: python3 dht11_alternative.py")
    elif 'RPi.GPIO' in available_libs:
        print("   ✅ RPi.GPIO is available")
        print("   💡 You can use: python3 dht11_alternative.py")
    else:
        print("   ❌ No suitable DHT libraries found")
        print("   💡 Install libraries using commands below")
    
    print()
    provide_installation_commands()
    
    print("🔌 Hardware Setup Reminder:")
    print("   DHT11 VCC  → Pi Pin 1 (3.3V)")
    print("   DHT11 GND  → Pi Pin 6 (Ground)")
    print("   DHT11 DATA → Pi Pin 7 (GPIO4)")
    print()
    print("Run this diagnostic again after installing libraries!")

if __name__ == "__main__":
    main()
