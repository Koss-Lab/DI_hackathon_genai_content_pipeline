# generator.py
# This class handles text generation using a small transformer model.

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class TextGenerator:
    def __init__(self, model_name="EleutherAI/gpt-neo-125M"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

    def load(self):
        print(f"Loading model: {self.model_name} ...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        print("Model loaded successfully.")

    def generate(self, prompt, max_length=150, temperature=0.7):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            do_sample=True,
            temperature=temperature,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
