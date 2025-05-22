# sensor_interface.py

import random
import time
from config import SENSOR_TYPE

# — Simulated sensor for development —
def simulated_door_percentage():
    return random.choice([0, 1, 0, 15, 30, 60, 0, 0, 100, 5])

# — Reed switch (digital GPIO) —
def read_reed_switch():
    import RPi.GPIO as GPIO
    REED_PIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(REED_PIN, GPIO.IN)
    return 100 if GPIO.input(REED_PIN) else 0

# — Ultrasonic (distance → “% open”) —
def read_ultrasonic():
    import RPi.GPIO as GPIO
    TRIG = 23
    ECHO = 24
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

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

# — Potentiometer via MCP3008 ADC —
def read_adc_sensor():
    import spidev
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1350000
    # read channel 0
    r = spi.xfer2([1, (8 + 0) << 4, 0])
    value = ((r[1] & 3) << 8) + r[2]
    return int((value / 1023) * 100)

# — 4–20 mA sensor via 250Ω → 1–5 V on MCP3008 channel 0 —
def read_420_sensor():
    import spidev
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1350000
    # read channel 0
    r = spi.xfer2([1, (8 + 0) << 4, 0])
    raw = ((r[1] & 3) << 8) + r[2]
    # MCP3008 gives 0–1023 for 0–3.3 V, but if you scale
    # 4–20 mA through 250 Ω → 1–5 V, clamp & map 1 V–5 V
    # On a 3.3 V ADC you’ll actually max at ~3.3 V (≈100%), so:
    min_adc = int((1.0 / 3.3) * 1023)
    max_adc = 1023
    val = max(min_adc, min(raw, max_adc))
    return int(((val - min_adc) / (max_adc - min_adc)) * 100)

# — Dispatcher: picks the right source —
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
    raise ValueError(f"Unknown SENSOR_TYPE: {SENSOR_TYPE}")
