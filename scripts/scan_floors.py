import time
from src.models.floor_detector import FloorDetector

sleep_minutes = 10
floordetector = FloorDetector()

while True:
    try:
        floordetector.check_floor_prices()
        print(f"Sleeping {sleep_minutes} minutes")
    except Exception as E:
        print(f"Exception: {E}")
    time.sleep(60 * sleep_minutes)
