# PLU Auto-Entry Automation

This project automates PLU training and testing by recognising the on-screen product image, matching it against a set of template screenshots, and typing the correct PLU automatically. It also saves unknown items for later labelling and can detect an end screen to stop the run. The idea is simple: stop doing repetitive PLU input manually, because life is too short for that.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Setup and Usage](#setup-and-usage)
- [Accuracy Tips](#accuracy-tips)
- [Other Use Cases](#other-use-cases)
- [Final Notes](#final-notes)

---

## Overview

The script captures a defined region of the screen, compares it to a library of template images, identifies the closest match, and automatically enters the PLU code. Unknown items are saved with incremental filenames so you can label them later. A special `STOP` image ends the script cleanly, and a fail-safe stops everything the moment your mouse touches the top-left corner.

The system is fast, simple, and surprisingly accurate when configured correctly.

---

## Features

- Automatic image capture of the product region using exact pixel coordinates.
- Template-based image recognition using a lightweight pixel-difference method.
- Automatic PLU entry using keyboard automation.
- Unknown item handling: screenshots saved for manual labelling later.
- Auto-stop behaviour when the script detects the STOP template.
- Fail-safe exit: move your mouse to the top-left corner to instantly halt the program.
- Configurable thresholds to tune matching tolerance and improve accuracy.

---

## Prerequisites

### Software

- Python 3.9+
- Windows 10 / 11
- pip installed

Install dependencies:

```bash
pip install opencv-python pyautogui numpy
