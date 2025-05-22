# doormonitor.py

import tkinter as tk
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

from config import (
    USE_SIMULATION, SENSOR_TYPE,
    OPEN_THRESHOLD, ALERT_DELAY_MIN, CHECK_INTERVAL_MS,
    EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_TO,
    SMTP_SERVER, SMTP_PORT
)
from sensor_interface import get_door_percentage

# pre-calc
ALERT_DELAY = timedelta(minutes=ALERT_DELAY_MIN)

def send_email():
    msg = MIMEText("The door has been open for more than "
                   f"{ALERT_DELAY_MIN} minutes.")
    msg["Subject"] = "Door Alert"
    msg["From"]    = EMAIL_ADDRESS
    msg["To"]      = EMAIL_TO

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        log.insert(tk.END, f"[{datetime.now():%H:%M:%S}] Email sent\n")
    except Exception as e:
        log.insert(tk.END, f"[{datetime.now():%H:%M:%S}] Email failed: {e}\n")

# — GUI setup —
root = tk.Tk()
root.title("Door Monitor")

status_label = tk.Label(root, text="Door Status: CLOSED",
                        font=("Arial", 18), fg="green")
status_label.pack(pady=10)

percent_label = tk.Label(root, text="Open 0%", font=("Arial", 14))
percent_label.pack(pady=5)

log = tk.Text(root, height=10, width=50)
log.pack(pady=10)

# — State —
door_open_since = None
email_sent = False

# — Monitor loop —
def monitor_loop():
    global door_open_since, email_sent

    percent = get_door_percentage(USE_SIMULATION)
    now = datetime.now()

    percent_label.config(text=f"Open {percent}%")
    if percent > OPEN_THRESHOLD:
        status_label.config(text="Door Status: OPEN", fg="red")
        if door_open_since is None:
            door_open_since = now
            log.insert(tk.END, f"[{now:%H:%M:%S}] Door opened\n")
        elif now - door_open_since > ALERT_DELAY and not email_sent:
            send_email()
            email_sent = True
    else:
        if door_open_since is not None:
            log.insert(tk.END, f"[{now:%H:%M:%S}] Door closed\n")
        door_open_since = None
        email_sent = False
        status_label.config(text="Door Status: CLOSED", fg="green")

    log.see(tk.END)
    root.after(CHECK_INTERVAL_MS, monitor_loop)

# — Start —
root.after(1000, monitor_loop)
root.mainloop()
