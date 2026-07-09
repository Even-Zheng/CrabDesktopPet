import os
import sys

# Get the directory where the script/EXE is located
if getattr(sys, 'frozen', False):
    # Running as compiled EXE
    BASE_DIR = os.path.join(os.path.dirname(sys.executable), "assets")
else:
    # Running in development
    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

GIF_PATHS = {
    "await": {
        f"await_{i}": os.path.join(BASE_DIR, "await", f"await_{i}.gif")
        for i in range(1, 6)
    },
    "walk": os.path.join(BASE_DIR, "walk", "Walk.gif"),
    "run": os.path.join(BASE_DIR, "run", "Run.gif"),
    "click": {
        "click_1": os.path.join(BASE_DIR, "click", "click_1.gif"),
        "click_2": os.path.join(BASE_DIR, "click", "click_2.gif"),
    },
    "catch": os.path.join(BASE_DIR, "catch", "catch.gif"),
    "drop":  os.path.join(BASE_DIR, "drop", "drop.gif"),
    "bye":   os.path.join(BASE_DIR, "bye", "bye.gif"),
}

WINDOW = {
    "frameless": True,
    "stay_on_top": True,
    "no_taskbar": True,
    "transparent": True,
}

MOVE = {
    "walk_speed": 3,
    "run_speed": 8,
    "drop_speed": 5,
}

TIMING = {
    "idle_threshold": 10000,
    "await_duration": 10000,
    "click_duration": 8000,
    "bye_duration": 6000,
    "check_interval": 50,
}

PROB = {
    "await_chance": 0.5,
    "walk_chance": 0.5,
}

DRAG_THRESHOLD = 10
EDGE_MARGIN = 10