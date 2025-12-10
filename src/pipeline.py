# src/pipeline.py
import os
import json
import datetime
from api_generator import APIGenerator
from content_filter import ContentFilter
from utils import load_default_prompts, save_json


class ContentPipeline:
    def __init__(self, use_api=True):
        self.generator = APIGenerator() if use_api else None
        self.filter = ContentFilter()
        self.models_loaded = False
        self.last_results = []

    # ---------------------------------------------------------
    # Load models ONCE (API generator + simple filter)
    # ---------------------------------------------------------
    def _ensure_models_loaded(self):
        if self.models_loaded:
            return

        if self.generator:
            print("[API] No local model to load (OK)")

        # ContentFilter n’a **aucun load()**
        self.models_loaded = True

    # ---------------------------------------------------------
    # Process default prompts
    # ---------------------------------------------------------
    def run(self):
        self._ensure_models_loaded()

        prompts = load_default_prompts()
        results = []

        for p in prompts:
            print(f"[PIPELINE] Processing prompt: {p}")
            generated = self.generator.generate(p)

            flagged, words = self.filter.check(generated)

            result = {
                "prompt": p,
                "generated_text": generated,
                "flagged": flagged,
                "flagged_words": words,
                "timestamp": datetime.datetime.now().isoformat()
            }

            results.append(result)

        self.last_results = results
        save_json("last_results.json", results)

        print("\n[PIPELINE] Completed!")
        print(f"[PIPELINE] {len(results)} items processed.")
        print(f"[PIPELINE] {sum(r['flagged'] for r in results)} items flagged.")

        return results

    # ---------------------------------------------------------
    # Process a single user prompt
    # ---------------------------------------------------------
    def process_single(self, prompt):
        self._ensure_models_loaded()

        generated = self.generator.generate(prompt)
        flagged, words = self.filter.check(generated)

        result = [{
            "prompt": prompt,
            "generated_text": generated,
            "flagged": flagged,
            "flagged_words": words,
            "timestamp": datetime.datetime.now().isoformat()
        }]

        self.last_results = result
        save_json("last_results.json", result)

        return result

    # ---------------------------------------------------------
    # Batch CSV processing
    # ---------------------------------------------------------
    def run_batch_csv(self, csv_path="data/prompts.csv"):
        import csv

        self._ensure_models_loaded()

        results = []

        with open(csv_path, "r", encoding="utf-8") as f:
            for row in csv.reader(f):
                prompt = row[0].strip()
                generated = self.generator.generate(prompt)

                flagged, words = self.filter.check(generated)

                results.append({
                    "prompt": prompt,
                    "generated_text": generated,
                    "flagged": flagged,
                    "flagged_words": words,
                    "timestamp": datetime.datetime.now().isoformat()
                })

        self.last_results = results
        save_json("last_results.json", results)

        return results

    # ---------------------------------------------------------
    # Return last pipeline output
    # ---------------------------------------------------------
    def get_last_results(self):
        if os.path.exists("last_results.json"):
            with open("last_results.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return None
