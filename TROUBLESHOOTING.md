# DHT11 "Sensor Not Found" Error - Troubleshooting Guide

## ❌ Error: "DHT sensor not found, check wiring"

This error means your Raspberry Pi cannot communicate with the DHT11 sensor. Here are the solutions in order of likelihood:

---

## 🚀 QUICK FIXES (Try these first!)

### 1. **Run with sudo permissions**
```bash
sudo python3 dht11_realtime.py
```
**Why:** GPIO access often requires elevated permissions.

### 2. **Check your wiring EXACTLY**
```
DHT11 → Raspberry Pi 4B
VCC   → Pin 1 (3.3V) - RED wire
DATA  → Pin 7 (GPIO4) - YELLOW/WHITE wire  
GND   → Pin 6 (Ground) - BLACK wire
```
**Common mistakes:**
- Using Pin 2 (5V) instead of Pin 1 (3.3V) ❌
- Wrong GPIO pin for DATA wire ❌
- Loose connections ❌

### 3. **Try different GPIO pin**
Move DATA wire from Pin 7 to Pin 11 (GPIO17), then modify your code:
```python
# Change this line:
dht = adafruit_dht.DHT11(board.D4)
# To this:
dht = adafruit_dht.DHT11(board.D17)
```

---

## 🔧 DETAILED TROUBLESHOOTING

### Step 1: Hardware Verification
```bash
# Run hardware check:
python3 dht11_hardware_check.py

# If permission denied:
sudo python3 dht11_hardware_check.py
```

### Step 2: Test Multiple Methods
```bash
# Run the quick fix script:
python3 dht11_quickfix.py

# This will try different libraries and methods
```

### Step 3: Check Libraries
```bash
# Reinstall libraries:
pip3 install --upgrade adafruit-circuitpython-dht
sudo apt-get install libgpiod2

# Alternative library:
pip3 install Adafruit_DHT
```

### Step 4: Physical Inspection

**Check these with multimeter (if available):**
1. **Power:** Pin 1 to Pin 6 should read ~3.3V
2. **Continuity:** Ensure wires are connected properly
3. **Signal:** Pin 7 should show voltage changes

**Visual inspection:**
- Ensure DHT11 pins are inserted fully into breadboard
- Check for bent or damaged pins
- Verify jumper wires are good quality

---

## 🔌 WIRING DIAGRAMS

### DHT11 Pinout (facing front):
```
┌─────────────┐
│  ┌─┐ ┌─┐    │ DHT11 Front View
│  │ │ │ │    │
│  │1│ │2│ │3│ │4│
└──┴─┴─┴─┴─┴─┴─┘
   │   │  │   │
   VCC DATA NC GND
```

### Raspberry Pi GPIO (looking down at board):
```
Pin 1 (3.3V)  ●─●  Pin 2 (5V)
Pin 3 (GPIO2) ●─●  Pin 4 (5V) 
Pin 5 (GPIO3) ●─●  Pin 6 (GND)
Pin 7 (GPIO4) ●─●  Pin 8 (GPIO14)  ← DHT11 DATA goes here
```

---

## 🛠️ ALTERNATIVE SOLUTIONS

### Solution A: Try GPIO17 instead of GPIO4
```bash
# Move DATA wire to Pin 11 (GPIO17)
# Update your code to use board.D17
```

### Solution B: Add Pull-up Resistor
```
Connect 4.7kΩ resistor between:
DHT11 DATA pin ←→ DHT11 VCC pin
```

### Solution C: Different Power Source
```bash
# Try Pin 2 (5V) instead of Pin 1 (3.3V) for VCC
# Some DHT11 modules work better with 5V
```

### Solution D: Use Legacy Library
```bash
pip3 install Adafruit_DHT
python3 dht11_alternative.py
```

---

## 🧪 TEST SCRIPTS AVAILABLE

1. **`dht11_hardware_check.py`** - Basic hardware test
2. **`dht11_wiring_test.py`** - Comprehensive wiring check  
3. **`dht11_quickfix.py`** - Tries multiple methods
4. **`dht11_diagnostic.py`** - Full system diagnosis

---

## 📞 IF NOTHING WORKS

### Hardware Issues:
1. **Bad DHT11 sensor** - Try with another sensor
2. **Faulty jumper wires** - Replace all wires
3. **Breadboard problems** - Try direct connections
4. **Pi GPIO damage** - Test other GPIO pins

### Software Issues:
1. **Library conflicts** - Create fresh virtual environment
2. **OS issues** - Update Raspberry Pi OS
3. **Permission problems** - Always use sudo

---

## ✅ SUCCESS CHECKLIST

Before claiming the sensor is broken, verify:

- [ ] Wiring is exactly as specified above
- [ ] Used sudo when running scripts  
- [ ] Tested multiple GPIO pins (4, 17, 18)
- [ ] Tried different power voltages (3.3V, 5V)
- [ ] Tested with different libraries
- [ ] Checked all physical connections
- [ ] Ensured stable power supply
- [ ] Tested with known-good jumper wires

---

## 🎯 MOST LIKELY SOLUTION

**90% of "sensor not found" errors are fixed by:**

```bash
sudo python3 dht11_realtime.py
```

**If that doesn't work, the issue is usually wiring. Double-check:**
- VCC to Pin 1 (3.3V)  
- DATA to Pin 7 (GPIO4)
- GND to Pin 6 (Ground)

Try the hardware check script to verify your connections!
