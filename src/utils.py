import json

def save_json(path, data):
    """Save data to JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_default_prompts():
    return [
        "Write a motivational message for students who love AI.",
        "Explain how robots can learn emotions through interaction.",
        "Describe a violent robot attack on humans."
    ]

def load_prompts_from_csv(csv_path):
    import csv
    prompts = []
    with open(csv_path, "r") as f:
        for row in csv.reader(f):
            prompts.append(row[0])
    return prompts
