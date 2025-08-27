#!/usr/bin/env python3
"""
Simple DHT11 Hardware Check
No external libraries required - just basic file system access
"""

import os
import time

def check_gpio_files():
    """Check if GPIO files are accessible"""
    print("🔍 Checking GPIO System Files...")
    
    gpio_paths = [
        "/sys/class/gpio",
        "/dev/gpiomem", 
        "/dev/mem"
    ]
    
    accessible = []
    
    for path in gpio_paths:
        if os.path.exists(path):
            try:
                # Try to access the path
                if os.path.isdir(path):
                    os.listdir(path)
                    accessible.append(path)
                    print(f"   ✅ {path} - Accessible")
                else:
                    with open(path, 'r') as f:
                        pass
                    accessible.append(path)
                    print(f"   ✅ {path} - Accessible")
            except PermissionError:
                print(f"   ❌ {path} - Permission denied (try sudo)")
            except Exception as e:
                print(f"   ⚠️  {path} - {str(e)}")
        else:
            print(f"   ❌ {path} - Not found")
    
    return len(accessible) > 0

def test_gpio4_export():
    """Try to export GPIO4 and test it"""
    print("\n🔌 Testing GPIO4 (DHT11 Data Pin)...")
    
    try:
        # Export GPIO4
        with open('/sys/class/gpio/export', 'w') as f:
            f.write('4')
        print("   ✅ GPIO4 exported successfully")
        
        time.sleep(0.1)
        
        # Set direction to output
        with open('/sys/class/gpio/gpio4/direction', 'w') as f:
            f.write('out')
        print("   ✅ GPIO4 set to output")
        
        # Test writing values
        with open('/sys/class/gpio/gpio4/value', 'w') as f:
            f.write('1')
        time.sleep(0.1)
        
        with open('/sys/class/gpio/gpio4/value', 'w') as f:
            f.write('0')
        print("   ✅ GPIO4 output test successful")
        
        # Set to input and read
        with open('/sys/class/gpio/gpio4/direction', 'w') as f:
            f.write('in')
        
        with open('/sys/class/gpio/gpio4/value', 'r') as f:
            value = f.read().strip()
        print(f"   ✅ GPIO4 input test successful (value: {value})")
        
        # Cleanup
        with open('/sys/class/gpio/unexport', 'w') as f:
            f.write('4')
        print("   ✅ GPIO4 unexported")
        
        return True
        
    except PermissionError:
        print("   ❌ Permission denied - try running with sudo")
        return False
    except FileNotFoundError as e:
        print(f"   ❌ GPIO file not found: {e}")
        return False
    except Exception as e:
        print(f"   ❌ GPIO test failed: {e}")
        return False

def main():
    """Main hardware check"""
    print("=" * 50)
    print("    DHT11 Hardware Quick Check")
    print("=" * 50)
    print()
    
    # Check basic GPIO access
    gpio_accessible = check_gpio_files()
    
    # Test specific GPIO pin
    if gpio_accessible:
        gpio4_ok = test_gpio4_export()
    else:
        gpio4_ok = False
        print("\n❌ Cannot access GPIO system - try running with sudo")
    
    print("\n" + "=" * 50)
    print("🔧 IMMEDIATE SOLUTIONS FOR 'DHT SENSOR NOT FOUND':")
    print("=" * 50)
    
    if not gpio_accessible:
        print("\n1. 🔑 PERMISSION ISSUE:")
        print("   sudo python3 dht11_realtime.py")
        print("   sudo python3 dht11_quickfix.py")
    
    print("\n2. 🔌 CHECK PHYSICAL WIRING:")
    print("   DHT11 Pin 1 (VCC)  → Pi Pin 1 (3.3V)")
    print("   DHT11 Pin 2 (DATA) → Pi Pin 7 (GPIO4)")  
    print("   DHT11 Pin 4 (GND)  → Pi Pin 6 (Ground)")
    print("   NOTE: DHT11 Pin 3 is not connected")
    
    print("\n3. 🔄 TRY DIFFERENT GPIO PIN:")
    print("   Move DATA wire from Pin 7 to Pin 11 (GPIO17)")
    print("   Then modify code: board.D4 → board.D17")
    
    print("\n4. ⚡ POWER TROUBLESHOOTING:")
    print("   • Ensure stable 3.3V power (NOT 5V)")
    print("   • Check all connections are secure")
    print("   • Try different jumper wires")
    
    print("\n5. 🧪 TEST WITH ALTERNATIVE SCRIPT:")
    print("   python3 dht11_wiring_test.py")
    print("   python3 dht11_quickfix.py")
    
    print("\n6. 📦 LIBRARY ISSUES:")
    print("   pip3 install --upgrade adafruit-circuitpython-dht")
    print("   sudo apt-get install libgpiod2")
    
    if gpio4_ok:
        print("\n✅ GPIO4 hardware test passed!")
        print("💡 Issue is likely software/library related")
        print("   Try: sudo python3 dht11_realtime.py")
    elif gpio_accessible:
        print("\n⚠️  GPIO accessible but GPIO4 test failed")
        print("💡 Try running with sudo permissions")
    else:
        print("\n❌ GPIO system not accessible")
        print("💡 Must run with sudo for GPIO access")
    
    print("\n📋 NEXT STEPS:")
    print("1. Run: sudo python3 dht11_hardware_check.py")
    print("2. If that works, run: sudo python3 dht11_realtime.py") 
    print("3. Check physical wiring with multimeter if available")
    print("4. Try different GPIO pin (GPIO17 = Pin 11)")

if __name__ == "__main__":
    main()
