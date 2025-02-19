# -*- coding: utf-8 -*-
"""Classifying_News.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_kVB3rRwjAHZvw6WV1kwkewRoTkJeWs_
"""

import pandas as pd
from joblib import load

class ModelPredictor:
    def __init__(self, model_path):
        self.model = load(model_path)

    def predict_and_add_column(self, df, input_column, output_column):

        if input_column not in df.columns:
            raise ValueError(f"Column '{input_column}' does not exist in the DataFrame.")


        predictions = self.model.predict(df[input_column])


        df[output_column] = predictions
        return df

    def save_dataframe(self, df, output_path):
        df.to_csv(output_path, index=False)

