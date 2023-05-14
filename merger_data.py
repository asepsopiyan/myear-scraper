import json
import csv
import os


def merge_data(detail_product_file, size_product_file):
    with open(detail_product_file, 'r') as f1:
        detail_data = json.load(f1)
    with open(size_product_file, 'r') as f2:
        size_data = json.load(f2)

    id_to_size = {item['id']: item['size'] for item in size_data}

    merged_data = []

    for detail_item in detail_data:
        product_id = detail_item['id']
        if product_id in id_to_size:
            detail_item['size'] = id_to_size[product_id]
            merged_data.append(detail_item)

    return merged_data

def save_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

def save_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def create_directories(output_json_file, output_csv_file):
    os.makedirs(os.path.dirname(output_json_file), exist_ok=True)
    os.makedirs(os.path.dirname(output_csv_file), exist_ok=True)

# Ubah 'main' menjadi 'merge_and_save'
def merge_and_save():
    detail_product_file = 'result/json/detail_product.json'
    size_product_file = 'result/json/size_product.json'
    output_json_file = 'result/json/merged_data.json'
    output_csv_file = 'result/csv/merged_data.csv'

    create_directories(output_json_file, output_csv_file)

    merged_data = merge_data(detail_product_file, size_product_file)
    save_to_json(merged_data, output_json_file)
    save_to_csv(merged_data, output_csv_file)

if __name__ == '__main__':
    merge_and_save()
