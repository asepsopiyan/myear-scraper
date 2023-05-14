import os
import requests
import json
import time


def scrape_data(url, url_product):
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
                results = data_json

                # Memeriksa apakah "Results" memiliki item
                if len(results["productList"]) > 0:
                    for product in results["productList"]:
                        # Mengambil data yang diinginkan
                        id = product["id"]
                        name = product["name"]
                        brand = product["brand"]
                        seo_token = product["seoToken"]
                        variant_data = product["variantData"]
                        id_list = [data["id"] for data in variant_data]

                        response_stock = requests.get(
                            f"https://api-online.myer.com.au/v2/product/productsupplemental?products={id}&itemDetails=true")
                        stock_json = json.loads(response_stock.text)
                        stock_indicator = stock_json["productList"][0]["stockIndicator"]



                        # Mengumpulkan data dalam dictionary
                        data = {
                            "id": id,
                            "name": name,
                            "brand": brand,
                            "seoToken": seo_token,
                            "variantDataIds": id_list,
                            "stockIndicator": stock_indicator,
                            "url": url_product
                        }

                        # Memassukan data ke result
                        result.append(data)
                else:
                    print("Tidak ada data yang ditemukan dalam productList.")

                elapsed_time = time.time() - start_time
                print(f"Elapsed time: {elapsed_time:.2f} seconds")

                return

            else:
                raise Exception(f"Permintaan tidak berhasil. Status code: {response.status_code}")

        except Exception as e:
            attempt += 1
            print(f"Exception occurred: {e}. Retrying {attempt}/{max_attempts}...")

    print(f"Failed to retrieve data from URL {url} after {max_attempts} attempts.")


if __name__ == "__main__":
    # Memuat data URL dari file JSON
    input_file = "result/json/manufacture_number.json"
    with open(input_file, "r") as file:
        data = json.load(file)

    # Mengumpulkan data dari setiap URL
    result = []
    total_urls = len(data)

    print("[GET DATA] - Memulai proses scraping...")

    for index, ids in enumerate(data):
        brand = ids['brand'].replace(" ", "%2520") + "%2520"
        m_number = ids['manufacture_number'][0]
        url_product = ids['url']
        url = f"https://api-online.myer.com.au/v3/product/collection?facetId=shop_by_colour&facetValue={brand}{m_number}"
        print(f"Mengambil data dari URL: {url}")
        scrape_data(url, url_product)

        # Menampilkan progress
        progress = (index + 1) / total_urls * 100
        print(f"Progress [GET DATA]: {progress:.2f}%")

    # Menyimpan hasil scraping dalam format JSON
    output_folder = "result/json"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "detail-product.json")
    with open(output_file, "w") as file:
        json.dump(result, file, indent=4)

    print("[GET DATA] - proses scraping selesai.")