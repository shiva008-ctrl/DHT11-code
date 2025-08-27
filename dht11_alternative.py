#!/usr/bin/env python3
"""
Simple DHT11 test script using RPi.GPIO library
Alternative implementation for systems where CircuitPython doesn't work
"""

import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime

# DHT11 sensor pin
DHT_PIN = 4

def read_dht11():
    """
    Read temperature and humidity from DHT11 sensor
    Returns tuple (temperature, humidity) or (None, None) if error
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DHT_PIN, GPIO.OUT)
    
    # Send start signal
    GPIO.output(DHT_PIN, GPIO.LOW)
    time.sleep(0.02)  # 20ms
    GPIO.output(DHT_PIN, GPIO.HIGH)
    time.sleep(0.00004)  # 40us
    
    GPIO.setup(DHT_PIN, GPIO.IN)
    
    # Read data
    data = []
    timeout_counter = 0
    
    # Wait for sensor response
    while GPIO.input(DHT_PIN) == GPIO.HIGH:
        timeout_counter += 1
        if timeout_counter > 1000:
            GPIO.cleanup()
            return None, None
    
    # Read 40 bits of data
    for i in range(40):
        # Wait for high signal
        timeout_counter = 0
        while GPIO.input(DHT_PIN) == GPIO.LOW:
            timeout_counter += 1
            if timeout_counter > 1000:
                GPIO.cleanup()
                return None, None
        
        # Measure high signal duration
        start_time = time.time()
        timeout_counter = 0
        while GPIO.input(DHT_PIN) == GPIO.HIGH:
            timeout_counter += 1
            if timeout_counter > 1000:
                GPIO.cleanup()
                return None, None
        
        duration = time.time() - start_time
        
        # Determine if bit is 0 or 1
        if duration > 0.00005:  # 50us threshold
            data.append(1)
        else:
            data.append(0)
    
    GPIO.cleanup()
    
    # Convert bits to bytes
    humidity_int = 0
    humidity_dec = 0
    temp_int = 0
    temp_dec = 0
    checksum = 0
    
    for i in range(8):
        humidity_int += data[i] * (2 ** (7 - i))
    for i in range(8, 16):
        humidity_dec += data[i] * (2 ** (15 - i))
    for i in range(16, 24):
        temp_int += data[i] * (2 ** (23 - i))
    for i in range(24, 32):
        temp_dec += data[i] * (2 ** (31 - i))
    for i in range(32, 40):
        checksum += data[i] * (2 ** (39 - i))
    
    # Verify checksum
    if (humidity_int + humidity_dec + temp_int + temp_dec) & 0xFF != checksum:
        return None, None
    
    humidity = humidity_int + humidity_dec * 0.1
    temperature = temp_int + temp_dec * 0.1
    
    return temperature, humidity

def main():
    """Main function for alternative DHT11 reading"""
    print("DHT11 Sensor Test (RPi.GPIO version)")
    print("Press Ctrl+C to exit")
    print("-" * 40)
    
    try:
        while True:
            temperature, humidity = read_dht11()
            
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if temperature is not None and humidity is not None:
                temp_f = temperature * 9.0 / 5.0 + 32.0
                print(f"[{current_time}] Temp: {temperature:.1f}°C ({temp_f:.1f}°F), Humidity: {humidity:.1f}%")
            else:
                print(f"[{current_time}] Failed to read sensor data")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        GPIO.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    main()
