from io import BytesIO
import os
import random
import time

import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

csv_file = "sketch_links.csv"
df = pd.read_csv(csv_file)

df = df.sample(frac=1).reset_index(drop=True)

for index, row in df.iterrows():
    page_name = row["Page"]
    link = row["Link"]
    uuid_str = link.split("?id=")[-1]
    file_name = f"images/{uuid_str}.jpg"

    if os.path.exists(file_name):
        print(f"Skipping {file_name}")
        continue

    driver.get(link)

    tries = 0
    while tries < 3 and not os.path.exists(file_name):
        tries += 1
        try:
            time.sleep(random.uniform(3, 27.5))
            meme_div = driver.find_element(By.ID, "memeimg")
            screenshot = meme_div.screenshot_as_png
            image = Image.open(BytesIO(screenshot))
            image.save(file_name, "JPEG")
            print(f"Saved {file_name}")
        except Exception as e:
            print(f"Error processing {link}: {e}")
            time.sleep(random.uniform(1.5, 3.5))

    if tries == 3:
        print(f"Failed to process {link}")

driver.quit()
