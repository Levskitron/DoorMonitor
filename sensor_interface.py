# sensor_interface.py

import random
import time
from config import SENSOR_TYPE, ADC_CHANNEL, RESISTOR_OHMS, V_REF, MIN_CURRENT_MA, MAX_CURRENT_MA

# === Simulated sensor for development ===
def simulated_door_percentage():
    return random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])

# === Reed switch (digital GPIO) ===
def read_reed_switch():
    import RPi.GPIO as GPIO
    REED_PIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(REED_PIN, GPIO.IN)
    return 100 if GPIO.input(REED_PIN) else 0

# === Ultrasonic (distance → % open) ===
def read_ultrasonic():
    import RPi.GPIO as GPIO
    TRIG = 23
    ECHO = 24
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    # send pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # measure echo
    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        end = time.time()

    distance = (end - start) * 17150  # cm
    if distance < 5:
        return 100
    if distance > 30:
        return 0
    return int(100 - ((distance - 5) / 25) * 100)

# === Potentiometer via MCP3008 ADC ===
def read_adc_sensor():
    import spidev
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1350000
    # read configured channel
    cmd = [1, (8 + ADC_CHANNEL) << 4, 0]
    r = spi.xfer2(cmd)
    raw = ((r[1] & 3) << 8) + r[2]
    # map raw to 0-100%
    return int((raw / 1023) * 100)

# === 4–20 mA sensor via resistor → voltage on MCP3008 ===
def read_420_sensor():
    import spidev
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1350000

    # read the configured channel
    cmd = [1, (8 + ADC_CHANNEL) << 4, 0]
    r = spi.xfer2(cmd)
    raw = ((r[1] & 3) << 8) + r[2]

    # convert raw to voltage
    voltage = (raw / 1023) * V_REF

    # convert voltage to current (I = V / R) in mA
    current_ma = (voltage / RESISTOR_OHMS) * 1000

    # clamp to expected range
    current_ma = max(MIN_CURRENT_MA, min(current_ma, MAX_CURRENT_MA))

    # map 4–20 mA → 0–100%
    percent = ((current_ma - MIN_CURRENT_MA) /
               (MAX_CURRENT_MA - MIN_CURRENT_MA)) * 100

    return int(percent)

# === Dispatcher: picks the right source ===
def get_door_percentage(simulation=True):
    if simulation:
        return simulated_door_percentage()
    if SENSOR_TYPE == "reed":
        return read_reed_switch()
    if SENSOR_TYPE == "ultrasonic":
        return read_ultrasonic()
    if SENSOR_TYPE == "adc":
        return read_adc_sensor()
    if SENSOR_TYPE == "420":
        return read_420_sensor()
    # fallback
    return simulated_door_percentage()  # unknown type → simulate