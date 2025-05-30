# test_spi_i2c.py

import spidev
import megaind
from config import (
    ADC_CHANNEL, V_REF,
    RESISTOR_OHMS, MIN_CURRENT_MA, MAX_CURRENT_MA,
    I2C_STACK_LEVEL, I2C_CHANNEL
)

def test_spi():
    print("=== SPI Scan ===")
    for bus in (0, 1):
        for device in (0, 1):
            try:
                spi = spidev.SpiDev()
                spi.open(bus, device)
                spi.max_speed_hz = 1_350_000
                cmd = [1, (8 + ADC_CHANNEL) << 4, 0]
                r = spi.xfer2(cmd)
                raw = ((r[1] & 3) << 8) + r[2]
                voltage = (raw / 1023) * V_REF
                print(f"SPI{bus}, CE{device} → raw={raw:4d}, V={voltage:.2f} V")
                spi.close()
            except Exception as e:
                print(f"SPI{bus}, CE{device} → ERROR: {e}")

def test_i2c():
    print("\n=== I²C Scan (all stack levels × channels 1–4) ===")
    for stack in (0, 1):
        for ch in range(1, 5):
            try:
                raw_ua = megaind.get4_20In(stack, ch)
                current_ma = raw_ua / 1000.0
                current_ma = max(MIN_CURRENT_MA, min(current_ma, MAX_CURRENT_MA))
                percent = ((current_ma - MIN_CURRENT_MA) /
                           (MAX_CURRENT_MA - MIN_CURRENT_MA)) * 100
                raw_int = int(raw_ua)
                print(f"I2C stack={stack}, CH{ch} → "
                      f"{raw_int:6d} µA, {current_ma:5.2f} mA, {percent:5.1f}%")
            except Exception as e:
                print(f"I2C stack={stack}, CH{ch} → ERROR: {e}")

if __name__ == "__main__":
    test_spi()
    test_i2c()
