import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import pandas as pd

class NewsSummarizer:
    def __init__(self, model_checkpoint_path, model_name='t5-base'):
        self.model_name = model_name
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        
        # Load the entire checkpoint
        checkpoint = torch.load(model_checkpoint_path, map_location=torch.device('cpu'))
        
        # Extract the state dictionary from the checkpoint
        state_dict = checkpoint['state_dict']
        
        # Create a new T5 model and load the state dictionary
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.model.load_state_dict({k.replace('model.', ''): v for k, v in state_dict.items() if k.startswith('model.')})
        self.model.eval()  # Set the model to evaluation mode

    def summarize(self, text, input_max_length=512, summary_max_length=150):
        # Tokenize the input text
        text_encoding = self.tokenizer(
            text,
            max_length=input_max_length,
            truncation=True,
            padding='max_length',
            add_special_tokens=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        text_encoding = {key: val.to('cpu') for key, val in text_encoding.items()}

        # Generate the summary
        generated_ids = self.model.generate(
            input_ids=text_encoding['input_ids'],
            attention_mask=text_encoding['attention_mask'],
            max_length=summary_max_length,
            num_beams=8,
            repetition_penalty=2.5,
            length_penalty=2,
            early_stopping=True
        )
        preds = [
            self.tokenizer.decode(generated_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        ]
        return " ".join(preds)

    def summarize_dataframe(self, df, text_column, summary_column, input_max_length=512, summary_max_length=150):
        summaries = []
        i = 1;
        for text in df[text_column]:
            print("Summarising Text:"," ",i)
            summary = self.summarize(text, input_max_length, summary_max_length)
            summaries.append(summary)
            i = i + 1
        df[summary_column] = summaries
        return df
