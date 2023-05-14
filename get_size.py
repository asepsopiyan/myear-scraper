import os
import requests
import json
import time
from bs4 import  BeautifulSoup


def scrape_size(url,id,datas):
    attempt = 0
    max_attempts = 5

    while attempt < max_attempts:
        try:
            start_time = time.time()

            # Mengirim permintaan GET ke URL
            response = requests.get(url)

            # Memeriksa apakah permintaan berhasil
            if response.status_code == 200:

                # Membuat objek BeautifulSoup dari response
                soup = BeautifulSoup(response.text, "html.parser")
                sizes = soup.find('div', class_="css-16fbgeu").find_all('div', class_='css-fv4sox')
                id_size = [size.find('input')["value"] for size in sizes]

                data = {
                    "id": id,
                    "size": id_size,
                }



                elapsed_time = time.time() - start_time
                print(f"Elapsed time: {elapsed_time:.2f} seconds")

                return data

            else:
                raise Exception(f"Permintaan tidak berhasil. Status code: {response.status_code}")

        except Exception as e:
            attempt += 1
            print(f"Exception occurred: {e}. Retrying {attempt}/{max_attempts}...")

    print(f"Failed to retrieve data from URL {url} after {max_attempts} attempts.")
    return None


if __name__ == "__main__":
    # Memuat data URL dari file JSON
    input_file = "result/json/detail_product.json"
    with open(input_file, "r") as file:
        data = json.load(file)

    # Mengumpulkan data dari setiap URL
    result = []
    total_urls = len(data)

    print("[GET SIZE] - Memulai proses scraping...")

    for index, datas in enumerate(data):
        url = datas["url"]
        id = datas["id"]
        print(f"Mengambil data dari URL: {url}")
        scraped_size = scrape_size(url, id, datas)

        if scraped_size is not None:
            result.append(scraped_size)

        # Menampilkan progress
        progress = (index + 1) / total_urls * 100
        print(f"Progress [GET SIZE]: {progress:.2f}%")

    # Menyimpan hasil scraping dalam format JSON
    output_folder = "result/json"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "size_product.json")
    with open(output_file, "w") as file:
        json.dump(result, file, indent=4)

    print("[GET SIZE] - proses scraping selesai.")