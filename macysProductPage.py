from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def extract_product_links(search_url):
    options = Options()
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)
    time.sleep(5)

    # Scroll to load all content
    for _ in range(10):
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(2)

    product_links = []

    # Select all <a> tags with class 'brand-and-name'
    anchor_tags = driver.find_elements(By.CSS_SELECTOR, "a.brand-and-name")
    for tag in anchor_tags:
        href = tag.get_attribute("href")
        if href:
            full_link = "https://www.macys.com" + href if href.startswith("/") else href
            product_links.append(full_link)

    driver.quit()
    return product_links

def extract_product_details(link):
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(link)
    time.sleep(5)

    try:
        # Product title
        try:
            title = driver.find_element(By.CSS_SELECTOR, "label[itemprop='brand'] a").text.strip()
        except:
            title = driver.title.strip()

        # Price
        try:
            price = driver.find_element(By.CSS_SELECTOR, "span[role='text'][aria-label^='Current Price']").text.strip()
        except:
            price = "N/A"

        # Sizes
        try:
            size_elements = driver.find_elements(By.CSS_SELECTOR, "span[id^='span']")
            sizes = [s.text.strip() for s in size_elements if s.text.strip() and len(s.text.strip()) <= 4]
            sizes = ', '.join(list(set(sizes))) if sizes else "N/A"
        except:
            sizes = "N/A"

        # Image
        # Image extraction block (updated)
        try:
            image_tag = driver.find_element(By.CSS_SELECTOR, "img.picture-image.stylitics-shop-similar")
            image = image_tag.get_attribute("src") or image_tag.get_attribute("data-src")
        except:
            image = "N/A"

        driver.quit()
        return {
            "Brand": "Macy",
            "Product Title": title,
            "Price": price,
            "Sizes": sizes,
            "Image": image,
            "Link": link
        }

    except Exception as e:
        driver.quit()
        print(f"Failed to extract product: {link} | Error: {e}")
        return None

if __name__ == "__main__":
    query = "woman shoes"
    csv_file = "macys_products.csv"

    # Open CSV and write header once
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Brand", "Product Title", "Price", "Sizes", "Link"])
        writer.writeheader()

        # Loop through pages 1 to 20
        for page in range(1, 21):
            url = f"https://www.macys.com/shop/featured/{query}/Pageindex,Productsperpage/{page},120?ss=true"
            print(f"\n[🌐] Scraping Page {page}...\n[+] Getting product links...")
            links = extract_product_links(url)
            print(f"[✅] FOUND {len(links)} LINKS ON PAGE {page}.\n")

            for idx, link in enumerate(links, 1):
                print(f"[{idx}/{len(links)}] Scraping: {link}")
                product_data = extract_product_details(link)

                if product_data:
                    writer.writerow(product_data)

                    print(f"✅ {product_data['Product Title']}")
                    print(f"   Brand: {product_data['Brand']}")
                    print(f"   Price: {product_data['Price']}")
                    print(f"   Sizes: {product_data['Sizes']}")
                    print(f"   Link: {product_data['Link']}\n")
                else:
                    print("❌ Failed to extract product details.\n")

    print(f"\n[🎉] DONE! Data from all 20 pages saved to '{csv_file}'")
