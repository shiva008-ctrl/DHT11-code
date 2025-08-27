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

### Common Issues:

1. **Permission Error**
   ```bash
   sudo python3 dht11_realtime.py
   ```

2. **Library Import Error**
   - Try installing with sudo: `sudo pip3 install adafruit-circuitpython-dht`
   - Or use virtual environment

3. **Sensor Not Responding**
   - Check wiring connections
   - Ensure DHT11 is getting 3.3V power
   - Try different GPIO pin (modify code accordingly)

4. **Timeout Errors**
   - Normal occasionally due to sensor timing
   - Check for loose connections
   - Ensure stable power supply

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
