# config.py

# — Simulation vs. real sensor —
USE_SIMULATION = True       # True = use simulated data
SENSOR_TYPE    = "reed"     # "reed", "adc", "ultrasonic", or "420" (ignored if USE_SIMULATION=True)

# — Door logic —
OPEN_THRESHOLD   = 1                                  # % open to count as “open”
ALERT_DELAY_MIN  = 5                                  # minutes until alert
CHECK_INTERVAL_MS = 5000                              # how often to poll (ms)

# — Email settings —
EMAIL_ADDRESS  = "your_email_address"
EMAIL_PASSWORD = "your_app_password"                  # use a Gmail App Password
EMAIL_TO       = "recipient_email_address"
SMTP_SERVER    = "smtp.gmail.com"
SMTP_PORT      = 465

# 4–20 mA sensor calibration
ADC_CHANNEL    = 0      # MCP3008 channel (0–7)
RESISTOR_OHMS  = 250    # Ω value used in the current-to-voltage conversion
V_REF          = 3.3    # ADC reference voltage (3.3 or 5.0)
MIN_CURRENT_MA = 4      # loop’s minimum current (mA)
MAX_CURRENT_MA = 20     # loop’s maximum current (mA)