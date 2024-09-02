import csv
import os
import random
import re
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
OUTPUT_FILE = "scraped_tweets.csv"
SCRAPE_LIMIT = 10_000

xpath = {
    "username_input": "//input[@autocomplete='username']",
    "next_button": "//button[@role='button' and @type='button' and .//span[text()='Next']]",
    "password_input": "//input[@name='password']",
    "login_button": "//button[.//span[text()='Log in']]",
    "verification_banner": "//span[text()='Enter your verification code']",
    "posts": "//article[@role='article']",
}

base_url = "https://x.com"
sign_in_url = f"{base_url}/i/flow/login"
profile_url = f"{base_url}/{USERNAME}"
likes_url = f"{profile_url}/likes"

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

wait_short = WebDriverWait(driver, 5)
wait_medium = WebDriverWait(driver, 15)
wait_long = WebDriverWait(driver, 45)


def login():
    driver.get(sign_in_url)

    username_input = wait_medium.until(
        EC.presence_of_element_located((By.XPATH, xpath["username_input"]))
    )
    username_input.send_keys(USERNAME)
    time.sleep(random.uniform(0.5, 1.5))

    button = wait_medium.until(
        EC.presence_of_element_located((By.XPATH, xpath["next_button"]))
    )
    button.click()
    time.sleep(random.uniform(0.5, 1.5))

    password_input = wait_medium.until(
        EC.presence_of_element_located((By.XPATH, xpath["password_input"]))
    )
    password_input.send_keys(PASSWORD)
    time.sleep(random.uniform(0.5, 1.5))

    button = wait_medium.until(
        EC.presence_of_element_located((By.XPATH, xpath["login_button"]))
    )
    button.click()
    time.sleep(random.uniform(0.5, 1.5))

    try:
        verification_element = wait_short.until(
            EC.presence_of_element_located((By.XPATH, xpath["verification_banner"]))
        )
        print("Verification code required, waiting for input")
        wait_long.until(
            EC.invisibility_of_element_located((By.XPATH, xpath["verification_banner"]))
        )
        print("Verification code entered")
        time.sleep(random.uniform(1.5, 3.5))
    except TimeoutException:
        print("No verification code required")


def initialize_post_ids_seen():
    """Read the existing output file and initialize the set of post IDs that have already been saved."""
    post_ids_seen = set()

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                post_ids_seen.add(row["Post ID"])
    else:
        with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Post ID",
                    "User Handle",
                    "Username",
                    "Datetime",
                    "Content",
                    "Replies",
                    "Reposts",
                    "Likes",
                    "Views",
                    "Post URL",
                ]
            )

    print(f"Initialized {len(post_ids_seen)} post IDs seen")
    return post_ids_seen


def scrape_likes():
    driver.get(likes_url)
    time.sleep(8)
    post_ids_seen = initialize_post_ids_seen()

    while len(post_ids_seen) < SCRAPE_LIMIT:
        posts = driver.find_elements(By.XPATH, xpath["posts"])
        print(f"Found {len(posts)} posts")

        with open(OUTPUT_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for post in posts:
                try:
                    post_url = post.find_element(
                        By.XPATH, ".//a[contains(@href, '/status')]"
                    ).get_attribute("href")

                    match = re.search(r"/([^/]+)/status/(\d+)", post_url)

                    if match:
                        user_handle = match.group(1)
                        post_id = match.group(2)
                    else:
                        user_handle = None
                        post_id = None
                except:
                    user_handle = None
                    post_id = None

                # Skip the post if the post_id is None or already in the file
                if not post_id or post_id in post_ids_seen:
                    continue

                try:
                    username = post.find_element(
                        By.XPATH, ".//div[@data-testid='User-Name']//span"
                    ).text
                except:
                    username = "N/A"

                try:
                    datetime_full = post.find_element(
                        By.XPATH, ".//a[contains(@href, '/status')]/time"
                    ).get_attribute("datetime")
                except:
                    datetime_full = "N/A"

                try:
                    post_content = post.find_element(
                        By.XPATH, ".//div[@data-testid='tweetText']//span"
                    ).text
                except:
                    post_content = "N/A"

                try:
                    replies = post.find_element(
                        By.XPATH,
                        ".//div[@aria-label][@role='group']//button[@data-testid='reply']//span[contains(@style, 'transform')]",
                    ).text
                except:
                    replies = "N/A"

                try:
                    reposts = post.find_element(
                        By.XPATH,
                        ".//div[@aria-label][@role='group']//button[@data-testid='retweet']//span[contains(@style, 'transform')]",
                    ).text
                except:
                    reposts = "N/A"

                try:
                    likes = post.find_element(
                        By.XPATH,
                        ".//div[@aria-label][@role='group']//button[@data-testid='unlike']//span[contains(@style, 'transform')]",
                    ).text
                except:
                    likes = "N/A"

                try:
                    views = post.find_element(
                        By.XPATH,
                        ".//div[@aria-label][@role='group']//a[contains(@href, '/analytics')]//span[contains(@style, 'transform')]",
                    ).text
                except:
                    views = "N/A"

                writer.writerow(
                    [
                        post_id,
                        user_handle,
                        username,
                        datetime_full,
                        post_content,
                        replies,
                        reposts,
                        likes,
                        views,
                        post_url,
                    ]
                )

                post_ids_seen.add(post_id)
                time.sleep(random.uniform(0.5, 3))
                print(f"Scraped {post_id}")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(4, 9))



if __name__ == "__main__":
    login()
    scrape_likes()
    driver.quit()
