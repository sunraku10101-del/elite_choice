import requests
from bs4 import BeautifulSoup
from github import Github
import os
import json
import datetime
import re

# ==================== CONFIG ====================
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
GITHUB_REPO = "sunraku10101-del/elite_choice"
AFFILIATE_TAG = "elitechoic002-21"

PLACEHOLDER_IMAGE = "https://via.placeholder.com/300x300?text=Elite+Choice"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

# ==================== AMAZON SCRAPER ====================
def scrape_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-IN,en;q=0.9"
    }

    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    # TITLE
    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else "Amazon Product"

    # IMAGE
    image = PLACEHOLDER_IMAGE
    img_tag = soup.find("img", id="landingImage")
    if img_tag and img_tag.get("data-a-dynamic-image"):
        try:
            image = list(json.loads(img_tag["data-a-dynamic-image"]).keys())[0]
        except:
            pass

    # PRICE
    price_tag = soup.select_one(".a-price-whole")
    price = price_tag.get_text(strip=True) if price_tag else "Check Price"
    price = re.sub(r"[^\d]", "", price)

    return title, image, price

# ==================== SAFE JS UPDATE ====================
def update_products_js(category, product):
    file_path = "products.js" if category == "beauty" else "fashion-products.js"

    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode("utf-8")

        if product["link"] in content:
            print("⚠️ Product already exists. Skipping.")
            return

        insert_index = content.find("[")
        if insert_index == -1:
            print("❌ Invalid JS structure")
            return

        product_block = json.dumps(product, indent=2)

        updated = (
            content[:insert_index + 1]
            + "\n"
            + product_block
            + ","
            + content[insert_index + 1:]
        )

        repo.update_file(
            file_path,
            f"Bot: Add product to {category}",
            updated,
            file.sha
        )

        print(f"✅ Product added to {file_path}")

    except Exception as e:
        print(f"❌ JS UPDATE ERROR: {e}")

# ==================== RSS UPDATE ====================
def update_rss_feed(category, title, image_url):
    file_path = f"{category}.xml"
    now = datetime.datetime.utcnow()
    rss_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
    page_link = f"https://sunraku10101-del.github.io/elite_choice/{category}.html"

    new_item = f"""
    <item>
      <title>{title}</title>
      <link>{page_link}</link>
      <description>Premium {category} pick from Elite Choice</description>
      <pubDate>{rss_date}</pubDate>
      <media:content url="{image_url}" medium="image" />
    </item>
"""

    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode("utf-8")

        if "</channel>" not in content:
            return

        updated = content.replace("</channel>", new_item + "\n</channel>", 1)

        repo.update_file(
            file_path,
            f"Bot: RSS update ({category})",
            updated,
            file.sha
        )

        print("✅ RSS updated")

    except:
        pass

# ==================== MAIN LOGIC ====================
def add_product(amazon_url, category):
    clean_url = amazon_url.split("?")[0]

    title, image, price = scrape_amazon(clean_url)

    product_data = {
        "img": image,
        "title": title,
        "price": f"₹{price}",
        "link": f"{clean_url}?tag={AFFILIATE_TAG}"
    }

    update_products_js(category, product_data)

    if category in ["beauty", "fashion"]:
        update_rss_feed(category, title, image)

# ==================== RUN ====================
if __name__ == "__main__":
    print("=== Elite Choice SAFE BOT ACTIVE ===")

    while True:
        url = input("Amazon URL (or exit): ").strip()
        if url.lower() == "exit":
            break

        category = input("Category (beauty/fashion): ").strip().lower()
        if category not in ["beauty", "fashion"]:
            print("❌ Invalid category")
            continue

        add_product(url, category)
