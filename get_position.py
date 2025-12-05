import pyautogui
import time

pyautogui.FAILSAFE = True

print("You have 5 seconds to get ready...")
time.sleep(5)

print("Now move your mouse to the desired point and KEEP IT STILL for 5 seconds...")
time.sleep(5)

x, y = pyautogui.position()
print(f"Position: ({x}, {y})")
