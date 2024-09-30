import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# Removing html tags
def remove_html_tags(text:str):
    """
    This method removing HTML tags from text.
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def is_skapiec_url(url:str)->bool:
    """
    Method takes url and check if it is from skapiec, if yes returns True, if no returns False
    """
    return url.startswith('/site/')

# Scraping method with automatic pagination
def scrapping(phrase:str, pages:int):
    """
    This function takes a phrase as an argument, searches for items on the skapiec.pl website using BeautifulSoup.
    It parses the data, finds specific data by HTML tags: name, price, PNG, internal URL, external URL,
    and saves everything to a list, then returns that list.
    """
    product_info = []
    page = 1

    while page <= int(pages):
        # Loading skapiec page with pagination, parsing html
        url = f"https://www.skapiec.pl/szukaj?query={phrase}&page={page}&sort=score"
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Finding data with bs4 by tags
            products = soup.find_all('h2', title=True)
            prices = soup.find_all('span', class_='price')
            internal_urls = soup.find_all('a', class_='product-box-narrow__title')
            photos = soup.find_all('div', class_='product-box-narrow__photo-box-image')
            external_urls = soup.find_all('a', class_='button button--primary button--md button--fw-500 product-box-narrow__button product-box-narrow__button--shop')
            # Consistency check
            if len(products) == len(prices):
                # Getting data and appending to list
                for product, price, internal_url, photo, external_url in zip(products, prices, internal_urls, photos, external_urls):
                    name = product['title']
                    price_value = price.get_text().replace('\xa0zł', '').replace(',', '.')
                    skapiec_url = internal_url['href'] if internal_url else None
                    photo = photo.find('img')['src'] if photo.find('img') else None
                    shop_url = external_url['href'] if external_url else None
                    product_info.append({'name': name, 'price': price_value, 'internal_url': skapiec_url, 'photo': photo, 'external_url': shop_url, 'page': page})
            else:
                print("Number of products and prices doesn't match.")
            page += 1  # Move to the next page
        else:
            print(f"Failed to fetch page {page}. Status code: {r.status_code}")
            break

    return product_info

if __name__ == '__main__':
    # Take phrase from user and scrap!
    search_phrase = input("Enter phrase: ")
    result = scrapping(search_phrase)
    if result:
        for item in result:
            skapiec_url = item['internal_url'] if item['internal_url'] else "Brak"
            shop_url = item['external_url'] if item['external_url'] else "brak"
            is_skapiec = is_skapiec_url(skapiec_url)
            print(f"Page: {item['page']}, Name: {item['name']}, Price: {item['price']} , Internal URL: {'skapiec.pl'+skapiec_url}, External URL: {shop_url}, Photo: {item['photo']}, Is from skapiec: {is_skapiec}\n")
    else:
        print("No matches found")
