import requests
from bs4 import BeautifulSoup
from github import Github
import os
import json
import datetime

# ==================== CONFIG ====================
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found! Set GITHUB_TOKEN environment variable.")

GITHUB_REPO = "sunraku10101-del/elite_choice"
AFFILIATE_TAG = "elitechoic002-21"

# Connect to GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

# ==================== FUNCTIONS ====================

def scrape_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else "Amazon Product"

    image_url = ""
    image_tag = soup.find("img", id="landingImage")
    if image_tag and image_tag.get("data-a-dynamic-image"):
        images = json.loads(image_tag["data-a-dynamic-image"])
        image_url = list(images.keys())[0]
    elif image_tag and image_tag.get("src"):
        image_url = image_tag["src"]

    price_tag = soup.find("span", class_="a-price-whole")
    price = price_tag.get_text(strip=True) if price_tag else "Check price"

    return title, image_url, price

def update_rss_feed(category, title, image_url):
    """Adds product to XML for Pinterest"""
    file_path = f"{category}.xml"
    now = datetime.datetime.now()
    rss_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
    item_link = f"https://sunraku10101-del.github.io/elite_choice/{category}.html"
    
    new_item = f"""    <item>
      <title>{title}</title>
      <link>{item_link}</link>
      <description>Check out this premium {category} pick from Elite Choice Kerala!</description>
      <pubDate>{rss_date}</pubDate>
      <media:content url="{image_url}" medium="image" />
    </item>"""

    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode("utf-8")
        if "</channel>" in content:
            updated_content = content.replace("</channel>", f"{new_item}\n  </channel>")
            repo.update_file(file_path, f"Bot: Add {title} to {category}.xml", updated_content, file.sha)
            print(f"✅ Updated {file_path} for Pinterest")
    except Exception as e:
        print(f"⚠️ Could not update {file_path}: {e}")

def update_category_page(category, product_html):
    """Adds product to HTML website"""
    file_path = f"{category}.html"
    try:
        file = repo.get_contents(file_path)
        old_content = file.decoded_content.decode("utf-8")
      # CORRECTED: The marker is now ACTUALLY filled in!
      placeholder = "<!-- PRODUCTS HERE -->"
        if placeholder in old_content:
            new_content = old_content.replace(placeholder, product_html + "\n" + placeholder)
            repo.update_file(file_path, f"Bot: Add product to {category}", new_content, file.sha)
            print(f"✅ Updated {category}.html on GitHub")
        else:
            print(f"⚠️ Error: Could not find '{placeholder}' in {category}.html")
    except Exception as e:
        print(f"❌ Error updating {category}.html: {e}")

def add_product(amazon_url, category):
    if "?" in amazon_url:
        clean_url = amazon_url.split("?")[0]
    else:
        clean_url = amazon_url

    title, image, price = scrape_amazon(clean_url)
    
    product_html = f"""
        <div class="card">
            <img src="{image}" alt="{title}">
            <h3>{title}</h3>
            <div class="price">₹{price}</div>
            <a class="btn" href="{clean_url}?tag={AFFILIATE_TAG}" target="_blank">Buy Now</a>
        </div>
    """
    # This runs the Website update
    update_category_page(category, product_html)
    
    # This runs the Pinterest update
    if category in ["fashion", "beauty"]:
        update_rss_feed(category, title, image)

# ===================== RUN BOT =====================
if __name__ == "__main__":
    print("=== Elite Choice Automation Bot ===")
    while True:
        url = input("Enter Amazon URL (or 'exit'): ").strip()
        if url.lower() == "exit": break
        category = input("Enter category (fashion/beauty): ").strip().lower()
        add_product(url, category)

