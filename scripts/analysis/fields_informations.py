import logging
import ijson
import json


def read_descriptions():
    path = r"C:\Users\estre\Documents\stage\fields_off_csv.txt"
    with open(path, "r", encoding="utf-8") as file:
        logging.info("Showing fields...")
        for obj in ijson.items(file, "fields.item"):
            print(obj)
    logging.info("FIELDS SHOWN")


def show_all_fields():
    path = r"C:\Users\estre\Documents\stage\off_csv_fields_description.txt"
    fields_list = "Fields of the csv file for Open Food Facts:"
    with open(path, "r", encoding="utf-8") as file:
        for obj in ijson.items(file, "fields.item"):
            fields_list += f"\n\t{obj['name']}"
    logging.info(fields_list)


def show_field_description(field_name):
    path = r"C:\Users\estre\Documents\stage\off_csv_fields_description.txt"
    field_description = f"Information about {field_name}:"
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        fields = data.get('fields', [])

        field = next((document for document in fields if document.get("name") == field_name), None)

        if field:
            for item in field.keys():
                field_description += f"\n\t{item}: {field[item]}"
        else:
            field_description += f"\n\tnot found: {field_name} is not a field in the CSV file"

        logging.info(field_description)


def show_all_fields_descriptions():
    path = r"C:\Users\estre\Documents\stage\off_csv_fields_description.txt"
    fields_descriptions = ""
    with open(path, "r", encoding="utf-8") as file:
        for field in ijson.items(file, "fields.item"):
            fields_descriptions += f"\nInformation about {field['name']}:"
            for item in field.keys():
                fields_descriptions += f"\n\t{item}: {field[item]}"
    logging.info(fields_descriptions)
