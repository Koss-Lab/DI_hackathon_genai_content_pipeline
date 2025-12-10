# src/local_generator.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LocalGenerator:
    """
    Simple local text generator using a small HF model.
    Used only when USE_OPENAI_API != true in .env
    """

    def __init__(self, model_name: str = "EleutherAI/gpt-neo-125M", max_new_tokens: int = 128):
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.tokenizer = None
        self.model = None
        self.device = "cpu"

    def load(self):
        """Load the local HF model + tokenizer (only once)."""
        if self.tokenizer is not None and self.model is not None:
            return

        print(f"Loading local model: {self.model_name} ...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.model.to(self.device)
        print("Local model loaded successfully.")

    def generate(self, prompt: str) -> str:
        """Generate text from the local model."""
        if self.tokenizer is None or self.model is None:
            raise RuntimeError("LocalGenerator not loaded. Call .load() first.")

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=True,
                temperature=0.8,
                top_p=0.95,
            )

        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text
