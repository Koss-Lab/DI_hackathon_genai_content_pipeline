# scheduler.py

import os
import sys
from dotenv import load_dotenv
import schedule
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from src.pipeline import ContentPipeline
from src.utils import save_json


load_dotenv(os.path.join(ROOT, ".env"))


def run_scheduled_job():
    print("[SCHEDULER] Running scheduled pipeline...")
    pipeline = ContentPipeline()
    results = pipeline.run()
    save_json(results)
    print("[SCHEDULER] Completed.")


def scheduler_loop():
    schedule.every(1).hours.do(run_scheduled_job)

    print("⏳ Scheduler active. Running every 1 hour...")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    scheduler_loop()
