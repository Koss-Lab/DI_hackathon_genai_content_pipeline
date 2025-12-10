# src/api_generator.py

import os
from openai import OpenAI

class APIGenerator:
    def __init__(self):
        # Load env vars
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")  # FIXED

        if not self.api_key:
            raise ValueError("ERROR: OPENAI_API_KEY not found in .env")

        # Init OpenAI client (NEW SDK)
        self.client = OpenAI(api_key=self.api_key)

    def load(self):
        """API generator doesn't need loading, but pipeline expects this method."""
        print("[API] No local model to load (OK)")

    def generate(self, prompt: str) -> str:
        print(f"[API] Generating with model: {self.model_name}")

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.9
        )

        return response.choices[0].message.content
