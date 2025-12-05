PLU Auto-Entry Automation

This project automates PLU training and testing by recognising the product image shown on the screen, matching it against a set of template images, and automatically typing the correct PLU number. The script can also handle unknown items, save their images for later labelling, and stop automatically when the ending screen appears. It was built out of necessity, but also because entering 60+ PLU codes by hand is not anyone’s idea of a good time.

What This Project Actually Does

Captures only the product portion of your screen using exact pixel coordinates.

Compares that captured image against your template library using simple pixel-difference matching.

Types the corresponding PLU using the keyboard.

If the script is unsure, it saves the screenshot into the templates folder for you to label later.

Recognises a special template (the “STOP” screen) and gracefully ends the run.

Stops instantly if you drag your mouse to the top-left corner of the screen. Handy for when things go off-track.

The goal is simple: automate repetitive PLU entry and make the whole process bearable.

Prerequisites
Software

Python 3.9 or newer

pip installed

Windows 10 or 11

Install dependencies:

pip install opencv-python pyautogui numpy

Emulator

You’ll need an emulator running the PLU training/testing application. Bluestacks, LDPlayer, and Windows Subsystem for Android all work fine.

Screen Coordinates

The script relies on fixed pixel coordinates.
If the window moves, the automation becomes confused very quickly, so use a helper script to record:

IMAGE_LEFT / IMAGE_TOP

IMAGE_RIGHT / IMAGE_BOTTOM

Once these are correct, the system becomes very reliable.

How It Works
1. Screen Capture

A screenshot is taken, and only the region containing the product image is cropped using your configured coordinates.

2. Template Matching

Every template is compared to the current product image.
A simple difference score decides which template is the closest match.
Because the templates are created from real screenshots, this basic method is surprisingly accurate.

3. Decision Logic

If the difference score is low enough, the script types the matching PLU and presses Enter.

If confidence is too low, the script:

Saves the current image as an unknown

Types zero

Moves on

4. STOP Screen Detection

If the matched PLU equals "STOP", the script prints a message and ends immediately.

5. Fail-Safe Stop

Moving the mouse to the top-left corner instantly stops the script.
This prevents runaway automation, which everyone learns to appreciate eventually.

Project Structure
/project/
│
├── auto_plu.py                # Main automation script
├── get_position.py            # Tool for capturing cursor coordinates
│
└── templates/
       ├── known product images
       ├── unknown_001.png
       ├── unknown_002.png
       └── unknown_083.png     # STOP template

How To Use It

Open your emulator and load the PLU training/test screen.

Make sure the screen sits exactly where your coordinates expect it.

Run:

python auto_plu.py


You get three seconds to click the emulator window.

The script cycles through each product, recognises it, enters the PLU and moves on.

When the STOP screen is detected, the script exits cleanly.

Any unknown images appear inside the templates folder so you can label them later.

As you label more templates, the accuracy improves automatically.

How Else This Can Be Used

Although designed around PLU recognition, this entire approach is general-purpose. With minimal changes, you can adapt it for:

Automated data entry driven by on-screen images

Lightweight desktop UI test automation

Dataset generation from consistent screenshots

Simple game automation for predictable mechanics

Training simulations where each screen expects a key input

Anywhere an image appears on screen and a corresponding action must follow, this script offers a fast and simple solution.

Accuracy Tips

Make sure template images are clean, cropped correctly and consistently sized.

Do not move the emulator window mid-run.

Use a lower MATCH_THRESHOLD for stricter matching, higher for a looser tolerance.

If the script starts making mistakes, your window has probably shifted a pixel or two. It happens.

Final Notes

This project intentionally avoids heavy ML models. The strength lies in consistency: if the screenshots the script sees match the templates you provide, the system performs extremely well.

If you want to build a more advanced version using SSIM, convolutional models, or real-time OCR, that can be done too.
