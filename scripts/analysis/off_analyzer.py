import logging
import csv
import json

def analyze_off_csv_data(filename: str, limit: int = None) -> None:
    if limit is not None:
        logging.info(f"Analyzing the data of {limit} products from Open Food Facts csv dataset...")
    else:
        logging.info("Analyzing the data of all products from Open Food Facts csv dataset...")

    # Increase the CSV field size limit to avoid the error:
    # _csv.Error: field larger than field limit (131072)
    csv.field_size_limit(2 ** 30)

    n = 0
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)

        fields_types = dict.fromkeys(header, [])

        for row in reader:
            for field_index in range(len(header)):
                field, field_value = header[field_index], row[field_index]
                if not type(field_value) in fields_types[field]:
                    fields_types[field].append(type(field_value))

            n += 1

            if limit is not None and n >= limit:
                break

    logging.info("OFF data analyzed.")
    result = ""
    for field in fields_types:
        result += f"\n\t{field}: {fields_types[field]}"
    logging.info(result)


def analyze_off_jsonl_data(filename: str, nonetype_included: bool, limit: int = None) -> None:
    if limit is not None:
        logging.info(f"Analyzing the data of {limit} products from Open Food Facts jsonl dataset...")
    else:
        logging.info("Analyzing the data of all products from Open Food Facts jsonl dataset...")

    # Increase the CSV field size limit to avoid the error:
    # _csv.Error: field larger than field limit (131072)
    csv.field_size_limit(2 ** 30)

    n = 0
    with (open(filename, "r", encoding="utf-8") as file):
        fields_types = {}
        fields_can_be_none = set()

        for line in file:
            try:
                obj = json.loads(line.strip())

                for key in obj.keys():
                    if nonetype_included or obj[key] is not None:
                        if key not in fields_types.keys():
                            fields_types[key] = {type(obj[key]): 1}
                        elif not type(obj[key]) in fields_types[key].keys():
                            fields_types[key][type(obj[key])] = 1
                        else:
                            fields_types[key][type(obj[key])] += 1
                    elif key not in fields_types.keys():
                        fields_types[key] = {}

                    if obj[key] is None:
                        fields_can_be_none.add(key)

                n += 1

                if limit is not None and n >= limit:
                    break

            except json.JSONDecodeError as e:
                logging.info(f"Error parsing line: {line}. Error: {e}")

    logging.info("OFF data analyzed.")
    result = ""
    for field in fields_types:
        result += f"\n\t{field}: {fields_types[field]}"
    logging.info(f"{result}\n")

    result2 = ""
    for value in fields_can_be_none:
        result2 += f"\n\t {value}"
    logging.info(f"{len(fields_can_be_none)} out of {len(fields_types)} fields can be None : {result2}")



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    # analyze_off_csv_data(r"C:\Users\estre\Documents\stage\bds\off\full\en.openfoodfacts.org.products.csv\en.openfoodfacts.org.products.csv", 10)
    analyze_off_jsonl_data(r"C:\Users\estre\Documents\stage\bds\off\full\filtered_canada_products.json", False)
