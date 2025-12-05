PLU Auto-Entry Automation

This project automates PLU training and testing by recognising the on-screen product image, matching it against a set of template screenshots, and typing the correct PLU automatically. It also saves unknown items for later labelling and can detect an end screen to stop the run. The idea is simple: stop doing repetitive PLU input manually, because life is too short for that.

Table of Contents

Overview

Features

Prerequisites

How It Works

Project Structure

Setup and Usage

Accuracy Tips

Other Use Cases

Final Notes

Overview

The script captures a defined region of the screen, compares it to a library of template images, identifies the closest match, and automatically enters the PLU code. Unknown items are saved with incremental filenames so you can label them later. A special STOP image ends the script cleanly, and a fail-safe stops everything the moment your mouse touches the top-left corner.

The system is fast, simple, and surprisingly accurate when configured correctly.

Features

Automatic image capture of the product region using exact pixel coordinates.

Template-based image recognition using a lightweight pixel-difference method.

Automatic PLU entry using keyboard automation.

Unknown item handling: screenshots saved for manual labelling later.

Auto-stop behaviour when the script detects the STOP template.

Fail-safe exit: move your mouse to the top-left corner to instantly halt the program.

Configurable thresholds: tune matching tolerance to improve accuracy.

Prerequisites
Software

Python 3.9+

Windows 10 / 11

pip installed

Install dependencies:

pip install opencv-python pyautogui numpy

Emulator

You’ll need an emulator running your PLU training or testing application.
Compatible options include:

Bluestacks

LDPlayer

Windows Subsystem for Android

Screen Coordinates

You must provide the exact product image coordinates using a helper script such as get_position.py. The automation relies on these being accurate. If your window moves even slightly, everything goes downhill very quickly.

How It Works
1. Region Capture

The script takes an entire screenshot, then crops out the specific region containing the product image:

roi = img[IMAGE_TOP:IMAGE_BOTTOM, IMAGE_LEFT:IMAGE_RIGHT]

2. Template Comparison

Each template in the templates/ folder is compared by resizing it to the ROI size and computing a difference score. The template with the lowest score wins.

This works very well because the templates are captured from the exact same environment.

3. PLU Submission

If the match score is below the configured threshold, the script types the PLU and presses Enter:

pyautogui.write(plu)
pyautogui.press("enter")

4. Unknown Items

If the script fails to confidently recognise the item:

The image is saved to the templates folder with a new filename such as unknown_019.png.

The script inputs 0 to keep the flow going.

You can later label the unknown image and add it to the ITEMS dictionary.

5. STOP Image Detection

If a recognised template maps to "STOP":

The script prints a message.

The loop ends immediately.

No PLU is typed.

6. Fail-Safe

If you drag your mouse to the top-left corner, PyAutoGUI raises a fail-safe exception and the script ends immediately. Useful when the script starts behaving too confidently.

Project Structure
project/
│
├── auto_plu.py              # Main automation script
├── get_position.py          # Helper tool to capture cursor positions
│
└── templates/
      ├── known images
      ├── unknown_001.png
      ├── unknown_002.png
      └── unknown_083.png    # STOP template

Setup and Usage
1. Position Your Emulator

Open your training/testing application, position the window, and ensure nothing overlaps the product area.

2. Confirm Coordinates

Use a helper script to confirm:

IMAGE_LEFT / IMAGE_TOP

IMAGE_RIGHT / IMAGE_BOTTOM

Update these inside the main script.

3. Run the Program

From the terminal:

python auto_plu.py


You will get a brief countdown to focus the emulator window.

4. Watch It Work

The script will:

Recognise items

Enter PLUs

Save unknown images

Stop automatically when the STOP template appears

5. Label Unknowns

Open the templates/ folder and label the newly captured unknown images.
Add them to the ITEMS dictionary:

"templates/unknown_019.png": "123",


As you label more templates, accuracy improves.

Accuracy Tips

Use clean, tightly cropped templates that match the screenshot resolution.

Keep the emulator window in the exact same position for every run.

Lower MATCH_THRESHOLD for stricter matching; raise it if the script becomes too picky.

If accuracy suddenly drops, your emulator window likely shifted a pixel. It happens.

Other Use Cases

The system is not limited to PLU matching. It can also be adapted for:

On-screen automation tasks

Lightweight desktop UI testing

Simple dataset creation tools

Training simulations

Image-driven workflows

Basic game automation where each screen corresponds to a predictable action

Anywhere the computer sees an image and must respond with a keystroke or action, this approach works.

Final Notes

This project intentionally avoids heavy machine learning. It relies on consistent screenshots and deterministic matching, which works surprisingly well in structured environments.

If you want to extend this with SSIM, deep learning models, real-time OCR, or more advanced behaviour, that can be added without rewriting the entire system.
