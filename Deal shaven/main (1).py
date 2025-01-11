import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def scrape_deals(store_name, start, end, csv_filename):
    """Function to scrape product deals from the DealsHeaven website."""
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Image", "Price", "Discount", "Special Price", "Link", "Rating"])

        for current_page in range(start, end + 1):
            url = f"https://dealsheaven.in/store/{store_name.lower()}?page={current_page}"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to retrieve page {current_page}. Skipping...")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            all_items = soup.find_all("div", class_="product-item-detail")

            if not all_items:
                print(f"No products found on page {current_page}. Stopping scraper.")
                break

            for item in all_items:
                product = {}

                discount = item.find("div", class_="discount")
                product['Discount'] = discount.text.strip() if discount else "N/A"

                link = item.find("a", href=True)
                product['Link'] = link['href'] if link else "N/A"

                image = item.find("img", src=True)
                product['Image'] = image['data-src'] if image else "N/A"

                details_inner = item.find("div", class_="deatls-inner")

                title = details_inner.find("h3", title=True) if details_inner else None
                product['Title'] = title['title'].replace("[Apply coupon] ", "").replace('"', '') if title else "N/A"

                price = details_inner.find("p", class_="price") if details_inner else None
                product['Price'] = f"{price.text.strip().replace(',', '')}" if price else "N/A"

                s_price = details_inner.find("p", class_="spacail-price") if details_inner else None
                product['Special Price'] = f"{s_price.text.strip().replace(',', '')}" if s_price else "N/A"

                rating = details_inner.find("div", class_="star-point") if details_inner else None
                if rating:
                    style_width = rating.find("div", class_="star") if rating else None
                    if style_width:
                        percent = style_width.find("span", style=True) if style_width else None
                        if percent:
                            style = percent['style']
                            width_percentage = int(style.split(":")[1].replace('%', '').strip())
                            stars = round((width_percentage / 100) * 5, 1)
                            product['Rating'] = stars
                        else:
                            product['Rating'] = "N/A"
                    else:
                        product['Rating'] = "N/A"
                else:
                    product['Rating'] = "N/A"

                writer.writerow([product.get('Title', 'N/A'), product.get("Image", "N/A"), product.get('Price', 'N/A'), product.get('Discount', 'N/A'), product.get('Special Price', 'N/A'), product.get("Link", "N/A"), product.get('Rating', 'N/A')])

def get_deals(csv_filename):
    """Function to read CSV data."""
    return pd.read_csv(csv_filename)