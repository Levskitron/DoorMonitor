# config.py

# — Simulation vs. real sensor —
USE_SIMULATION = True       # True = use simulated data
SENSOR_TYPE    = "reed"     # "reed", "adc", "ultrasonic", or "420" (ignored if USE_SIMULATION=True)

# — Door logic —
OPEN_THRESHOLD   = 1                                  # % open to count as “open”
ALERT_DELAY_MIN  = 5                                  # minutes until alert
CHECK_INTERVAL_MS = 5000                              # how often to poll (ms)

# — Email settings —
EMAIL_ADDRESS  = "email@example.com"
EMAIL_PASSWORD = "your_app_password"                  # use a Gmail App Password
EMAIL_TO       = "recipient_email@example.com"
SMTP_SERVER    = "smtp.gmail.com"
SMTP_PORT      = 465
