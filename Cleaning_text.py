import re
import pandas as pd
from spellchecker import SpellChecker

class TextCleaner:
    def __init__(self):
        self.spell = SpellChecker()

    def clean_text(self, text):
        # Replace non-letter and non-number characters with spaces
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        # Normalize spaces by replacing multiple spaces with a single space
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        # Check and correct spelling
        words = cleaned_text.split()
        corrected_words = [self.spell.correction(word) if self.spell.correction(word) else word for word in words]
        corrected_text = ' '.join(corrected_words)

        return corrected_text

    def clean_dataframe(self, df, text_column):
        # Apply the clean_text function to each element in the specified text column
        df[text_column] = df[text_column].apply(self.clean_text)
        return df
