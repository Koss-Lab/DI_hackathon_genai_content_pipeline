# src/api_generator.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI


class APIGenerator:
    """
    Universal OpenAI API wrapper
    Compatible with openai >= 1.0 (2025 standard)
    Works for CLI, Telegram bot, Railway deployment.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL_NAME", "gpt-4o-mini")

        if not self.api_key:
            raise ValueError("ERROR: OPENAI_API_KEY not found in environment")

        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        """Generate text using OpenAI Chat Completions API."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"[API ERROR]\n{e}"
