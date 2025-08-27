# DHT11 Sensor Setup and Installation Guide

## Hardware Requirements
- Raspberry Pi 4B
- DHT11 Temperature and Humidity Sensor
- Jumper wires (3 wires minimum)
- Breadboard (optional)

## Wiring Diagram
```
DHT11 Sensor    →    Raspberry Pi 4B
VCC (+)         →    3.3V (Physical Pin 1)
GND (-)         →    Ground (Physical Pin 6)
DATA (Signal)   →    GPIO4 (Physical Pin 7)
```

## Installation Steps

### 1. Update your Raspberry Pi
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Python dependencies
```bash
# Install pip if not already installed
sudo apt install python3-pip -y

# Install required libraries
pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2

# Alternative method if above doesn't work:
pip3 install RPi.GPIO
pip3 install Adafruit_DHT
```

### 3. Enable GPIO (if needed)
```bash
# Enable GPIO interface
sudo raspi-config
# Navigate to Interface Options → GPIO → Enable
```

### 4. Run the script
```bash
# Make the script executable
chmod +x dht11_realtime.py

# Run the script
python3 dht11_realtime.py
```

## Troubleshooting

### Issue: Script shows header but doesn't read data

**Symptoms:**
- Script displays "GPIO Pin: 4 (Physical Pin 7)" and "Press Ctrl+C to exit"
- No temperature/humidity readings appear
- Script seems to hang

**Solutions:**

#### Step 1: Run Diagnostic
```bash
python3 dht11_diagnostic.py
```
This will check your system and identify missing libraries or permission issues.

#### Step 2: Check Library Installation
```bash
# Try installing with different methods:

# Method 1 (Recommended):
pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2

# Method 2 (If Method 1 fails):
sudo pip3 install adafruit-circuitpython-dht

# Method 3 (Legacy library):
pip3 install Adafruit_DHT

# Method 4 (Basic GPIO):
pip3 install RPi.GPIO
```

#### Step 3: Permission Issues
```bash
# Try running with sudo permissions:
sudo python3 dht11_realtime.py

# Or use the enhanced version:
sudo python3 dht11_enhanced.py
```

#### Step 4: Hardware Check
1. **Verify Wiring:**
   ```
   DHT11 VCC  → Pi Pin 1 (3.3V) - RED wire
   DHT11 GND  → Pi Pin 6 (Ground) - BLACK wire  
   DHT11 DATA → Pi Pin 7 (GPIO4) - YELLOW/WHITE wire
   ```

2. **Check Power Supply:**
   - Ensure stable 3.3V power
   - Try using Pin 17 (5V) instead of Pin 1 (3.3V) for VCC

3. **Test Different GPIO Pin:**
   - Try GPIO17 (Pin 11) instead of GPIO4 (Pin 7)
   - Modify the code: change `board.D4` to `board.D17`

#### Step 5: Alternative Scripts
If main script doesn't work, try these alternatives:

```bash
# Enhanced version with better error handling:
python3 dht11_enhanced.py

# Simple version using RPi.GPIO:
python3 dht11_alternative.py
```

### Common Issues:

1. **"Import board could not be resolved"**
   ```bash
   pip3 install adafruit-circuitpython-dht
   sudo apt-get install libgpiod2
   ```

2. **"Permission denied" or "timeout" errors**
   ```bash
   sudo python3 dht11_realtime.py
   ```

3. **"No module named 'board'"**
   ```bash
   # Install CircuitPython libraries:
   pip3 install adafruit-blinka
   pip3 install adafruit-circuitpython-dht
   ```

4. **GPIO not accessible**
   ```bash
   sudo raspi-config
   # Navigate to Interface Options → GPIO → Enable
   sudo reboot
   ```

5. **Sensor returns None values**
   - Check wiring connections
   - Ensure sensor is genuine DHT11 (not DHT22)
   - Try different GPIO pin
   - Check for loose connections

### Alternative GPIO Pins:
If GPIO4 doesn't work, you can try these pins (modify the code):
- GPIO17 (Physical Pin 11): `board.D17`
- GPIO27 (Physical Pin 13): `board.D27`
- GPIO22 (Physical Pin 15): `board.D22`

## Features of the Script:
- Real-time temperature and humidity monitoring
- Displays both Celsius and Fahrenheit
- Comfort level indicator
- Error handling and statistics
- Clean terminal interface
- Graceful exit with Ctrl+C

## Expected Output:
The script will display live readings every 2 seconds with:
- Current temperature in °C and °F
- Humidity percentage
- Comfort level assessment
- Reading statistics
- Error tracking
