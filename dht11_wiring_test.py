#!/usr/bin/env python3
"""
DHT11 Wiring and Hardware Test Script
This script helps test your DHT11 hardware connections step by step
"""

import time
import sys

def test_basic_gpio():
    """Test basic GPIO functionality"""
    print("🔌 Testing Basic GPIO Access...")
    try:
        import RPi.GPIO as GPIO
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Test GPIO4 (Pin 7) - where DHT11 data should be connected
        pin = 4
        print(f"   Testing GPIO{pin} (Physical Pin 7)...")
        
        # Set as output and toggle
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)
        
        # Set as input and read
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        state = GPIO.input(pin)
        
        GPIO.cleanup()
        
        print(f"   ✅ GPIO{pin} is accessible, current state: {state}")
        return True
        
    except ImportError:
        print("   ❌ RPi.GPIO library not installed")
        print("   Install with: pip3 install RPi.GPIO")
        return False
    except Exception as e:
        print(f"   ❌ GPIO access failed: {e}")
        print("   Try running with: sudo python3 dht11_wiring_test.py")
        return False

def test_pin_voltages():
    """Guide user through voltage testing"""
    print("\n⚡ Power Supply Test Guide:")
    print("   Use a multimeter to check these voltages:")
    print()
    print("   1. Pi Pin 1 (3.3V) to Pi Pin 6 (GND): Should read ~3.3V")
    print("   2. DHT11 VCC to DHT11 GND: Should read ~3.3V")
    print("   3. Pi Pin 7 (GPIO4) to Pi Pin 6 (GND): Should read 0-3.3V")
    print()
    
    response = input("   Do you have a multimeter to test? (y/n): ").lower().strip()
    if response == 'y':
        voltage = input("   What voltage do you read between Pin 1 and Pin 6? (enter number): ")
        try:
            v = float(voltage)
            if 3.2 <= v <= 3.4:
                print("   ✅ Power supply voltage is good")
                return True
            else:
                print(f"   ⚠️  Voltage {v}V is outside normal range (3.2-3.4V)")
                return False
        except:
            print("   ❓ Invalid voltage reading")
            return False
    else:
        print("   💡 Consider getting a multimeter for hardware debugging")
        return True

def test_wiring_continuity():
    """Guide user through wiring checks"""
    print("\n🔗 Wiring Continuity Test:")
    print("   Please verify these connections:")
    print()
    print("   DHT11 Pin → Raspberry Pi Pin")
    print("   ─────────────────────────────")
    print("   VCC (+)   → Pin 1 (3.3V)")
    print("   GND (-)   → Pin 6 (Ground)")  
    print("   DATA      → Pin 7 (GPIO4)")
    print()
    print("   Common wiring mistakes:")
    print("   ❌ Using Pin 2 (5V) instead of Pin 1 (3.3V)")
    print("   ❌ Wrong ground pin")
    print("   ❌ DATA wire on wrong GPIO pin")
    print("   ❌ Loose connections")
    print("   ❌ Damaged jumper wires")
    print()
    
    wiring_ok = input("   Have you double-checked all connections? (y/n): ").lower().strip()
    return wiring_ok == 'y'

def test_sensor_with_pullup():
    """Test sensor with pull-up resistor simulation"""
    print("\n🔧 Testing DHT11 Communication...")
    
    try:
        import RPi.GPIO as GPIO
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        pin = 4
        
        print("   Testing DHT11 response pattern...")
        
        # Simulate DHT11 start signal
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.02)  # 20ms low
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.00004)  # 40μs high
        
        # Switch to input and check for response
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # DHT11 should pull low for 80μs, then high for 80μs
        start_time = time.time()
        timeout = 0.001  # 1ms timeout
        
        # Wait for DHT11 to respond (pull low)
        while GPIO.input(pin) == GPIO.HIGH:
            if time.time() - start_time > timeout:
                print("   ❌ No response from DHT11 (timeout waiting for low signal)")
                GPIO.cleanup()
                return False
        
        print("   ✅ DHT11 responded to start signal!")
        
        # Wait for DHT11 to go high
        start_time = time.time()
        while GPIO.input(pin) == GPIO.LOW:
            if time.time() - start_time > timeout:
                break
        
        if GPIO.input(pin) == GPIO.HIGH:
            print("   ✅ DHT11 communication pattern detected!")
            GPIO.cleanup()
            return True
        else:
            print("   ⚠️  Partial response from DHT11")
            GPIO.cleanup()
            return False
            
    except Exception as e:
        print(f"   ❌ Communication test failed: {e}")
        try:
            GPIO.cleanup()
        except:
            pass
        return False

def test_alternative_pins():
    """Test DHT11 on alternative GPIO pins"""
    print("\n📍 Testing Alternative GPIO Pins...")
    
    alternative_pins = [17, 18, 22, 27]
    
    print("   If GPIO4 doesn't work, try these pins:")
    for pin in alternative_pins:
        physical_pin = {17: 11, 18: 12, 22: 15, 27: 13}.get(pin, "?")
        print(f"   GPIO{pin} (Physical Pin {physical_pin})")
    
    print("\n   To test a different pin:")
    print("   1. Move DHT11 DATA wire to new pin")
    print("   2. Modify code: change 'board.D4' to 'board.D17' (for GPIO17)")
    print("   3. Run test again")

def provide_hardware_solutions():
    """Provide hardware troubleshooting solutions"""
    print("\n🛠️  HARDWARE TROUBLESHOOTING SOLUTIONS:")
    print("=" * 50)
    
    print("\n1. 🔌 Check Power Supply:")
    print("   • Use Pin 1 (3.3V) NOT Pin 2 (5V)")
    print("   • Ensure stable power connection")
    print("   • Try external 3.3V power supply if Pi power is unstable")
    
    print("\n2. 🔗 Verify Wiring:")
    print("   • DHT11 VCC  → Pi Pin 1 (3.3V) - Usually RED wire")
    print("   • DHT11 GND  → Pi Pin 6 (GND)  - Usually BLACK wire")
    print("   • DHT11 DATA → Pi Pin 7 (GPIO4) - Usually YELLOW/WHITE wire")
    
    print("\n3. 🧪 Test Components:")
    print("   • Try different jumper wires")
    print("   • Test DHT11 sensor with another device")
    print("   • Check for physical damage to sensor")
    
    print("\n4. 🔧 Add Pull-up Resistor:")
    print("   • Connect 4.7kΩ resistor between DATA and VCC")
    print("   • This improves signal reliability")
    
    print("\n5. 📍 Try Different GPIO Pin:")
    print("   • Move DATA wire to GPIO17 (Pin 11)")
    print("   • Update code: board.D4 → board.D17")
    
    print("\n6. ⚡ Power Issues:")
    print("   • Ensure Pi has adequate power supply (5V 3A)")
    print("   • Remove other USB devices to reduce power draw")
    print("   • Check for voltage drops under load")

def main():
    """Main testing function"""
    print("=" * 60)
    print("         DHT11 Hardware Troubleshooting Tool")
    print("         'DHT sensor not found' Error Diagnosis")
    print("=" * 60)
    print()
    
    print("This script will help diagnose why your DHT11 isn't responding...")
    print()
    
    # Test 1: Basic GPIO
    gpio_ok = test_basic_gpio()
    
    # Test 2: Power supply
    power_ok = test_pin_voltages()
    
    # Test 3: Wiring
    wiring_ok = test_wiring_continuity()
    
    # Test 4: Sensor communication
    if gpio_ok and wiring_ok:
        sensor_ok = test_sensor_with_pullup()
    else:
        sensor_ok = False
    
    # Test 5: Alternative pins
    test_alternative_pins()
    
    # Results and recommendations
    print("\n" + "=" * 60)
    print("📋 DIAGNOSIS RESULTS:")
    print("=" * 60)
    
    if gpio_ok and sensor_ok:
        print("✅ Hardware appears to be working!")
        print("💡 The issue might be software-related:")
        print("   • Try: sudo python3 dht11_realtime.py")
        print("   • Check library installation")
        print("   • Use: python3 dht11_quickfix.py")
    elif gpio_ok and not sensor_ok:
        print("⚠️  GPIO works but DHT11 doesn't respond:")
        print("💡 Hardware issue - check wiring and sensor")
    elif not gpio_ok:
        print("❌ GPIO access problems:")
        print("💡 Run with sudo or check permissions")
    else:
        print("❌ Multiple issues detected")
    
    provide_hardware_solutions()
    
    print("\n📞 Next Steps:")
    print("1. Fix any hardware issues identified above")
    print("2. Run: python3 dht11_quickfix.py")
    print("3. Try: sudo python3 dht11_realtime.py")
    print("4. If still failing, try GPIO17 instead of GPIO4")

if __name__ == "__main__":
    main()
