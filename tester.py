import requests
from bs4 import BeautifulSoup
from github import Github
import os
import json
import datetime

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
    image = ""
    img_tag = soup.find("img", id="landingImage")
    if img_tag and img_tag.get("data-a-dynamic-image"):
        try:
            image = list(json.loads(img_tag["data-a-dynamic-image"]).keys())[0]
        except:
            image = ""

    if not image:
        image = PLACEHOLDER_IMAGE

    # PRICE
    price_tag = soup.select_one(".a-price-whole")
    price = price_tag.get_text(strip=True) if price_tag else "Check Price"
    price = price.replace("₹", "").strip()

    return title, image, price

# ==================== RSS UPDATE (PINTEREST) ====================
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
            print("❌ RSS ERROR: </channel> missing")
            return

        updated = content.replace("</channel>", new_item + "\n</channel>", 1)

        repo.update_file(
            file_path,
            f"Bot: Add {title} to RSS",
            updated,
            file.sha
        )

        print(f"✅ RSS UPDATED: {file_path}")

    except Exception as e:
        print(f"❌ RSS ERROR: {e}")

# ==================== HTML UPDATE (BULLETPROOF) ====================
def update_category_page(category, product_html):
    file_path = f"{category}.html"
    anchor = "<!-- BOT_INSERT -->"

    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode("utf-8")

        # SAFETY CHECKS
        if "<!DOCTYPE html>" not in content:
            print("❌ HTML corrupted. Aborting update.")
            return

        if anchor not in content:
            print("❌ BOT_INSERT not found. Aborting.")
            return

        if product_html in content:
            print("⚠️ Product already exists. Skipping.")
            return

        new_content = content.replace(anchor, f"\n{product_html}\n{anchor}", 1)

        repo.update_file(
            file_path,
            f"Bot: Add product to {category}",
            new_content,
            file.sha
        )

        print(f"✅ HTML UPDATED: {file_path}")

    except Exception as e:
        print(f"❌ HTML ERROR: {e}")

# ==================== MAIN LOGIC ====================
def add_product(amazon_url, category):
    clean_url = amazon_url.split("?")[0]

    title, image, price = scrape_amazon(clean_url)

    product_html = f"""
<div class="card">
    <img src="{image}" alt="{title}" loading="lazy">
    <h3>{title}</h3>
    <div class="price">₹{price}</div>
    <a class="btn" href="{clean_url}?tag={AFFILIATE_TAG}" target="_blank" rel="nofollow noopener">
        🛒 Buy on Amazon
    </a>
    <div class="trust">✔ Verified Amazon Seller</div>
</div>
""".strip()

    update_category_page(category, product_html)

    if category.lower().strip() in ["fashion", "beauty"]:
        update_rss_feed(category.lower().strip(), title, image)

# ==================== RUN ====================
if __name__ == "__main__":
    print("=== Elite Choice Bot ACTIVATED (FINAL STABLE BUILD) ===")
    while True:
        url = input("Amazon URL (or exit): ").strip()
        if url.lower() == "exit":
            break

        cat = input("Category (beauty/fashion): ").strip().lower()
        add_product(url, cat)
