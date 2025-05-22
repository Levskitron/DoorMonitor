import tkinter as tk
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import random

# === CONFIGURATION
OPEN_THRESHOLD = 1
ALERT_DELAY = timedelta(minutes=5)
CHECK_INTERVAL_MS = 5000
EMAIL_SENT_FLAG = False

#EMAIL SETTINGS
EMAIL_ADDRESS = "email@example.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_TO = "recipient_email@example.com"

def send_email():
    subject = "Door Alert"
    body = "The door has been open for more than 5 minutes"
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_TO
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", e)

# SIMULATED SENSOR
def get_door_percentage():
    return random.choice ([0, 1, 0, 15, 30, 60, 0, 0, 100, 5])
                              
#GUI SETUP
root = tk.Tk()
root.title("Door Monitor")

status_label = tk.Label(root, text="Door Status: CLOSED", font=("Arial", 18), fg="green")
status_label.pack(pady=10)

percent_label= tk.Label(root, text="Open 0%", font=("Arial", 14))
percent_label.pack(pady=5)

log = tk.Text(root, height=10, width=50, state='normal')
log.pack(pady=10)

#STATE VARIABLES
door_open_since = None
email_sent = False

# MONITOR LOOP
def monitor_loop():
    global door_open_since, email_sent

    percent_open = get_door_percentage()
    now = datetime.now()

    percent_label.config(text=f"Open {percent_open}%")

    if percent_open > 1:
        status_label.config(text="Door Status: OPEN", fg="red")
        if door_open_since is None:
            door_open_since = now
            log.insert(tk.END, f"[{now:%H:%M:%S}] Door opened. \n")
        elif now - door_open_since > timedelta(minutes=5):
            if not email_sent:
                send_email()
                log.insert(tk.END, f"[{now:%H:%M:%S}] Door open too long! Email sent. \n")
                email_sent = True
    else:
        if door_open_since is not None:
            log.insert(tk.END, f"[{now:%H:%M:%S}] Door closed. \n")
        door_open_since = None
        email_sent = False
        status_label.config(text="Door Status: CLOSED", fg="green")

    log.see(tk.END)
    root.after(5000, monitor_loop)
    
# START LOOP
root.after (1000, monitor_loop)
root.mainloop()