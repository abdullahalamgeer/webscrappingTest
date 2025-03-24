# 🛍 Macy's Product Scraper API

This project is a **Flask-based web API** that scrapes product data from [macys.com](https://www.macys.com) based on a search query provided via URL.

It extracts key product information from Macy’s product listings including:

- Product Title  
- Price  
- Available Sizes  
- Product Image  
- Product Link  
- Brand (fixed as "Macy")

This is useful for market research, competitor analysis, or simply collecting product data in bulk for testing purposes.

---

## 🚀 Features

✅ Accepts a `query` parameter via GET request  
✅ Scrapes 2 products per page from page 1 to 20  
✅ Extracts product details from each link  
✅ Returns results as clean JSON  
✅ Includes sample CSV export (`macys_products.csv`)  
✅ Lightweight and simple to deploy

---

## 📁 Repository Structure

| File | Description |
|------|-------------|
| `api.py` | Flask API entry point |
| `macysData.py` | Handles page-level scraping and product link extraction |
| `macysProductPage.py` | Handles scraping detailed product data (title, price, sizes, image) |
| `macys_products.csv` | Sample output file from scraping |
| `requirements.txt` | Required Python libraries for the project |

---

## 🧰 Requirements

- Python 3.7+
- Google Chrome installed
- ChromeDriver (auto-installed using `webdriver-manager`)
- Internet connection (real-time scraping)

---

## 🔧 Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/macys-scraper-api.git
cd macys-scraper-api
