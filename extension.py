import csv
import json


def read_csv(filename):
    data = []
    with open('./{}.csv'.format(filename), 'r', newline='', encoding='utf-8') as cvs:
        reader = csv.reader(cvs)
        for item in reader:
            data.append(item)
    # Don't send the header row
    return data[1:]


def save_json(scraped_data):
    json_data = json.dumps(scraped_data, indent=4)
    with open('./items.json', 'w', encoding='utf-8') as file:
        file.write(json_data)


if __name__ == "__main__":
    print("Import this file for using Extensions")
