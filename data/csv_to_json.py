import csv
import json


def convert(csv_file, json_file, model):
    with open(csv_file, encoding='utf-8') as csv_f:
        result = []
        for row in csv.DictReader(csv_f):
            record = {"model": model, "pk":row["id"]}
            del row["id"]

            if "price" in row:
                row["price"] = int(row["price"])

            if "is_published" in row:
                if row["is_published"] == "True":
                    row["is_published"] = True
                else:
                    row["is_published"] = False

            if "location_id" in row:
                row["locations"] = [row["location_id"]]
                del row["location_id"]

            record["fields"] = row
            result.append(record)

    with open(json_file, 'w', encoding='utf-8') as json_f:
        json_f.write(json.dumps(result, ensure_ascii=False))


convert('category.csv', 'categories.json', 'ad.category')
convert('ad.csv', 'ads.json', 'ad.ad')
convert('location.csv', 'location.json', 'users.location')
convert('user.csv', 'user.json', 'users.user')
