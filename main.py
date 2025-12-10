# main.py
# Entry point for the AI content generation pipeline

import os
import pathlib
from dotenv import load_dotenv

# Force the absolute path to .env
env_path = pathlib.Path(__file__).parent / ".env"
print("Loading .env from:", env_path)

load_dotenv(dotenv_path=env_path)

print("ENV loaded? Key exists:", os.getenv("OPENAI_API_KEY") is not None)


load_dotenv()  # Load .env variables before anything else

from src.pipeline import ContentPipeline


def main():
    print("[MAIN] Starting pipeline...\n")

    pipeline = ContentPipeline()

    pipeline.run()

    print("\n[MAIN] Pipeline finished.")


if __name__ == "__main__":
    main()
