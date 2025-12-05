import cv2
import numpy as np
import pyautogui
import time
import os

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05   # was 0.2 – smaller pause = faster


# ==============================
# 1) CONFIG – EDIT THESE
# ==============================

# Product image area on your screen (from get_position.py)
IMAGE_LEFT   = 1358   # top-left X
IMAGE_TOP    = 360    # top-left Y
IMAGE_RIGHT  = 1622   # bottom-right X
IMAGE_BOTTOM = 542    # bottom-right Y

# Green PLU button centre (no longer needed for Enter, but kept in case)
PLU_BUTTON_X = 1846
PLU_BUTTON_Y = 440

# How many products to process in one run
NUM_TO_HANDLE = 100    # set to 1 to test just one

# If best match score <= this, we trust it and type the PLU.
MATCH_THRESHOLD = 5.0   # stricter than before

# Folder and name pattern for unknown images
TEMPLATE_DIR = "templates"
UNKNOWN_PREFIX = "unknown_"

# Known templates -> PLU mapping
ITEMS = {
    "templates/unknown_001.png": "141",
    "templates/unknown_002.png": "8",
    "templates/unknown_003.png": "606",
    "templates/unknown_004.png": "391",
    "templates/unknown_005.png": "75",
    "templates/unknown_006.png": "36",
    "templates/unknown_007.png": "51",
    "templates/unknown_008.png": "45",
    "templates/unknown_009.png": "89",
    "templates/unknown_010.png": "64",
    "templates/unknown_011.png": "479",
    "templates/unknown_012.png": "95",
    "templates/unknown_013.png": "92",
    "templates/unknown_014.png": "68",
    "templates/unknown_015.png": "24",
    "templates/unknown_016.png": "143",
    "templates/unknown_017.png": "49",
    "templates/unknown_018.png": "10",
    "templates/unknown_019.png": "56",
    "templates/unknown_020.png": "20",
    "templates/unknown_021.png": "148",
    "templates/unknown_022.png": "81",
    "templates/unknown_023.png": "323",
    "templates/unknown_024.png": "16",
    "templates/unknown_025.png": "127",
    "templates/unknown_026.png": "426",
    "templates/unknown_027.png": "52",
    "templates/unknown_028.png": "17",
    "templates/unknown_029.png": "443",
    "templates/unknown_030.png": "48",
    "templates/unknown_031.png": "6",
    "templates/unknown_032.png": "428",
    "templates/unknown_033.png": "343",
    "templates/unknown_034.png": "366",
    "templates/unknown_035.png": "132",
    "templates/unknown_036.png": "11",
    "templates/unknown_037.png": "90",
    "templates/unknown_038.png": "451",
    "templates/unknown_039.png": "381",
    "templates/unknown_040.png": "70",
    "templates/unknown_041.png": "481",
    "templates/unknown_042.png": "170",
    "templates/unknown_043.png": "79",
    "templates/unknown_044.png": "138",
    "templates/unknown_045.png": "367",
    "templates/unknown_046.png": "363",
    "templates/unknown_047.png": "71",
    "templates/unknown_048.png": "30",
    "templates/unknown_049.png": "33",
    "templates/unknown_050.png": "320",
    "templates/unknown_051.png": "58",
    "templates/unknown_052.png": "365",
    "templates/unknown_053.png": "456",
    "templates/unknown_054.png": "515",
    "templates/unknown_055.png": "38",
    "templates/unknown_056.png": "86",
    "templates/unknown_057.png": "300",
    "templates/unknown_058.png": "420",
    "templates/unknown_059.png": "44",
    "templates/unknown_060.png": "50",
    "templates/unknown_061.png": "395",
    "templates/unknown_062.png": "118",
    "templates/unknown_063.png": "317",
    "templates/unknown_064.png": "83",
    "templates/unknown_065.png": "438",
    "templates/unknown_066.png": "43",
    "templates/unknown_067.png": "55",
    "templates/unknown_068.png": "608",
    "templates/unknown_069.png": "607",
    "templates/unknown_070.png": "244",
    "templates/unknown_071.png": "82",
    "templates/unknown_072.png": "125",
    "templates/unknown_073.png": "159",
    "templates/unknown_074.png": "405",
    "templates/unknown_075.png": "335",
    "templates/unknown_076.png": "54",
    "templates/unknown_077.png": "389",
    "templates/unknown_078.png": "40",
    "templates/unknown_079.png": "470",
    "templates/unknown_080.png": "706",
    "templates/unknown_081.png": "98",
    "templates/unknown_082.png": "442",
    "templates/unknown_083.png": "STOP",   # sentinel / ending screen
}


# ==============================
# 2) IMAGE + TEMPLATE HELPERS
# ==============================

def capture_product_roi():
    """Screenshot the whole screen and crop the product image area."""
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    roi = img[IMAGE_TOP:IMAGE_BOTTOM, IMAGE_LEFT:IMAGE_RIGHT]
    return roi


def debug_save_current_product():
    """One-off helper to check that IMAGE_* coords are correct."""
    print("You have 3 seconds to focus the PLU window...")
    time.sleep(3)
    roi = capture_product_roi()
    cv2.imwrite("debug_current_product.png", roi)
    print("Saved current product area to debug_current_product.png")


def load_templates():
    """Load all known template images."""
    templates = []
    for path, plu in ITEMS.items():
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            print(f"Warning: could not load template {path}")
            continue
        templates.append((path, img, plu))
    return templates


def score_difference(img1, img2):
    """Simple pixel difference score (lower is better)."""
    h, w = img1.shape[:2]
    img2_resized = cv2.resize(img2, (w, h))
    diff = cv2.absdiff(img1, img2_resized)
    mse = diff.mean()
    return mse


def best_match_for_roi(roi, templates):
    """Return (best_plu, best_score, best_path) for this ROI."""
    if not templates:
        # No templates at all: nothing to match against
        return None, float("inf"), None

    best_plu = None
    best_score = float("inf")
    best_path = None

    for path, tmpl_img, plu in templates:
        score = score_difference(roi, tmpl_img)
        print(f"{path} score: {score:.2f}")
        if score < best_score:
            best_score = score
            best_plu = plu
            best_path = path

    print(f"Best match: {best_path} with score {best_score:.2f}, PLU {best_plu}")
    return best_plu, best_score, best_path


def next_unknown_filename():
    """Return the next unknown_###.png filename in templates/."""
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    existing = [
        f for f in os.listdir(TEMPLATE_DIR)
        if f.startswith(UNKNOWN_PREFIX) and f.endswith(".png")
    ]

    max_idx = 0
    for name in existing:
        try:
            num_part = name[len(UNKNOWN_PREFIX):-4]
            idx = int(num_part)
            if idx > max_idx:
                max_idx = idx
        except ValueError:
            continue

    return os.path.join(TEMPLATE_DIR, f"{UNKNOWN_PREFIX}{max_idx + 1:03d}.png")


# ==============================
# 3) TYPING / SUBMITTING
# ==============================

def type_plu_and_submit(plu):
    """Type a PLU and press Enter (faster than clicking the PLU button)."""
    print(f"Typing PLU: {plu}")
    pyautogui.write(plu, interval=0.02)  # faster typing
    pyautogui.press("enter")             # use Enter instead of clicking button


def type_zero_and_submit():
    """Fallback for unknown: type 0 and press Enter."""
    print("Unknown item – typing 0 instead.")
    pyautogui.write("0", interval=0.02)
    pyautogui.press("enter")


# ==============================
# 4) MAIN FLOW (RECOGNISE OR COLLECT UNKNOWN)
# ==============================

def main():
    # If you ever need to re-check cropping, uncomment:
    # debug_save_current_product()
    # return

    print(f"Will handle up to {NUM_TO_HANDLE} products.")
    print("You have 3 seconds to bring the PLU window to the front...")
    time.sleep(3)

    templates = load_templates()
    if not templates:
        print("No known templates loaded – will treat EVERYTHING as unknown and just collect images.")

    for i in range(NUM_TO_HANDLE):
        print(f"\n===== Product {i + 1} of {NUM_TO_HANDLE} =====")
        try:
            roi = capture_product_roi()
            best_plu, best_score, best_path = best_match_for_roi(roi, templates)

            # If we hit the ending screen template, stop completely
            if best_plu == "STOP" and best_score <= MATCH_THRESHOLD:
                print(f"Detected STOP screen (score {best_score:.2f}). Stopping script.")
                break

            # Case 1: we have templates and found a confident match
            if templates and best_plu is not None and best_score <= MATCH_THRESHOLD:
                print(f"Recognised as PLU {best_plu} (score {best_score:.2f}).")
                type_plu_and_submit(best_plu)

            else:
                # Case 2: either no templates at all OR not confident enough → save and use 0
                filename = next_unknown_filename()
                cv2.imwrite(filename, roi)
                print(f"Saved as unknown template: {filename} (score {best_score:.2f}).")
                type_zero_and_submit()

            # Wait for the next product to load – speeded up
            time.sleep(1.3)

        except pyautogui.FailSafeException:
            print(f"\nFail-safe triggered (mouse hit top-left) at item {i + 1}. Stopping early.")
            break
        except Exception as e:
            print(f"\nError on item {i + 1}: {e}. Stopping early.")
            break

    print("\nDone – processed all requested products.")


if __name__ == "__main__":
    main()
