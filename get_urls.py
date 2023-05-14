import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def scrape_urls(url):
    attempt = 0
    max_attempts = 5

    while attempt < max_attempts:
        try:
            start_time = time.time()

            # Konfigurasi Selenium
            chrome_options = Options()
            chrome_options.add_argument("--headless")

            # Membuat objek WebDriver
            driver = webdriver.Chrome(options=chrome_options)

            # Mengunjungi URL dengan Selenium
            driver.get(url)

            # Mendapatkan konten HTML yang sudah dirender
            rendered_html = driver.page_source

            # Membuat objek BeautifulSoup dari konten HTML
            soup = BeautifulSoup(rendered_html, 'html.parser')

            # Menemukan parent elemen yang ingin di scrape
            links = soup.find('ul', class_="css-1w5tqa5").find_all('li')

            # Mengolah hasil scraping sesuai kebutuhan
            url_list = [f"https://www.myer.com.au{link.find('h3', class_='h5 css-181jwkd').find('a')['href']}" for link in links]
            id_api = [link.find('div', class_="inlineRating").find('div')['data-bv-product-id'] for link in links]

            # Menutup WebDriver
            driver.quit()

            elapsed_time = time.time() - start_time
            print(f"Elapsed time: {elapsed_time:.2f} seconds")

            return url_list, id_api

        except Exception as e:
            attempt += 1
            print(f"Exception occurred: {e}. Retrying {attempt}/{max_attempts}...")
            driver.quit()

    print(f"Failed to retrieve data from URL {url} after {max_attempts} attempts.")
    return [], []


if __name__ == "__main__":
    # Daftar URL yang ingin Anda scrape
    base_url = "https://www.myer.com.au/c/men/mens-clothing/casual-shirts?pageNumber="
    total_pages = 51
    urls = [base_url + str(page) for page in range(1, total_pages + 1)]

    # Mengumpulkan data URL
    data = {
        "urls": [],
        "id_api": []
    }

    # Memantau proses scraping
    print("[GET URL] - Memulai proses scraping...")

    for index, url in enumerate(urls):
        print(f"Mengambil data dari URL: {url}")

        # Memperbarui data URL
        scraped_urls, scraped_ids = scrape_urls(url)
        data["urls"].extend(scraped_urls)
        data["id_api"].extend(scraped_ids)

        # Menampilkan progress
        progress = (index + 1) / len(urls) * 100
        print(f"Progress [GET URL]: {progress:.2f}%")

    # Membuat folder result/json/urls jika belum ada
    output_folder = "result/json"
    os.makedirs(output_folder, exist_ok=True)

    # Menyimpan data dalam format JSON
    output_file = os.path.join(output_folder, "url-id.json")
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)

    # Proses scraping selesai
    print("[GET URL] - proses scraping selesai.")
