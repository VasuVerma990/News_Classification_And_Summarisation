import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageEnhance
import pytesseract
import io

class NewsTextExtractor:
    def __init__(self, csv_file, output_file, url_column, total_height=3000, scroll_pause_time=4, scroll_increment=500):
        self.csv_file = csv_file
        self.output_file = output_file
        self.url_column = url_column
        self.total_height = total_height
        self.scroll_pause_time = scroll_pause_time
        self.scroll_increment = scroll_increment

        # Read the CSV file and check for the required column
        self.df = pd.read_csv(csv_file)

        if self.url_column not in self.df.columns:
            raise ValueError(f"Column '{self.url_column}' not found in the CSV file.")

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920x1080')

        self.driver = webdriver.Chrome(options=chrome_options)

    def crop_right_half(self, image):
        width, height = image.size
        left = 0
        upper = 0
        right = width*0.65
        lower = height
        left_half = image.crop((left, upper, right, lower))
        return left_half

    def preprocess_image(self, image):
        # Crop the right half of the image
        image = self.crop_right_half(image)
        # Enhance image quality (example: adjust contrast)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)  # Adjust contrast factor as needed
        return image

    def scroll_and_capture(self, driver):
        extracted_texts = []
        current_position = 0
        while current_position < self.total_height:
            driver.execute_script(f"window.scrollBy(0, {self.scroll_increment});")
            time.sleep(self.scroll_pause_time)
            current_position += self.scroll_increment

            screenshot = driver.get_screenshot_as_png()
            screenshot_image = Image.open(io.BytesIO(screenshot))
            screenshot_image = self.preprocess_image(screenshot_image)
            
            text = pytesseract.image_to_string(screenshot_image, lang='eng', config='--oem 3 --psm 3')
            extracted_texts.append(text)

            new_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
            if new_position > self.total_height:
                break

        return "\n".join(extracted_texts)

    def extract_texts(self):
        extracted_texts = []
        for index, row in self.df.iterrows():
            url = row[self.url_column]
            print(f"Processing {index + 1}/{len(self.df)}: {url}")
            try:
                self.driver.get(url)
                time.sleep(5)
                text = self.scroll_and_capture(self.driver)
                extracted_texts.append(text)
            except Exception as e:
                print(f"Failed to process {url}: {e}")
                extracted_texts.append("")

        self.df['Data'] = extracted_texts
        self.df.to_csv(self.output_file, index=False)

    def close_driver(self):
        self.driver.quit()
