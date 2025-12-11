# src/api_generator.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()

class APIGenerator:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("ERROR: OPENAI_API_KEY not found in environment variables")

        # configure old OpenAI client
        openai.api_key = self.api_key

    def generate(self, prompt: str) -> str:
        """Generate text using the old OpenAI SDK (0.28.1)."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )

            return response["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"[API ERROR] {e}")
            return f"[API ERROR] {str(e)}"
