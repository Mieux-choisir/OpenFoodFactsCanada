import logging
import ijson
import json


def show_all_fields():
    """Shows the names of all the fields in the documentation"""
    filename = r"../../off_csv_fields_descriptions.json"

    fields_list = "Fields of the csv file for Open Food Facts:"
    with open(filename, "r", encoding="utf-8") as file:
        for obj in ijson.items(file, "fields.item"):
            fields_list += f"\n\t{obj['name']}"
    logging.info(fields_list)


def show_field_description(field_name):
    """Shows the description of a given field name in the documentation"""
    filename = r"../../off_csv_fields_descriptions.json"

    field_description = f"Information about {field_name}:"
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        fields = data.get("fields", [])

        field = next(
            (document for document in fields if document.get("name") == field_name),
            None,
        )

        if field:
            for item in field.keys():
                field_description += f"\n\t{item}: {field[item]}"
        else:
            field_description += (
                f"\n\tnot found: {field_name} is not a field in the CSV file"
            )

        logging.info(field_description)


def show_all_fields_descriptions():
    """Shows the descriptions of all the fields in the documentation"""
    filename = r"../../off_csv_fields_descriptions.json"

    fields_descriptions = ""
    with open(filename, "r", encoding="utf-8") as file:
        for field in ijson.items(file, "fields.item"):
            fields_descriptions += f"\nInformation about {field['name']}:"
            for item in field.keys():
                fields_descriptions += f"\n\t{item}: {field[item]}"
    logging.info(fields_descriptions)