import csv
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

pages = [
    "abx-heart-monitor",
    "baby-cries",
    "baby-shower",
    "baby-of-the-year",
    "babysitter-hit-and-run",
    "banana-breath",
    "barley-tonight",
    "big-wave",
    "blues-brother",
    "bozo-dubbed-part-1",
    "bozo-dubbed-part-2",
    "calicocutpantscom",
    "carber-hot-dog-vac",
    "choking",
    "claires",
    "coffin-flop",
    "credit-card-roulette",
    "dan-flashes",
    "dan-vegas-mega-money-quiz",
    "darmine-doggy-door",
    "daves-huge-dumps",
    "detective-crashmore-press-junket",
    "detective-crashmore-trailer",
    "diner-wink",
    "dog-hair",
    "drivers-ed",
    "fake-water",
    "feed-eggs",
    "fentons-horse-ranch",
    "focus-group",
    "friend-group",
    "fully-loaded-nachos",
    "funeral-organ",
    "game-night",
    "garfield-house",
    "gelutol",
    "ghost-tour",
    "ghosts-of-christmas-way-future",
    "gift-receipt",
    "has-this-ever-happened-to-you",
    "herbie-hancock",
    "honk-if-youre-horny",
    "insider-trading",
    "instagram",
    "insult-comic-restaurant",
    "king-of-the-dirty-songs",
    "laser-spine-specialists",
    "little-buff-boys-commercial",
    "little-buff-boys-competition",
    "magicians-suck",
    "metal-motto-search",
    "motorcycles",
    "new-office-printer",
    "pacific-proposal-park",
    "parked-on-the-sidewalk",
    "parking-lot",
    "pay-it-forward",
    "photo-booth",
    "prank-show",
    "professor-dinner",
    "pulling-the-door-open",
    "randall-is-interesting",
    "rat-mom",
    "river-mountain-high-part-1",
    "river-mountain-high-part-2",
    "scott-loves-his-wife",
    "shirt-brothers",
    "shops-at-the-creek",
    "silent-theater",
    "stable-of-stars",
    "street-sets",
    "studio-audience",
    "summer-loving",
    "summer-loving-farewell",
    "supermarket-swap-vr-edition",
    "talking-about-my-kids",
    "tammy-craps",
    "tasty-time-vids",
    "the-bones-are-their-money",
    "the-capital-room",
    "the-driving-crooner",
    "the-man",
    "whoopee-cushion",
    "wienermobile",
    "wilsons-toupees",
    "you-cant-skip-lunch",
]

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

results = []

for page in pages:
    url = f"https://ithinkyoushouldquote.me/sketch/{page}/"
    driver.get(url)
    time.sleep(random.uniform(1.5, 3.5))

    links = driver.find_elements(By.XPATH, "//a[contains(@href, '/meme/?id=')]")

    for link in links:
        href = link.get_attribute("href")
        results.append([page, href])
        print(page, href)

with open("sketch_links.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Page", "Link"])
    writer.writerows(results)

driver.quit()

print("Scraping complete. Results saved to sketch_links.csv.")
