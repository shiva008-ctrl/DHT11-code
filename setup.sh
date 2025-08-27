#!/bin/bash

# DHT11 Sensor Setup Script for Raspberry Pi 4B
# This script installs all necessary dependencies

echo "==================================="
echo "DHT11 Sensor Setup for Raspberry Pi"
echo "==================================="

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "Installing Python and pip..."
sudo apt install python3 python3-pip -y

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install libgpiod2 -y

# Install Python libraries
echo "Installing Python libraries..."
pip3 install adafruit-circuitpython-dht
pip3 install RPi.GPIO
pip3 install Adafruit_DHT

# Alternative installation method
echo "Installing alternative libraries..."
sudo pip3 install adafruit-circuitpython-dht
sudo pip3 install RPi.GPIO

# Make scripts executable
echo "Making scripts executable..."
chmod +x dht11_realtime.py
chmod +x dht11_alternative.py

# Enable GPIO interface
echo "GPIO interface should be enabled in raspi-config if not already done."
echo "Run: sudo raspi-config → Interface Options → GPIO → Enable"

echo ""
echo "Setup complete!"
echo "You can now run:"
echo "  python3 dht11_realtime.py"
echo "or"
echo "  python3 dht11_alternative.py"
echo ""
echo "Wiring:"
echo "  DHT11 VCC  → Pi Pin 1 (3.3V)"
echo "  DHT11 GND  → Pi Pin 6 (Ground)"
echo "  DHT11 DATA → Pi Pin 7 (GPIO4)"
