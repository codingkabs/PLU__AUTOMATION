# PLU Auto-Entry Automation

This project automates PLU training and testing by recognising the on-screen product image, matching it against a set of template screenshots, and typing the correct PLU automatically. It also saves unknown items for later labelling and detects an ending screen so it can stop cleanly. The motive was simple: entering 60+ PLU codes manually is a special form of punishment, and automation exists for a reason.

---

## Table of Contents

- Overview
- Features
- Prerequisites
- How It Works
- Project Structure
- Setup and Usage
- Accuracy Tips
- Other Use Cases
- Final Notes

---

## Overview

The script captures a fixed region of the screen, compares it with your existing templates, identifies the closest match, and enters the corresponding PLU. If the item is unknown, the system automatically saves the screenshot so you can label it later. A special STOP template ends the run, and a fail-safe mechanism stops everything if the mouse is moved to the top-left corner.

The system is fast, simple, and surprisingly accurate when configured correctly.

---

## Features

- Automated product-region screenshot capture.
- Template-matching with configurable tolerance.
- Automatic PLU input through keyboard simulation.
- Automatic saving of unknown items for later tagging.
- STOP-template detection for clean shutdown.
- Fail-safe exit by moving the cursor to the top-left.
- Adjustable delays for speed control.

---

## Prerequisites

### Software Required

- Python 3.9 or later  
- Windows 10 or 11  
- pip installed  

Install the required dependencies:

pip install opencv-python pyautogui numpy

(Left plain so it does not break formatting.)

---

## How It Works

### 1. Screen Region Capture

The script uses fixed coordinates to extract the portion of the display showing the current product image.

python
roi = img[IMAGE_TOP:IMAGE_BOTTOM, IMAGE_LEFT:IMAGE_RIGHT]


### 2. Template Comparison

Each template image in the `templates` folder is loaded and compared to the current screenshot using a simple image-difference method.  
The template with the lowest difference score is selected.

### 3. PLU Entry

If the match score falls below the defined threshold, the script types the PLU using simulated keyboard input and submits it.

### 4. Unknown Handling

If no template confidently matches:

- The current screenshot is saved as `unknown_###.png`
- The script enters `0` to move forward  
- You can later label the unknown files and add them to the ITEMS dictionary

### 5. STOP Detection

If a matched template corresponds to `"STOP"`:

- The script prints a message  
- Immediately exits  

### 6. Fail-Safe

Dragging your mouse to the top-left corner instantly stops the script, which is very useful when something unexpected happens.

---

## Project Structure

project/
│
├── auto_plu.py # Main automation script
├── get_position.py # Helper tool for coordinate capture
│
└── templates/
├── known templates
├── unknown_001.png
├── unknown_002.png
└── unknown_083.png # STOP template



---

## Setup and Usage

### 1. Open Your Emulator

Set up your PLU training/testing environment and position the window exactly where your coordinates expect it.  
Do not move or resize it during operation.

### 2. Configure Coordinates

Use a helper tool to record:

- IMAGE_LEFT  
- IMAGE_TOP  
- IMAGE_RIGHT  
- IMAGE_BOTTOM  

Update these in your script.

### 3. Run the Program

Run:

python auto_plu.py

Then click on the emulator window during the countdown.

### 4. Script Behaviour

The script will:

- Recognise known items  
- Enter PLUs  
- Save unknown images  
- Stop automatically when the STOP screen is detected  

### 5. Labelling Unknowns

Inside the `templates` folder you will find new unknown images:

