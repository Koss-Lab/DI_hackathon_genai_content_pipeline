# summarizer.py
# This class will summarize generated text and compare with the prompt.

from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

class Summarizer:

    def __init__(self, model_name="t5-small"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

    def load(self):
        print(f"Loading summarization model: {self.model_name} ...")
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        print("Summarizer loaded successfully.")

    def summarize(self, text):
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Summarizer not loaded. Call .load() first.")

        # T5 expects a "summarize:" prefix
        input_text = "summarize: " + text

        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            padding=True,
            truncation=True
        )

        summary_ids = self.model.generate(
            inputs.input_ids,
            max_length=60,
            min_length=10,
            length_penalty=1.0,
            num_beams=4,
            early_stopping=True
        )

        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
