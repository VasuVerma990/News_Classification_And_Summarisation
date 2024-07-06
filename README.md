# News_Classification_And_Summarisation

## Description
This project classifies and summarizes news articles scraped from Google News and related links on the same site. It automates the extraction, classification, and summarization processes to provide structured and concise outputs for efficient content consumption.

## Feature
- Automated Extraction: Utilizes OCR technology to extract content from screenshots of news articles.
- News Classification: Automatically classifies news articles based on content.
- Text Summarization: Generates concise summaries of the classified news articles.
- Structured Output: Produces structured files that combine classified sections and summaries for easy consumption.

## Requirements
- Transformers and PyTorch Lightning: For training and using the text summarization models.
      - pip install transformers pytorch-lightning -q
- For Classifications of news
      - pip install scikit-learn numpy
- Selenium: For automated browsing and scraping news articles from Google News.
      - pip install selenium
      - apt-get update
      - apt-get install -y chromium-chromedriver
      - cp /usr/lib/chromium-browser/chromedriver /usr/bin
- Pillow: For image manipulation and processing. Pytesseract: For extracting text from images using Tesseract OCR. Tesseract OCR: The OCR engine itself, 
  required by Pytesseract.
      - pip install selenium pillow pytesseract
      - apt-get install -y tesseract-ocr
- PySpellChecker: For correcting spelling errors in the extracted text.
      - pip install pyspellchecker

## Direction of Use
- Setup on Google Colab:
    - Upload all required files to Google Colab for easy installation.
    - Ensure the requirements are available and run the following command to install dependencies:
- Running the Example:
    - Open and execute the main.ipynb notebook in Google Colab.
    - Make sure all required libraries and files are imported and installed as advised.
- Providing Google News Link:
    - Input the Google News link you want to analyze in the notebook:
      Google News Example Link
    - Ensure the link points to a valid Google News search query.
- Execution:
    - Run all cells in the notebook to initiate the scraping, classification, and summarization process.
    - At the end, a news_summarise.txt file will be generated containing the classified news and its summarized content (note: summaries may be brief due to 
      model training on concise text).
- Adjusting OCR Parameters:
    - For improved OCR accuracy, adjust parameters in scraping_news_website.py.
    - Tweaks may include starting pointer positions and total page height adjustments for complete content capture.
  
