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

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

def scrape_amazon(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find(id="productTitle").get_text(strip=True) if soup.find(id="productTitle") else "Product"
    img_tag = soup.find("img", id="landingImage")
    image = ""
    if img_tag and img_tag.get("data-a-dynamic-image"):
        image = list(json.loads(img_tag["data-a-dynamic-image"]).keys())[0]
    price = soup.find("span", class_="a-price-whole").get_text(strip=True) if soup.find("span", class_="a-price-whole") else "Check Price"
    return title, image, price

def update_rss_feed(category, title, image_url):
    file_path = f"{category}.xml"
    now = datetime.datetime.now()
    rss_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
    item_link = f"https://sunraku10101-del.github.io/elite_choice/{category}.html"
    new_item = f"""    <item>
      <title>{title}</title>
      <link>{item_link}</link>
      <description>Check out this premium {category} pick!</description>
      <pubDate>{rss_date}</pubDate>
      <media:content url="{image_url}" medium="image" />
    </item>"""
    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode("utf-8")
        if "</channel>" in content:
            updated_content = content.replace("</channel>", f"{new_item}\n  </channel>")
            repo.update_file(file_path, f"Bot: Add {title} to RSS", updated_content, file.sha)
            print(f"✅ SUCCESS: {file_path} updated for Pinterest")
        else:
            print(f"⚠️ XML ERROR: Could not find </channel> in {file_path}")
    except Exception as e:
        print(f"❌ GITHUB ERROR: {e}")

def update_category_page(category, product_html):
    file_path = f"{category}.html"
    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode("utf-8")
        placeholder = ""
        if placeholder in content:
            new_content = content.replace(placeholder, product_html + "\n" + placeholder)
            repo.update_file(file_path, f"Bot: Add to {category}", new_content, file.sha)
            print(f"✅ SUCCESS: {category}.html updated")
    except Exception as e:
        print(f"❌ HTML ERROR: {e}")

def add_product(amazon_url, category):
    clean_url = amazon_url.split("?")[0]
    title, image, price = scrape_amazon(clean_url)
    product_html = f'<div class="card"><img src="{image}"><h3>{title}</h3><div class="price">₹{price}</div><a class="btn" href="{clean_url}?tag={AFFILIATE_TAG}">Buy Now</a></div>'
    
    # Run the updates
    update_category_page(category, product_html)
    
    # THE PINTEST TRIGGER
    clean_cat = category.lower().strip()
    print(f"DEBUG: Checking if '{clean_cat}' is in [fashion, beauty]...")
    if clean_cat in ["fashion", "beauty"]:
        update_rss_feed(clean_cat, title, image)
    else:
        print(f"DEBUG: Category '{clean_cat}' is not fashion or beauty. Skipping XML.")

if __name__ == "__main__":
    print("=== Elite Choice Bot ACTIVATED ===")
    while True:
        u = input("URL: ")
        if u == "exit": break
        c = input("Category: ")
        add_product(u, c)