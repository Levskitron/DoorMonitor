# DoorMonitor
**THIS PROJECT IS NO LONGER BEING DEVELOPED OR MAINTAINED!**

A Python-based IoT program that determines whether a door is **OPEN** or **CLOSED**, and estimates the percentage it is open, based on sensor data and will send an email to a predefined user if a door has been open for longer than 5 minutes.

## Project Overview

**DoorMonitor** is a group project developed for the class **QBCN-F241B Internet of Things (IOT)**. The primary goal is to monitor door activity using sensor input and intelligently assess the door’s state — either **CLOSED** or **OPEN** (≥1% open). The program will also sense whether a door has been left open for longer than 5 minutes, and if it has, then the program will send an alert email to a predefined email.
## Team Members

- Levi  
- Aidan  
- Imdad
- Calvin

## Features

- Reads and processes sensor input.
- Calculates the percentage a door is open.
- Determines door state: `CLOSED` or `OPEN`.

## Hardware and Software Used

- Python 3
- Visual Studio Code
- RaspberryPi
- GitHub

## How to Run
Run the file "doormonitor.py" in the IDE of your choice. 

### Prerequisites

- [Python 3.13.3](https://www.python.org/downloads/)
- Most libraries used in this project come built in with Python 3.
- If you are on a **RaspberryPi** ensure that you download the libraries found in **requirements.txt**, otherwise physical sensors will not function with the program. To do this, ensure that you have pip installed and run ``pip install -r requirements.txt`` after cloning the repository to your machine.
- If you are running the program on Windows, you currently cannot use this program with real sensor inputs, and can only run with the inbuilt simulated sensor data located in ``sensor_interface.py``.

### Installation

To clone the repository to your machine, run the following commands in a command prompt:

```bash
cd path/to/your/folder
git clone https://github.com/Levskitron/DoorMonitor.git
```

Or, open **Visual Studio Code**, go to the source control tab in the left menu, and press "Clone repository", if you are a collaborator, you can sign into GitHub through VS Code, and clone the repository to a specific folder.
- If you are not a collaborator, you will need to fork this repository, and then follow the steps above.

## BUGS AND ISSUES
This program was abandoned during the development phase of this project. The program itself did not work during the testing phase, so we switched to Node-RED to achieve the assignment requirements. The issues with this program primarily lie in a lack of debugging ability to test whether the program can detect any 4-20mA input, and regardless, the program at the moment does not seem to convert any inputs (if it even receives any) into a percentage or anything significant.

If you stumble across this repository and feel like working on the program on your own, feel free too! We won't be using it anymore, and it might be something interesting for someone else to figure out in the future.
