==================================================
PLU AUTO ENTRY AUTOMATION
==================================================

This project automates PLU training and testing by recognising the on screen product image, comparing it against template screenshots, and typing the correct PLU automatically. It also saves unknown items for later labelling and detects an ending screen to stop the run. It exists because manually entering long lists of PLU codes is not the best use of anyone’s day.

==================================================
TABLE OF CONTENTS
==================================================

Overview
Features
Prerequisites
How It Works
Project Structure
Setup and Usage
Accuracy Tips
Other Use Cases
Final Notes

==================================================
OVERVIEW
==================================================

The script captures a specified region of the screen, compares that region against existing template images, selects the closest match, and types the corresponding PLU. If no confident match is found, the script saves the screenshot to the templates folder and enters zero. A designated STOP template ends the script immediately. Moving the mouse to the top left corner stops execution through a built in fail safe.

The system is fast, consistent, and highly accurate when configured correctly.

==================================================
FEATURES
==================================================

Automatic extraction of the product image region
Template based comparison and matching
Automatic typing and submission of correct PLUs
Saving of unknown images for later manual tagging
STOP template detection for clean and instant termination
Fail safe exit by moving cursor to the top left
Configurable speed and matching threshold

==================================================
PREREQUISITES
==================================================

Python 3.9 or later
Windows 10 or 11
pip installed

Install dependencies using:
pip install opencv-python pyautogui numpy

==================================================
HOW IT WORKS
==================================================

Screen Region Capture
The script takes a screenshot and crops it using the configured coordinates. Only the area containing the product is processed.

Template Comparison
All templates in the templates folder are loaded and compared to the captured image. A simple pixel difference score is used to determine similarity. The template with the lowest score is treated as the predicted match.

PLU Entry
If the match score is below a defined threshold, the associated PLU value is typed followed by Enter.

Unknown Item Handling
If confidence is low, the screenshot is saved with an incremental filename such as unknown_017.png. The script submits zero and moves on.

STOP Detection
If the matched PLU corresponds to STOP, the script prints a message and exits immediately.

Fail Safe Exit
Moving the mouse to the top left corner causes the script to stop at once.

==================================================
PROJECT STRUCTURE
==================================================

project
auto_plu.py
get_position.py
templates
known templates
unknown_001.png
unknown_002.png
unknown_083.png

==================================================
SETUP AND USAGE
==================================================

Step 1
Open your emulator and position the PLU training or testing window. Once coordinates are captured, do not move or resize the window.

Step 2
Use a coordinate capture tool to determine:
IMAGE_LEFT
IMAGE_TOP
IMAGE_RIGHT
IMAGE_BOTTOM
Enter these values in the main script.

Step 3
Run the program:
python auto_plu.py
Focus the emulator window during the countdown.

Step 4
The script will process items sequentially. It will recognise known items, enter PLUs, save unknowns, and stop when the STOP template is detected.

Step 5
To improve accuracy, label unknown images by assigning PLU values in the mapping within the script. Over time the template library becomes complete and extremely reliable.

==================================================
ACCURACY TIPS
==================================================

Ensure templates are tightly cropped and consistent in size
Keep the emulator in the same position and size every time
Lower MATCH_THRESHOLD for stricter comparison
If results deteriorate, recheck your coordinates and ensure window alignment is unchanged

==================================================
OTHER USE CASES
==================================================

The same approach can automate any screen based workflow where actions depend on recognising visuals. Suitable areas include:
General UI automation
Lightweight software testing
Dataset generation through repeated screenshot capture
Simulation or training interface automation
Basic game automation driven by static screens

Any rule of the form when this picture appears perform this action can be implemented using this method.

==================================================
FINAL NOTES
==================================================

This project avoids heavy machine learning intentionally. The deterministic pixel based method is fast, predictable, and simple to debug. It provides a strong base for future enhancements such as OCR, structural similarity metrics, or more sophisticated recognition methods if desired.
