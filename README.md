# DoorMonitor.py

A Python-based IoT program that determines whether a door is **OPEN** or **CLOSED**, and estimates the percentage it is open, based on sensor data and will send an email to a predefined user if a door has been open for longer than 5 minutes.

## Project Overview

**DoorMonitor.py** is a group project developed for the class **QBCN-F241B Internet of Things (IOT)**. The primary goal is to monitor door activity using sensor input and intelligently assess the door’s state — either **CLOSED** or **OPEN** (≥1% open). The program will also sense whether a door has been left over for longer than 5 minutes, and if it has, then the program will send an alert email to a predefined email.
## Team Members

- Levi  
- Aidan  
- Imdad

## Features

- Reads and processes sensor input.
- Calculates the percentage a door is open.
- Determines door state: `CLOSED` or `OPEN`.

## Hardware and Software Used

- Python 3
- Virtual Studio Code
- RaspberryPi
- GitHub

## How to Run
Run the file "doormonitor.py" in the IDE of your choice.

### Prerequisites

- [Python 3.13.3](https://www.python.org/downloads/)
- All libraries used in this project come built in with Python 3

### Installation

Clone the repository:

```bash
cd (file_path_where_you_want_clone_to_be)
git clone https://github.com/your-username/DoorMonitor.py.git
```
