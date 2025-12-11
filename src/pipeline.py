# src/pipeline.py
import json
import datetime
import pandas as pd

from .api_generator import APIGenerator

# Railway can't install transformers -> disable Summarizer cleanly
try:
    from .summarizer import Summarizer
except Exception:
    Summarizer = None

from .ethical_filter import EthicalFilter
from .content_filter import ContentFilter
from .utils import save_json, load_default_prompts


class ContentPipeline:
    def __init__(self, use_api=True):
        self.generator = APIGenerator() if use_api else None
        self.filter = ContentFilter()
        self.models_loaded = False
        self.last_results = []

        # Summarizer disabled on Railway
        self.summarizer = Summarizer() if Summarizer else None

    # ---------------------------------------------
    # Save last results to file + memory
    # ---------------------------------------------
    def save_last_results(self, results):
        try:
            with open("last_results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            self.last_results = results
        except Exception as e:
            print("[PIPELINE] ERROR saving last results:", e)

    # ---------------------------------------------------------
    # Load models once
    # ---------------------------------------------------------
    def _ensure_models_loaded(self):
        if self.models_loaded:
            return

        if self.generator:
            print("[API] No local model to load (OK)")

        self.models_loaded = True

    # ---------------------------------------------------------
    # Run default prompts
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
    # Process a single prompt
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
        try:
            df = pd.read_csv(csv_path)

            if "prompt" not in df.columns:
                raise ValueError("CSV must contain a 'prompt' column")

            prompts = df["prompt"].dropna().tolist()

            results = []
            for prompt in prompts:
                results.extend(self.process_single(prompt))

            self.save_last_results(results)
            return results

        except Exception as e:
            return [{
                "prompt": "CSV_ERROR",
                "generated_text": str(e),
                "flagged": False
            }]

    # ---------------------------------------------------------
    # Load last results from JSON
    # ---------------------------------------------------------
    def get_last_results(self, limit=None):
        try:
            with open("last_results.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            if limit is not None:
                return data[-limit:]

            return data

        except FileNotFoundError:
            return []
