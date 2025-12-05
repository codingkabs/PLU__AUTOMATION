## PLU Auto Entry Automation

This project automates PLU training and testing by recognising the on screen product image, comparing it against template screenshots, and typing the correct PLU automatically. Unknown items are saved for later labelling, and the script can detect an ending screen to stop the run. It exists because manually entering dozens of PLU codes is not enjoyable for anyone.

## Table of Contents

Overview  
Features  
Prerequisites  
How It Works  
Project Structure  
Setup and Usage  
Accuracy Tips  
Other Use Cases  
Final Notes  

## Overview

The script captures a fixed region of the screen containing the product image. It compares that image against template files, finds the closest match, and types the corresponding PLU. If confidence is low, the screenshot is saved as an unknown item. A designated STOP template ends the script. Moving the mouse to the top left corner triggers a fail safe exit.

## Features

Automatic region capture for the product image  
Template based comparison  
Automatic PLU typing and submission  
Saving of unknown items for later labelling  
STOP template detection for controlled termination  
Fail safe stop by moving the cursor to the top left  
Configurable speed and match threshold  

## Prerequisites

Python 3.9 or later  
Windows 10 or 11  
pip installed  

Install required packages:  
pip install opencv-python pyautogui numpy

## How It Works

Screen capture  
The script takes a screenshot and extracts the product image using fixed coordinates.

Template comparison  
All template images inside the templates folder are loaded and compared to the current screenshot using a difference score. The smallest score indicates the closest match.

PLU entry  
If the match is confident, the script types the PLU and submits it using Enter.

Unknown item handling  
If no confident match is found, the screenshot is saved with an incremental filename such as unknown_017.png. The script enters zero to progress.

STOP detection  
If a template mapped to STOP is detected, the script ends immediately.

Fail safe  
Dragging the mouse to the top left corner instantly stops execution.

## Project Structure

project  
auto_plu.py  
get_position.py  
templates  
known templates  
unknown_001.png  
unknown_002.png  
unknown_083.png  

## Setup and Usage

Step 1  
Open your emulator and position the training or testing screen. Do not move or resize the window once coordinates are captured.

Step 2  
Use a coordinate capture tool to record the following values:  
IMAGE_LEFT  
IMAGE_TOP  
IMAGE_RIGHT  
IMAGE_BOTTOM  
Enter these values into the script.

Step 3  
Run the script using:  
python auto_plu.py  
Click on the emulator window during the countdown.

Step 4  
The automation will recognise items, input PLUs, save unknowns, and stop when the STOP template appears.

Step 5  
Review unknown images in the templates folder and assign PLU values by updating the mapping in the script.

## Accuracy Tips

Use consistent, tightly cropped template images  
Keep the emulator window fixed in the same place and size  
Lower MATCH_THRESHOLD for stricter recognition  
If accuracy drops, recheck the window position and coordinates  

## Other Use Cases

The same method can be used for general screen based automation including:  
User interface testing  
Dataset creation via screenshot capture  
Simulation or training interfaces  
Simple game automation requiring image based input  
Any workflow where visual detection triggers an action  

## Final Notes

The project intentionally avoids complex machine learning. The deterministic pixel based method is easy to debug, fast to run, and accurate when the environment is controlled. More advanced methods such as OCR or structural similarity metrics can be layered on top if needed but are not required for reliable operation.
