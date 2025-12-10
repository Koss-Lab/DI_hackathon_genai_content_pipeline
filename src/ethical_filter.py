# ethical_filter.py
# This class will apply rule-based or model-based filtering for unsafe content.
import json

class EthicalFilter:
    def __init__(self):
        # A simple word-based detection system
        self.blocklist = [
            "hate", "kill", "violence", "terror", "racist",
            "attack", "bomb", "sex", "nsfw", "porn"
        ]

    def flag_text(self, text):
        """
        Returns True if the text contains prohibited content.
        """
        lowered = text.lower()
        for word in self.blocklist:
            if word in lowered:
                return True
        return False

    def report(self, text):
        """
        Returns a detail report as a dict.
        """
        flagged_words = [
            word for word in self.blocklist if word in text.lower()
        ]

        return {
            "is_flagged": len(flagged_words) > 0,
            "flagged_words": flagged_words
        }
