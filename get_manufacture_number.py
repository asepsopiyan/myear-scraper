import os
import requests
import json
import time


def scrape_manufacture_number(url):
    attempt = 0
    max_attempts = 5

    while attempt < max_attempts:
        try:
            start_time = time.time()

            # Mengirim permintaan GET ke URL
            response = requests.get(url)

            # Memeriksa apakah permintaan berhasil
            if response.status_code == 200:
                data_json = json.loads(response.text)
                # Mengakses bagian "Results" dari JSON
                results = data_json['Results']

                # Memeriksa apakah "Results" memiliki item
                if len(results) > 0:
                    # Mengakses item pertama dalam "Results"
                    result = results[0]

                    # Mengambil data yang diinginkan
                    brand = result["Brand"]["Name"]
                    manufacture_number = result["ManufacturerPartNumbers"]
                    url = result["ProductPageUrl"]

                    # Mengumpulkan data dalam dictionary
                    data = {
                        "brand": brand,
                        "manufacture_number": manufacture_number,
                        "url": url
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
    input_file = "result/json/url-id.json"
    with open(input_file, "r") as file:
        data = json.load(file)

    # Mengumpulkan data dari setiap URL
    result = []
    total_urls = len(data["id_api"])

    print("[GET MANUFACTURE NUMBER] - Memulai proses scraping...")

    for index, id in enumerate(data["id_api"]):
        url = f"https://api.bazaarvoice.com/data/products.json?passkey=ca3JzrHhYAFG98Vhal06rzBxGsYnsrGMhTPa43TZTylqM&locale=en_AU&allowMissing=true&apiVersion=5.4&filter=id:{id}"
        print(f"Mengambil data dari URL: {url}")
        scraped_manufacture_number = scrape_manufacture_number(url)

        if scraped_manufacture_number is not None:
            result.append(scraped_manufacture_number)

        # Menampilkan progress
        progress = (index + 1) / total_urls * 100
        print(f"Progress [GET MANUFACTURE NUMBER]: {progress:.2f}%")

    # Menyimpan hasil scraping dalam format JSON
    output_folder = "result/json"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "manufacture_number.json")
    with open(output_file, "w") as file:
        json.dump(result, file, indent=4)

    print("[GET MANUFACTURE NUMBER] - proses scraping selesai.")