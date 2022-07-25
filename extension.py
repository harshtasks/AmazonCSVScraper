import csv
import json


def read_csv(filename):
    data = []
    try:
        with open('./{}.csv'.format(filename), 'r', newline='', encoding='utf-8') as cvs:
            reader = csv.reader(cvs)
            for item in reader:
                data.append(item)
        # Don't send the header row
        return data[1:]
    except:
        return []


def save_json(scraped_data, file_name):
    json_data = json.dumps(scraped_data, indent=4)
    try:
        with open('./{}.json'.format(file_name), 'w', encoding='utf-8') as file:
            file.write(json_data)
    except:
        print("Could not create {}.json".format(file_name))


if __name__ == "__main__":
    print("Import this file for using Extensions")
