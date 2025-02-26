import logging
import csv
import json
from datetime import datetime
import ijson


def analyze_off_csv_data(filename: str, nonetype_included: bool, limit: int = None) -> (dict, set):
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

        fields_types = {}
        fields_can_be_none = set()

        for row in reader:
            for field_index in range(len(header)):
                field, field_value = header[field_index], row[field_index]

                field_type = get_field_type(field, field_value)

                if nonetype_included or field_type != type(None).__name__:
                    if field not in fields_types.keys():
                        fields_types[field] = {field_type: 1}
                    elif field_type not in fields_types[field].keys():
                        fields_types[field][field_type] = 1
                    else:
                        fields_types[field][field_type] += 1
                elif field not in fields_types.keys():
                    fields_types[field] = {}

                if field_type == type(None).__name__:
                    fields_can_be_none.add(field)

            n += 1

            if limit is not None and n >= limit:
                break

    logging.info("OFF data analyzed.")
    show_fields_report(fields_types, fields_can_be_none)

    return fields_types, fields_can_be_none


def get_field_type(field: str, field_value: str) -> str:
    field_type = get_particular_cases_type(field, field_value)

    if not field_type:
        field_type = type(None).__name__

        if value_is_int(field_value):
            field_type = int.__name__
        elif value_is_float(field_value):
            field_type = float.__name__
        elif value_is_list(field_value):
            field_type = list.__name__
        elif value_is_string(field_value):
            field_type = str.__name__

    return field_type


def get_particular_cases_type(field: str, field_value: str) -> str:
    if field_value == "":
        return type(None).__name__
    if field == "code" or "_name" in field:
        return str.__name__
    if "_tags" in field:
        return list.__name__
    if "_100g" in field:
        return float.__name__
    if "_t" in field[:-2]:
        return int.__name__
    if "_datetime" in field:
        return datetime.__name__
    return None


def value_is_float(field_value: str) -> bool:
    is_float = False
    try:
        float(field_value)
        is_float = True
    except ValueError:
        pass
    return is_float


def value_is_int(field_value: str) -> bool:
    return field_value.isdigit()


def value_is_list(field_value: str) -> bool:
    return ',' in field_value


def value_is_string(field_value: str) -> bool:
    return field_value != ''


def analyze_off_jsonl_data(filename: str, nonetype_included: bool, limit: int = None) -> (dict, set):
    if limit is not None:
        logging.info(f"Analyzing the data of {limit} products from Open Food Facts jsonl dataset...")
    else:
        logging.info("Analyzing the data of all products from Open Food Facts jsonl dataset...")

    n = 0
    with (open(filename, "r", encoding="utf-8") as file):
        fields_types = {}
        fields_can_be_none = set()

        for line in file:
            try:
                obj = json.loads(line.strip())

                fields_types, fields_can_be_none = analyze_obj(obj, fields_types, fields_can_be_none, nonetype_included)

                n += 1

                if limit is not None and n >= limit:
                    break

            except json.JSONDecodeError as e:
                logging.info(f"Error parsing line: {line}. Error: {e}")

    logging.info("OFF data analyzed.")
    show_fields_report(fields_types, fields_can_be_none)

    return fields_types, fields_can_be_none


def analyze_fdc_data(filename: str, nonetype_included: bool, limit: int = None) -> (dict, set):
    if limit is not None:
        logging.info(f"Analyzing the data of {limit} products from Food Data Central dataset...")
    else:
        logging.info("Analyzing the data of all products from Food Data Central dataset...")

    n = 0

    with (open(filename, "r", encoding="utf-8") as file):
        fields_types = {}
        fields_can_be_none = set()

        for obj in ijson.items(file, "BrandedFoods.item"):
            fields_types, fields_can_be_none = analyze_obj(obj, fields_types, fields_can_be_none, nonetype_included)

            n += 1

            if limit is not None and n >= limit:
                break

    logging.info("FDC data analyzed.")
    show_fields_report(fields_types, fields_can_be_none)

    return fields_types, fields_can_be_none


def analyze_obj(obj: dict, fields_types: dict, fields_can_be_none: set, nonetype_included: bool) -> (dict, set):
    for key in obj.keys():
        fields_types = add_type_to_dict(fields_types, key, obj[key], nonetype_included)

        if obj[key] is None:
            fields_can_be_none.add(key)

    return fields_types, fields_can_be_none


def add_type_to_dict(fields_types, key, value, nonetype_included: bool):
    if nonetype_included or value is not None:
        if key not in fields_types.keys():
            fields_types[key] = {type(value).__name__: 1}
        elif not type(value).__name__ in fields_types[key].keys():
            fields_types[key][type(value).__name__] = 1
        else:
            fields_types[key][type(value).__name__] += 1
    elif key not in fields_types.keys():
        fields_types[key] = {}

    return fields_types


def show_fields_report(fields_types: dict, fields_can_be_none: set) -> None:
    types = "Analyzed fields types:"
    for field in fields_types:
        types += f"\n\t{field}: {fields_types[field]}"
    logging.info(f"{types}\n")

    possible_nonetypes = ""
    for value in fields_can_be_none:
        possible_nonetypes += f"\n\t {value}"
    logging.info(f"{len(fields_can_be_none)} out of {len(fields_types)} fields can be None : {possible_nonetypes}")


def show_inconsistent_fields(field_types: dict) -> None:
    inconsistent_fields = {}
    for field in field_types.keys():
        if len([key for key in field_types[field].keys() if key != 'NoneType']) > 1:
            inconsistent_fields[field] = list(field_types[field].keys())

    logging.info(f"Inconsistent fields: {inconsistent_fields}")


def record_values_for_field_off_csv(field_name: str, show_values: bool, filename: str, limit: int = None) -> set:
    if limit is not None:
        logging.info(f"Recording values from {limit} items for {field_name} field from Open Food Facts csv dataset...")
    else:
        logging.info(f"Recording all values for {field_name} field from Open Food Facts csv dataset...")

    # Increase the CSV field size limit to avoid the error:
    # _csv.Error: field larger than field limit (131072)
    csv.field_size_limit(2 ** 30)

    n = 0
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        values = set()

        for row in reader:
            idx = header.index(field_name)
            if row[idx] != '':
                values.add(row[idx])

            n += 1

            if limit is not None and n >= limit:
                break

    if show_values:
        show_set_values(values)

    logging.info(f"values for {field_name} field recorded")
    return values


def record_values_for_field_off_jsonl(field_name: str, show_values: bool, filename: str, limit: int = None) -> set:
    if limit is not None:
        logging.info(f"Recording values from {limit} items for {field_name} field from Open Food Facts jsonl dataset...")
    else:
        logging.info(f"Recording all values for {field_name} field from Open Food Facts jsonl dataset...")

    n = 0
    with open(filename, "r", encoding="utf-8") as file:
        values = set()
        for line in file:
            try:
                obj = json.loads(line.strip())
                value = obj[field_name]
                if value != '' and value is not None:
                    values.add(value)

                n += 1

                if limit is not None and n > limit:
                    break

            except json.JSONDecodeError as e:
                logging.info(f"Error parsing line: {line}. Error: {e}")

    if show_values:
        show_set_values(values)

    logging.info(f"values for {field_name} field recorded")
    return values


def record_values_for_field_fdc(field_name: str, show_values: bool, filename: str, limit: int = None) -> set:
    if limit is not None:
        logging.info(f"Recording values from {limit} items for {field_name} field from Food Data Central dataset...")
    else:
        logging.info(f"Recording all values for {field_name} field from Food Data Central dataset...")

    n = 0
    with open(filename, "r", encoding="utf-8") as file:
        values = set()
        for obj in ijson.items(file, "BrandedFoods.item"):
            value = obj[field_name]
            if value != '' and value is not None:
                values.add(value)

            n += 1

            if limit is not None and n > limit:
                break

    if show_values:
        show_set_values(values)

    logging.info(f"values for {field_name} field recorded")
    return values


def show_set_values(set_values: set) -> None:
    values_list = ""
    for value in set_values:
        values_list += f"\n\t{value}"
    logging.info(f"Values found:{values_list}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    off_csv_field_types, off_csv_none = analyze_off_csv_data(
        r"C:\Users\estre\Documents\stage\bds\off\full\en.openfoodfacts.org.products.csv\en.openfoodfacts.org.products.csv", False, 1000)
    off_jsonl_field_types, off_jsonl_none = analyze_off_jsonl_data(r"C:\Users\estre\Documents\stage\bds\off\full\filtered_canada_products.json", False, 1000)
    fdc_field_types, fdc_none = analyze_fdc_data(r"C:\Users\estre\Documents\stage\bds\fdc\FoodData_Central_branded_food_json_2024-10-31\brandedDownload.json",
                                                 False, 1000)

    fdc_field_types, fdc_none = analyze_fdc_data(r"C:\Users\estre\Documents\stage\bds\fdc\FoodData_Central_branded_food_json_2024-10-31\brandedDownload.json",
                                                 False, 1000)

    show_inconsistent_fields(off_csv_field_types)
    show_inconsistent_fields(off_jsonl_field_types)
    show_inconsistent_fields(fdc_field_types)

    record_values_for_field_off_csv("nutriscore_grade", True,
                            r"C:\Users\estre\Documents\stage\bds\off\full\en.openfoodfacts.org.products.csv\en.openfoodfacts.org.products.csv", 100)
    record_values_for_field_off_jsonl("nutriscore_grade", True, r"C:\Users\estre\Documents\stage\bds\off\full\filtered_canada_products.json", 100)
    record_values_for_field_fdc("brandOwner", True, r"C:\Users\estre\Documents\stage\bds\fdc\FoodData_Central_branded_food_json_2024-10-31\brandedDownload.json", 100)
