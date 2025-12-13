import requests
from bs4 import BeautifulSoup
from github import Github
import os

# ==================== CONFIG ====================

# Get GitHub token from environment variable and strip whitespace/newlines
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found! Set GITHUB_TOKEN environment variable.")

# Your GitHub repo
GITHUB_REPO = "sunraku10101-del/elite_choice"

# Your affiliate tag
AFFILIATE_TAG = "elitechoic002-21"

# Local temp folder to save HTML files before pushing
LOCAL_FOLDER = "temp_pages"

# ================================================

# Create temp folder if not exists
if not os.path.exists(LOCAL_FOLDER):
    os.makedirs(LOCAL_FOLDER)

# Connect to GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

import json

def scrape_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Product title
    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else "Amazon Product"

    # Product image (Amazon uses dynamic JSON)
    image_url = ""
    image_tag = soup.find("img", id="landingImage")

    if image_tag and image_tag.get("data-a-dynamic-image"):
        images = json.loads(image_tag["data-a-dynamic-image"])
        image_url = list(images.keys())[0]
    elif image_tag and image_tag.get("src"):
        image_url = image_tag["src"]

    # Product price
    price_tag = soup.find("span", class_="a-price-whole")
    price = price_tag.get_text(strip=True) if price_tag else "Check price"

    return title, image_url, price

html = generate_product_html(title, image, price, amazon_url, category)

    affiliate_url = product_url
    if "tag=" not in affiliate_url:
        if "?" in affiliate_url:
            affiliate_url += f"&tag={AFFILIATE_TAG}"
        else:
            affiliate_url += f"?tag={AFFILIATE_TAG}"

    # Beauty layout
    if category == "beauty":
        html = f"""
        <div class="card">
            <img src="{image_url}" alt="{title}">
            <h3>{title}</h3>
            <div class="price">₹{price}</div>
            <a class="btn" href="{affiliate_url}" target="_blank">Buy Now</a>
        </div>
        """

    # Fashion layout
    elif category == "fashion":
        html = f"""
        <div class="product">
            <img src="{image_url}" alt="{title}">
            <h3>{title}</h3>
            <p>Trending fashion pick</p>
            <div class="product-price">₹{price}</div>
            <a href="{affiliate_url}" target="_blank" class="buy-btn">Buy Now</a>
        </div>
        """

    else:
        html = f"<p>Unsupported category</p>"

    return html



def update_category_page(category, product_html):
    """Update the category HTML page in the repo"""
    file_path = f"{category}.html"

    try:
        file = repo.get_contents(file_path)
        old_content = file.decoded_content.decode("utf-8")
        new_content = old_content.replace("<!-- PRODUCTS HERE -->",
                                          product_html + "\n<!-- PRODUCTS HERE -->")
        repo.update_file(file_path, f"Add new product to {category}", new_content, file.sha)
        print(f"✅ Updated {category}.html on GitHub")
    except Exception as e:
        # If file does not exist, create new
        new_content = f"""
        <html>
        <head><title>{category.title()}</title></head>
        <body>
        <h1>{category.title()}</h1>
        <!-- PRODUCTS HERE -->
        {product_html}
        </body>
        </html>
        """
        repo.create_file(file_path, f"Create {category}.html with first product", new_content)
        print(f"✅ Created {category}.html on GitHub")

def add_product(amazon_url, category):
    title, image, price = scrape_amazon(amazon_url)
    html = generate_product_html(title, image, price, amazon_url)
    update_category_page(category, html)

# ===================== RUN BOT =====================
if __name__ == "__main__":
    print("=== Amazon Affiliate Bot Mode B ===")
    while True:
        url = input("Enter Amazon product URL (or 'exit' to quit): ").strip()
        if url.lower() == "exit":
            break
        category = input("Enter category (fashion/beauty/electronics/home): ").strip().lower()
        add_product(url, category)
        print("✅ Product added successfully!\n")




