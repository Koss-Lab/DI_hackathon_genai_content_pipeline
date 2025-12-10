# src/content_filter.py

class ContentFilter:
    def __init__(self):
        # mots interdits / sensibles
        self.blocked_words = [
            "kill",
            "attack",
            "assault",
            "terror",
            "harm"
        ]

    # ---------------------------------------------------------
    # Check content → returns (flagged: bool, list_of_words: [])
    # ---------------------------------------------------------
    def check(self, text: str):
        text_lower = text.lower()
        flagged_words = [w for w in self.blocked_words if w in text_lower]

        flagged = len(flagged_words) > 0
        return flagged, flagged_words
